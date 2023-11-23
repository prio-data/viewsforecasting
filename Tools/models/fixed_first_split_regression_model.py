from typing import Optional, Union
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier, HistGradientBoostingRegressor, HistGradientBoostingClassifier

from xgboost import XGBRegressor, XGBClassifier, XGBRFRegressor, XGBRFClassifier
from lightgbm import LGBMClassifier, LGBMRegressor


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


