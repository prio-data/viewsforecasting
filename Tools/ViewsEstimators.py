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

                    'RFRegressor': RandomForestRegressor(n_estimators=250, n_jobs=-2, random_state=random_state),
                    'RFClassifier': RandomForestClassifier(n_estimators=250, n_jobs=-2, random_state=random_state),

                    'XGBRFRegressor': XGBRFRegressor(n_estimators=100, learning_rate=0.05, random_state=random_state),
                    'XGBRFClassifier': XGBRFClassifier(n_estimators=100, learning_rate=0.05, random_state=random_state),

                    'GBMRegressor': GradientBoostingRegressor(n_estimators=200, random_state=random_state),
                    'GBMClassifier': GradientBoostingClassifier(n_estimators=200, random_state=random_state),

                    'XGBRegressor': XGBRegressor(n_estimators=100, learning_rate=0.05, n_jobs=-2, random_state=random_state),
                    'XGBClassifier': XGBClassifier(n_estimators=100, learning_rate=0.05, n_jobs=-2, random_state=random_state),
                    
                    'HGBRegressor': HistGradientBoostingRegressor(max_iter=200, random_state=random_state),
                    'HGBClassifier': HistGradientBoostingClassifier(max_iter=200, random_state=random_state),
                }
        estimator = estimators.get(estimator_name)

        return estimator

    def fit(self,
            X: Union[np.ndarray, pd.DataFrame],
            y: Union[np.ndarray, pd.Series]):
        """ Fit the model. """
        # Run several sanity checks on the input
        X, y = check_X_y(X, 
                         y, 
                         dtype=None, 
                         accept_sparse=False, 
                         accept_large_sparse=False, 
                         force_all_finite='allow-nan') # allow X and y contain NaNs but not infinities
    
        if len(np.unique(y)) < 2:
            raise ValueError("Input y for classifier must have more than one unique value.")

        # Save n of features in X to make checks later
        self.n_features_in_ = X.shape[1]
        
        # Instantiate the classifier
        self.clf_ = self._resolve_estimator(self.clf_name, random_state=42)

        # If defined, add parameters to the classifier
        if self.clf_params:
            self.clf_.set_params(**self.clf_params)
        
        # Fit the classifier
        self.clf_.fit(X, y > 0)

        # Instantiate the regressor
        self.reg_ = self._resolve_estimator(self.reg_name, random_state=42)
        
        # If defined, add parameters to the regressor
        if self.reg_params:
            self.reg_.set_params(**self.reg_params)

        # Fit the regressor for data where y > 0 only
        self.reg_.fit(X[y > 0], y[y > 0])

        # Set the is_fitted_ flag to True for further sanity checks
        self.is_fitted_ = True

        return self
    
    def predict(self, 
                X: Union[np.ndarray, pd.DataFrame]):
        """ Predict combined response using probabilistic classification outcome """
        # Run several sanity checks on the input
        X = check_array(X, 
                        dtype=None, 
                        accept_sparse=False, 
                        accept_large_sparse=False, 
                        force_all_finite='allow-nan')
        
        check_is_fitted(self, 'is_fitted_')

        if X.shape[1] != self.n_features_in_:
            raise ValueError("Number of features of the model must match the input."
                             f"Model n_features_in_ is {self.n_features_in_}"
                             f"and input n_features is {X.shape[1]}")
        
        # Predict with the classifier - take probability to be in class 1
        clf_predictions_proba = self.clf_.predict_proba(X)[:, 1]

        # Make predictions using the regressor
        reg_predictions = self.reg_.predict(X)

        # The final prediction is the product of the classifier and regressor predictions
        combined_predictions = clf_predictions_proba * reg_predictions
        
        return combined_predictions
    
    def predict_bin(self, 
                X: Union[np.ndarray, pd.DataFrame]):
        """ Predict combined response using binary classification outcome. """
        # Run several sanity checks on the input
        X = check_array(X, 
                        dtype=None, 
                        accept_sparse=False, 
                        accept_large_sparse=False, 
                        force_all_finite='allow-nan')
        
        check_is_fitted(self, 'is_fitted_')

        if X.shape[1] != self.n_features_in_:
            raise ValueError("Number of features of the model must match the input."
                             f"Model n_features_in_ is {self.n_features_in_}" 
                             f"and input n_features is {X.shape[1]}")

        # Predict with the classifier - take classes, 0 or 1
        clf_predictions_bin = self.clf_.predict(X)

        # Predict with the regressor
        reg_predictions = self.reg_.predict(X)

        # Make the final prediction
        combined_predictions = clf_predictions_bin * reg_predictions

        return combined_predictions


def test_hurdle_regression(clf_name:str='logistic', 
                           reg_name:str='linear'):
    """ Validate estimator using sklearn's provided utility and ensure it can fit and predict on fake dataset resembling distribution for hurdle regression."""
    # Create a synthetic dataset that simulates dataset with many zeroes
    X_reg, y_reg = make_regression(n_samples=1000, n_features=20)
    X_clf, y_clf = make_classification(n_samples=1000, n_features=20)
    X = np.hstack([X_clf, X_reg])
    y = y_clf * y_reg

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Instantiate a HurdleRegression object
    hr = HurdleRegression(clf_name=clf_name, reg_name=reg_name)

    # Fit the model to the data
    hr.fit(X_train, y_train)

    # Make predictions with probability of positive class from the classifier
    y_pred = hr.predict(X_test)
    print('Mean Squared Error for combined predictions with positive class probability from the classifier:', int(mean_squared_error(y_test, y_pred)))
    assert y_pred.shape == y_test.shape, "Predictions and y do not have the same shape"

    # Make predictions with binary outcome from the classifier
    y_pred_bin = hr.predict_bin(X_test)
    print('Mean Squared Error or combined predictions with binary outcome from the classifier:', int(mean_squared_error(y_test, y_pred_bin)))
    assert y_pred_bin.shape == y_test.shape, "Probability predictions and y do not have the same shape"


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
