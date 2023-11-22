# The ModelList is a list of dictionaries that define a range of models for the project

import os
from importlib.machinery import SourceFileLoader
import sys
# sys.path.append('../')
sys.path.append('../Tools')
#sys.path.append('../Intermediates')
# sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from sklearn import preprocessing
from sklearn.linear_model import ElasticNet
from sklearn.datasets import make_regression

from xgboost import XGBRegressor
from xgboost import XGBClassifier
from xgboost import XGBRFRegressor, XGBRFClassifier

from lightgbm import LGBMClassifier, LGBMRegressor

from ViewsEstimators import *

class FixedFirstSplitRegression(BaseEstimator):
    """ Regression model which makes the first split according to a specified feature and then splits according to other 
    algorithms. The model optimizes onset-situation predictions by fitting a two-part model and combining predictions:
            1) binary classifier
            2) continuous regression
    Implementeted as a valid sklearn estimator, so it can be used in pipelines and GridSearch objects.
    Args:
        ones_name: model to estimate if z variable is one (e.g. "onset")
        zeros_name: model to estimate if z variable is zeros (e.g. "continuation")
        ones_params: dict of parameters to pass to "ones" sub-model when initialized
        zeros_params: dict of parameters to pass to "zeros" sub-model when initialized
    """

    def __init__(self,
                 ones_name: str = 'RFRegressor',
                 zeros_name: str = 'RFRegressor',
                 ones_indicator: str = '',
                 ones_params: Optional[dict] = None,
                 zeros_params: Optional[dict] = None):

        self.ones_name = ones_name
        self.zeros_name = zeros_name
        self.ones_indicator = ones_indicator
        self.ones_params = ones_params
        self.zeros_params = zeros_params
        self.ones_fi = []
        self.zeros_fi = []

    @staticmethod
    def _resolve_estimator(func_name: str):
        """ Lookup table for supported estimators.
        This is necessary because sklearn estimator default arguments
        must pass equality test, and instantiated sub-estimators are not equal. """

        funcs = {'linear': LinearRegression(),
                 'logistic': LogisticRegression(solver='liblinear'),
                 'LGBMRegressor': LGBMRegressor(n_estimators=250),
                 'LGBMClassifier': LGBMClassifier(n_estimators=250),
                 'RFRegressor': XGBRFRegressor(n_estimators=250,n_jobs=-2),
                 'RFClassifier': XGBRFClassifier(n_estimators=250,n_jobs=-2),
                 'GBMRegressor': GradientBoostingRegressor(n_estimators=200),
                 'GBMClassifier': GradientBoostingClassifier(n_estimators=200),
                 'XGBRegressor': XGBRegressor(n_estimators=100,learning_rate=0.05,n_jobs=-2),
                 'XGBClassifier': XGBClassifier(n_estimators=100,learning_rate=0.05,n_jobs=-2),
                 'HGBRegressor': HistGradientBoostingRegressor(max_iter=200),
                 'HGBClassifier': HistGradientBoostingClassifier(max_iter=200),
                }

        return funcs[func_name]

    def fit(self,
            X: Union[np.ndarray, pd.DataFrame],
            y: Union[np.ndarray, pd.Series],
            z: Union[np.ndarray, pd.Series]):
        X, y = check_X_y(X, y, dtype=None,
                         accept_sparse=False,
                         accept_large_sparse=False,
                         force_all_finite='allow-nan')
        z = X[ones_indicator]

        if X.shape[1] < 2:
            raise ValueError('Cannot fit model when n_features = 1')

        self.ones_ = self._resolve_estimator(self.ones_name)
        if self.ones_params:
            self.ones_.set_params(**self.ones_params)
        self.ones_.fit(X[z==1], y[z==1])
        self.ones_fi = self.ones_.feature_importances_

        self.zeros_ = self._resolve_estimator(self.zeros_name)
        if self.zeros_params:
            self.zeros_.set_params(**self.zeros_params)
        self.zeros_.fit(X[z==0], y[z==0])
        self.zeros_fi = self.zeros_.feature_importances_

        self.is_fitted_ = True
        return self


    def predict(self, X: Union[np.ndarray, pd.DataFrame]):
#    def predict_expected_value(self, X: Union[np.ndarray, pd.DataFrame]):
        """ Predict combined response using probabilistic classification outcome """
        X = check_array(X, accept_sparse=False, accept_large_sparse=False)
        check_is_fitted(self, 'is_fitted_')
#        predict = 
        return self.clf_.predict_proba(X)[:, 1] * self.reg_.predict(X)

def manual_test():
    """ Validate estimator using sklearn's provided utility and ensure it can fit and predict on fake dataset. """
    check_estimator(HurdleRegression)
    from sklearn.datasets import make_regression
    X, y = make_regression()
    reg = FixedFirstSplitRegression()
    reg.fit(X, y)
    reg.predict(X)


def load_model_config(model_name):
    config_path = os.path.join('model_configs', f'{model_name}_config.py')
    model_config = SourceFileLoader('model_config', config_path).load_module()
    return model_config




def DefineEnsembleModels(level):
    ModelList = []

    if level == 'cm':

        
        model1_config = load_model_config('model1')
        model1 = {
            'modelname': model1_config.modelname,
            'algorithm': XGBRFRegressor(n_estimators = model1_config.n_estimators, n_jobs = model1_config.n_jobs),
            'depvar': model1_config.depvar,
            'data_train': model1_config.data_train,
            'queryset': model1_config.queryset,
            'preprocessing': model1_config.preprocessing,
            'level': model1_config.level,
            'description': model1_config.description,
            'long_description': model1_config.long_description,
        }
        ModelList.append(model1)

        model2_config = load_model_config('model2')
        model2 = {
            'modelname': model2_config.modelname,
            'algorithm': XGBRFRegressor(n_estimators = model2_config.n_estimators, learning_rate = model2_config.learning_rate, n_jobs = model2_config.n_jobs),
            'depvar': model2_config.depvar,
            'data_train': model2_config.data_train,
            'queryset': model2_config.queryset,
            'preprocessing': model2_config.preprocessing,
            'level': model2_config.level,
            'description': model2_config.description,
            'long_description': model2_config.long_description,
        }
        ModelList.append(model2)

        model3_config = load_model_config('model3')
        model3 = {
            'modelname': model3_config.modelname,
            'algorithm': HurdleRegression(clf_name=model3_config.clf_name, reg_name=model3_config.reg_name),
            'depvar': model3_config.depvar,
            'data_train': model3_config.data_train,
            'queryset': model3_config.queryset,
            'preprocessing': model3_config.preprocessing,
            'level': model3_config.level,
            'description': model3_config.description,
            'long_description': model3_config.long_description,
        }
        ModelList.append(model3)
        

      

    elif level == 'pgm':

        nj = 12
        n_estimators = 200

        rf_regressor = RandomForestRegressor(n_estimators=n_estimators, n_jobs=nj)

        xgb_regressor = XGBRegressor(n_estimators=n_estimators, tree_method='hist', n_jobs=nj)

        lgbm_regressor = LGBMRegressor(n_estimators=n_estimators)

        clf_params = {'n_estimators': n_estimators, 'n_jobs': nj}

        reg_params = {'n_estimators': n_estimators, 'n_jobs': nj}

        clf_lgbm_params = {'n_estimators': n_estimators}

        reg_lgbm_params = {'n_estimators': n_estimators}

        hur_regressor = HurdleRegression(clf_name='XGBClassifier', reg_name='XGBRegressor', clf_params=clf_params,
                                         reg_params=reg_params)
        hur_lgbm_regressor = HurdleRegression(clf_name='LGBMClassifier', reg_name='LGBMRegressor',
                                              clf_params=clf_lgbm_params, reg_params=reg_lgbm_params)

        model = {
            'modelname': 'fatalities002_pgm_baseline_lgbm',
            'algorithm': lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_baseline',
            'data_train': 'baseline',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_conflictlong_lgbm',
            'algorithm': lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_conflictlong',
            'data_train': 'conflictlong',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_conflictlong_hurdle_lgbm',
            'algorithm': hur_lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_conflictlong',
            'data_train': 'conflictlong',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_escwa_drought_hurdle_lgbm',
            'algorithm': hur_lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_escwa_drought',
            'data_train': 'escwa_drought',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_escwa_drought_lgbm',
            'algorithm': lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_escwa_drought',
            'data_train': 'escwa_drought',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_natsoc_hurdle_lgbm',
            'algorithm': hur_lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_natsoc',
            'data_train': 'natsoc',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_natsoc_lgbm',
            'algorithm': lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_natsoc',
            'data_train': 'natsoc',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_broad_hurdle_lgbm',
            'algorithm': hur_lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_broad',
            'data_train': 'broad',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_broad_lgbm',
            'algorithm': lgbm_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_broad',
            'data_train': 'broad',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_conflict_history_xgb',
            'algorithm': xgb_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_conflict_history',
            'data_train': 'conflicthist',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }

        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_conflict_treelag_hurdle',
            'algorithm': hur_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_conflict_treelag',
            'data_train': 'conflicttreelag',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities002_pgm_conflict_sptime_dist_hurdle',
            'algorithm': hur_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_conflict_sptime_dist',
            'data_train': 'conflictsptime_dist',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }
        ModelList.append(model)
    else:
        raise Exception(f"Unrecognised level {level}: allowed values are cm or pgm")

    for model in ModelList:
        model['predstore_calib'] = level + '_' + model['modelname'] + '_calib'
        model['predstore_test'] = level + '_' + model['modelname'] + '_test'

    return ModelList

