from typing import Optional, Union
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier, HistGradientBoostingRegressor, HistGradientBoostingClassifier

from xgboost import XGBRegressor, XGBClassifier, XGBRFRegressor, XGBRFClassifier
from lightgbm import LGBMClassifier, LGBMRegressor


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
        
        if estimator is None:
            raise ValueError(f"Unknown estimator: {estimator_name}")

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
