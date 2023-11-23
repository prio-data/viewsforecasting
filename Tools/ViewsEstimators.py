from typing import Optional, Union
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.base import BaseEstimator
from sklearn.utils.estimator_checks import check_estimator
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier, HistGradientBoostingRegressor, HistGradientBoostingClassifier
from sklearn.datasets import make_regression, make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.dummy import DummyClassifier

from xgboost import XGBRegressor, XGBClassifier, XGBRFRegressor, XGBRFClassifier
from lightgbm import LGBMClassifier, LGBMRegressor


####################
# HurdleRegression #
####################
class HurdleRegression(BaseEstimator):
    """ Regression model which handles excessive zeros by fitting a two-part model and combining predictions:
            1) binary classifier
            2) continuous regression
    Implementeted as a valid sklearn estimator, so it can be used in pipelines and GridSearch objects.
    Args:
        clf_name: name of a classifier sub-model to use
        reg_name: name of a regression sub-model to use
        clf_params: dict of parameters to pass to classifier sub-model when initialized
        reg_params: dict of parameters to pass to regression sub-model when initialized
    """
    # Define the constructor method for the class
    def __init__(self,
                 clf_name: str = 'logistic',
                 reg_name: str = 'linear',
                 clf_params: Optional[dict] = None,
                 reg_params: Optional[dict] = None):
        
        self.clf_name = clf_name
        self.reg_name = reg_name
        self.clf_params = clf_params
        self.reg_params = reg_params
        
    @staticmethod
    def _resolve_estimator(estimator_name: str, random_state=None):
        """ Lookup table for supported estimators.
        This is necessary because sklearn estimator default arguments
        must pass equality test, and instantiated sub-estimators are not equal. """

        estimators = {
                    'linear': LinearRegression(),
                    'logistic': LogisticRegression(solver='liblinear', random_state=random_state),

                    'LGBMRegressor': LGBMRegressor(n_estimators=250, random_state=random_state),
                    'LGBMClassifier': LGBMClassifier(n_estimators=250, random_state=random_state),

                    'RFRegressor': RandomForestRegressor(n_estimators=250, random_state=random_state),
                    'RFClassifier': RandomForestClassifier(n_estimators=250, random_state=random_state),

                    'XGBRFRegressor': XGBRFRegressor(n_estimators=100, learning_rate=0.05, random_state=random_state),
                    'XGBRFClassifier': XGBRFClassifier(n_estimators=100, learning_rate=0.05, random_state=random_state),

                    'GBMRegressor': GradientBoostingRegressor(n_estimators=200, random_state=random_state),
                    'GBMClassifier': GradientBoostingClassifier(n_estimators=200, random_state=random_state),

                    'XGBRegressor': XGBRegressor(n_estimators=100, learning_rate=0.05, random_state=random_state),
                    'XGBClassifier': XGBClassifier(n_estimators=100, learning_rate=0.05, random_state=random_state),
                    
                    'HGBRegressor': HistGradientBoostingRegressor(max_iter=200, random_state=random_state),
                    'HGBClassifier': HistGradientBoostingClassifier(max_iter=200, random_state=random_state),
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

        if X.shape[1] == 1:
            raise ValueError('Cannot fit model when n_features = 1')

        # Instantiate the classifier
        self.clf_ = self._resolve_estimator(self.clf_name, random_state=42)
        if self.clf_params:
            self.clf_.set_params(**self.clf_params)
        
        # Check if there are more than one unique values in y 
        # and if yes, fit the classifier to X, so y that is > 0, becomes 1
        # and if not, it is 0
        if len(np.unique(y)) > 1:
            self.clf_.fit(X, y > 0)
        else:
            # Handle the case where y has only one unique value
            self.clf_ = DummyClassifier(strategy='most_frequent')
            self.clf_.fit(X, y > 0)


        # Instantiate the regressor
        self.reg_ = self._resolve_estimator(self.reg_name, random_state=42)
        if self.reg_params:
            self.reg_.set_params(**self.reg_params)
    
        # Fit the regressor to the subset of the data where y > 0
        self.reg_.fit(X[y > 0], y[y > 0])

        self.is_fitted_ = True
        return self
    
    def predict(self, 
                X: Union[np.ndarray, pd.DataFrame]):
        """ Predict combined response using binary classification outcome """
        X = check_array(X, accept_sparse=False, accept_large_sparse=False)
        
        check_is_fitted(self, 'is_fitted_')

        if X.shape[1] != self.n_features_in_:
            raise ValueError(f"Number of features of the model must match the input. Model n_features_in_ is {self.n_features_in_} and input n_features is {X.shape[1]}")

        # Make predictions using the classifier
        clf_predictions = self.clf_.predict(X)

        # Make predictions using the regressor
        reg_predictions = self.reg_.predict(X)

        # The final prediction is the product of the classifier and regressor predictions
        combined_predictions = clf_predictions * reg_predictions

        return combined_predictions
    
    def predict_expected_value(self, X: Union[np.ndarray, pd.DataFrame]):
        """ Predict combined response using probabilistic classification outcome """
        X = check_array(X, accept_sparse=False, accept_large_sparse=False)
        
        check_is_fitted(self, 'is_fitted_')
        
        if X.shape[1] != self.n_features_in_:
            raise ValueError(f"Number of features of the model must match the input. Model n_features_in_ is {self.n_features_in_} and input n_features is {X.shape[1]}")

        # Make predictions using the classifier, take probbailities of being in class 1 ("positive" class)
        clf_prob_predictions = self.clf_.predict_proba(X)[:, 1]

        # Make predictions using the regressor
        reg_predictions = self.reg_.predict(X)

        # The final prediction is the product of the classifier and regressor predictions
        combined_predictions = clf_prob_predictions * reg_predictions
        
        return combined_predictions


def test_hurdle_regression(clf_name:str='logistic', reg_name:str='linear'):
    """ Validate estimator using sklearn's provided utility and ensure it can fit and predict on fake dataset. """

    # Create a synthetic regression dataset
    X_reg, y_reg = make_regression(n_samples=1000, n_features=20, n_informative=2)

    # Create a synthetic classification dataset
    X_clf, y_clf = make_classification(n_samples=1000, n_features=20, n_informative=2, n_redundant=10)

    # Combine the two datasets
    X = np.hstack([X_clf, X_reg])
    y = y_clf * y_reg

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

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

    # Make predictions
    y_pred_prob = hr.predict_expected_value(X_test)

    # Evaluate the model
    print('Mean Squared Error:', mean_squared_error(y_test, y_pred_prob))

    # Check if predictions have the same shape as y
    print(f"Shape of y_pred_prob: {y_pred_prob.shape}")
    print(f"Shape of y_test: {y_test.shape}")

    assert y_pred_prob.shape == y_test.shape, "Probability predictions and y do not have the same shape"


############ WIP ############
# FixedFirstSplitRegression #
############ WIP ############
class FixedFirstSplitRegression(BaseEstimator):
    def __init__(self,
                 ones_model_name: str = 'RFRegressor',
                 zeros_model_name: str = 'RFRegressor',
                 ones_model_params: Optional[dict] = None,
                 zeros_model_params: Optional[dict] = None,
                 split_by: str = ''):
        
        self.ones_model_name = ones_model_name
        self.zeros_model_name = zeros_model_name
        self.ones_model_params = ones_model_params
        self.zeros_model_params = zeros_model_params
        self.split_by = split_by

        self.ones_ = None
        self.zeros_ = None

    @staticmethod
    def _resolve_estimator(estimator_name: str):
        funcs = {
            'linear': LinearRegression(),
            'logistic': LogisticRegression(solver='liblinear'),

            'LGBMRegressor': LGBMRegressor(n_estimators=250),
            'LGBMClassifier': LGBMClassifier(n_estimators=250),

            'RFRegressor': RandomForestRegressor(n_estimators=250),
            'RFClassifier': RandomForestClassifier(n_estimators=250),

            'GBMRegressor': GradientBoostingRegressor(n_estimators=200),
            'GBMClassifier': GradientBoostingClassifier(n_estimators=200),

            'XGBRegressor': XGBRegressor(n_estimators=100, learning_rate=0.05),
            'XGBClassifier': XGBClassifier(n_estimators=100, learning_rate=0.05),

            'HGBRegressor': HistGradientBoostingRegressor(max_iter=200),
            'HGBClassifier': HistGradientBoostingClassifier(max_iter=200),
        }

        return funcs[estimator_name]

    def fit(self, 
            X: Union[np.ndarray, pd.DataFrame], 
            y: Union[np.ndarray, pd.Series],
            ):
    
        """ Fit the model based on the indicator values. """
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)
        if self.split_by not in X.columns:
            raise ValueError(f"split_by column '{self.split_by}' not found in X")

        split_indicator = X[self.split_by].astype(int)
        X = X.drop(columns=[self.split_by])
        X, y = check_X_y(X, y, accept_sparse=False, force_all_finite='allow-nan', dtype=np.float64)

        self.ones_ = self._resolve_estimator(self.ones_model_name)
        if self.ones_model_params:
            self.ones_.set_params(**self.ones_model_params)
        self.ones_.fit(X[split_indicator == 1], y[split_indicator == 1])

        self.zeros_ = self._resolve_estimator(self.zeros_model_name)
        if self.zeros_model_params:
            self.zeros_.set_params(**self.zeros_model_params)
        self.zeros_.fit(X[split_indicator == 0], y[split_indicator == 0])

        self.is_fitted_ = True
        return self

    def predict(self, X: Union[np.ndarray, pd.DataFrame]):
        """ Predict the response based on the split_by indicator values. """
        if isinstance(X, np.ndarray):
            X = pd.DataFrame(X)

        check_is_fitted(self, 'is_fitted_')

        if self.split_by not in X:
            raise ValueError(f"split_by column '{self.split_by}' not found in X")

        split_indicator = X[self.split_by].astype(int)
        X = X.drop(columns=[self.split_by])

        pred_ones = self.ones_.predict(X[split_indicator == 1])
        pred_zeros = self.zeros_.predict(X[split_indicator == 0])

        pred = np.zeros(X.shape[0])
        pred[split_indicator == 1] = pred_ones
        pred[split_indicator == 0] = pred_zeros

      # Create a DataFrame with predictions and split_by values
        result = pd.DataFrame({
            'prediction': pred,
            'split_by': split_indicator
        })

        return result

def test_fixed_first_split_regression(zeros_model_name:str='linear', 
                                      ones_model_name:str='linear', 
                                      split_by = "split_by"):
    """ Validate estimator using sklearn's provided utility and ensure it can fit and predict on fake dataset. """
    # Create a regression dataset
    X, y = make_classification(n_samples=100, n_features=20)

    # Convert to DataFrame and add a 'split_by' column
    X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(X.shape[1])])
    X['split_by'] = np.random.randint(0, 2, len(y))  # Random 0s and 1s for the indicator

    # Initialize and fit the FixedFirstSplitRegression model
    reg = FixedFirstSplitRegression(zeros_model_name=zeros_model_name, 
                                    ones_model_name=ones_model_name, 
                                    split_by=split_by)

    reg.fit(X, y)

    # Make predictions
    result = reg.predict(X)
    print("Predictions:", result)
