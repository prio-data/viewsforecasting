from typing import Optional, Union
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.base import BaseEstimator
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.dummy import DummyClassifier

from sklearn.ensemble import HistGradientBoostingRegressor, HistGradientBoostingClassifier
from xgboost import XGBRegressor, XGBClassifier, XGBRFRegressor, XGBRFClassifier
from lightgbm import LGBMClassifier, LGBMRegressor


class HurdleRegression(BaseEstimator):
    """ Regression model which handles excessive zeros by fitting a two-part model and combining predictions:
            1) binary classifier
            2) continuous regression
    Implementeted as a valid sklearn estimator, so it can be used in pipelines and GridSearch objects.
    Args:
        clf_name: currently supports either 'logistic' or 'LGBMClassifier'
        reg_name: currently supports either 'linear' or 'LGBMRegressor'
        clf_params: dict of parameters to pass to classifier sub-model when initialized
        reg_params: dict of parameters to pass to regression sub-model when initialized
    """
    # Define the constructor method for the class
    def __init__(self,
                 clf_name: str = 'logistic', # name of the classifier to use
                 reg_name: str = 'linear', # name of the regressor to use
                 clf_params: Optional[dict] = None,
                 reg_params: Optional[dict] = None):

        self.clf_name = clf_name
        self.reg_name = reg_name
        self.clf_params = clf_params
        self.reg_params = reg_params

    @staticmethod
    def _resolve_estimator(estimator_name: str):
        """ Lookup table for supported estimators.
        This is necessary because sklearn estimator default arguments
        must pass equality test, and instantiated sub-estimators are not equal. """

        estimators = {
                    'logistic': LogisticRegression(solver='liblinear'),
                    'linear': LinearRegression(),
                    
                    'LGBMClassifier': LGBMClassifier(n_estimators=250),
                    'LGBMRegressor': LGBMRegressor(n_estimators=250),

                    'RFClassifier': XGBRFClassifier(n_estimators=250,n_jobs=-2),
                    'RFRegressor': XGBRFRegressor(n_estimators=250,n_jobs=-2),

                    'GBMClassifier': GradientBoostingClassifier(n_estimators=200),
                    'GBMRegressor': GradientBoostingRegressor(n_estimators=200),

                    'XGBClassifier': XGBClassifier(n_estimators=100,learning_rate=0.05,n_jobs=-2),
                    'XGBRegressor': XGBRegressor(n_estimators=100,learning_rate=0.05,n_jobs=-2),

                    'HGBClassifier': HistGradientBoostingClassifier(max_iter=200),
                    'HGBRegressor': HistGradientBoostingRegressor(max_iter=200),
                }
        estimator = estimators.get(estimator_name)

        return estimator

    # Define the fit method for the class to train the model
    def fit(self,
            X: Union[np.ndarray, pd.DataFrame],
            y: Union[np.ndarray, pd.Series]):
        
        # Use sklearn fucntionality to check X and y for consistent length and enforce X to be 2D and y 1D. 
        # By default, X is checked to be non-empty and containing only finite values.
        # Standard input checks are also applied to y, such as checking that y
        # does not have np.nan or np.inf targets.
        X, y = check_X_y(X, 
                         y, 
                         dtype=None,
                         accept_sparse=False,
                         accept_large_sparse=False,
                         force_all_finite=True) #'allow-nan'
        
        # Set the number of features seen during fit
        self.n_features_in_ = X.shape[1]

        if X.shape[1] < 2:
            raise ValueError('Cannot fit model when n_features = 1')

        self.clf_ = self._resolve_estimator(self.clf_name)
        if self.clf_params:
            self.clf_.set_params(**self.clf_params)
        if len(np.unique(y)) > 1:
            self.clf_.fit(X, y > 0)
        else:
            # Handle the case where y has only one unique value
            self.clf_ = DummyClassifier(strategy='most_frequent')
            self.clf_.fit(X, y > 0)

        self.reg_ = self._resolve_estimator(self.reg_name)
        if self.reg_params:
            self.reg_.set_params(**self.reg_params)
        self.reg_.fit(X[y > 0], y[y > 0])

        self.is_fitted_ = True
        return self
    
    def predict(self, X: Union[np.ndarray, pd.DataFrame]):
        """ Predict combined response using binary classification outcome """
        X = check_array(X, accept_sparse=False, accept_large_sparse=False)
        check_is_fitted(self, 'is_fitted_')
        return self.clf_.predict(X) * self.reg_.predict(X)

    def predict_expected_value(self, X: Union[np.ndarray, pd.DataFrame]):
        """ Predict combined response using probabilistic classification outcome """
        X = check_array(X, accept_sparse=False, accept_large_sparse=False)
        check_is_fitted(self, 'is_fitted_')
        return self.clf_.predict_proba(X)[:, 1] * self.reg_.predict(X)


def manual_test(clf_name:str='logistic', reg_name:str='linear'):
    """ Validate estimator using sklearn's provided utility and ensure it can fit and predict on fake dataset. """
    reg = HurdleRegression(clf_name=clf_name, reg_name=reg_name)
    check_estimator(reg)
    X, y = make_regression()
    reg.fit(X, y)
    reg.predict(X)


def test_hurdle_regression(clf_name:str='logistic', reg_name:str='linear'):
    """ Validate estimator using sklearn's provided utility and ensure it can fit and predict on fake dataset. """

    # Create a synthetic regression dataset
    X_reg, y_reg = make_regression(n_samples=1000, n_features=20, n_informative=2, random_state=42)

    # Create a synthetic classification dataset
    X_clf, y_clf = make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=10, random_state=42)

    # Combine the two datasets
    X = np.hstack([X_clf, X_reg])
    y = y_clf * y_reg

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Instantiate a HurdleRegression object
    hr = HurdleRegression(clf_name=clf_name, reg_name=reg_name)
    check_estimator(hr)
    
    # Fit the model to the data
    hr.fit(X_train, y_train)

    # Make predictions
    y_pred = hr.predict(X_test)

    # Evaluate the model
    print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
    
    # Check if predictions have the same shape as y
    print(f"Shape of y_pred: {y_pred.shape}")
    print(f"Shape of y_test: {y_test.shape}")

    assert y_pred.shape == y_test.shape, "Predictions and y do not have the same shape"

    # Check if all predictions are either 0 or 1 (since it's a binary prediction) 
    print(f"Unique values in y_pred: {np.unique(y_pred)}")
