# The ModelList is a list of dictionaries that define a range of models for the project

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
    




def DefineEnsembleModels(level):
    ModelList = []

    if level == 'cm':
        nj = 12

#        model = {
#            'modelname':        'fatalities003_baseline_ons',
#            'algorithm':        FixedFirstSplitRegression(ones_name='LGBMClassifier', zeros_name='LGBMRegressor',onset_indicator = ''),
#            'depvar':           'ln_ged_sb_dep',
#            'data_train':       'baseline002',
#            'queryset':         'fatalities002_baseline',
#            'preprocessing':    'float_it',
#            'level':            'cm',
#            'description':      'Baseline model with a few conflict history features as well as log population, random forests regression model.',
#            'long_description':  'A very simple model with only five data columns (each column representing one feature): The number of fatalities in the same country at $t-1$, three decay functions of time since there was at least five fatalities in a single month, for each of the UCDP conflict types -- state-based, one-sided, or non-state conflict -- and log population size (Hegre2020RP,Pettersson2021JPR).The features in the baseline are included in all the models described below. This ensures that all models in the ensemble provides at least moderately good predictions, while guaranteeing diversity in feature sets and modelling approaches.'
#        }
#        ModelList.append(model)
        
        model = {
            'modelname':        'fatalities003_nl_baseline_rf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'baseline003',
            'queryset':         'fatalities003_baseline',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Baseline model with a few conflict history features as well as log population, random forests regression model.',
            'long_description':  'A very simple model with only five data columns (each column representing one feature): The number of fatalities in the same country at $t-1$, three decay functions of time since there was at least five fatalities in a single month, for each of the UCDP conflict types -- state-based, one-sided, or non-state conflict -- and log population size (Hegre2020RP,Pettersson2021JPR).The features in the baseline are included in all the models described below. This ensures that all models in the ensemble provides at least moderately good predictions, while guaranteeing diversity in feature sets and modelling approaches.'
        }
        ModelList.append(model)

        model = {
            'modelname':        'fatalities003_nl_conflicthistory_rf',
            'algorithm':        XGBRFRegressor(n_estimators=250, n_jobs=nj),
            'depvar':           "ged_sb_dep",
            'data_train':       'conflict_ln',
            'queryset':         "fatalities003_conflict_history",
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'A collection of variables that together map the conflict history of a country, random forests regression model.' ,
            'long_description': 'A collection of variables that together map the conflict history of a country. The features include lagged dependent variables for each conflict type as coded by the UCDP (state-based, one-sided, or non-state) for up to each of the preceding six months, decay functions of time since conflict caused 5, 100, and 500 deaths in a month, for each type of violence, whether ACLED (https://doi.org/10.1177/0022343310378914 recorded similar violence, and whether there was recent violence in any neighboring countries.'
        }
        ModelList.append(model)
        

        # Model: GED logged dependent variable, logged conflict history variables, gradient boosting
        model = {
            'modelname':        'fatalities003_nl_conflicthistory_gbm',
            'algorithm':        GradientBoostingRegressor(n_estimators=200),
            'depvar':           'ged_sb_dep',
            'data_train':       'conflict_ln',
            'queryset':         "fatalities003_conflict_history",
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'A collection of variables that together map the conflict history of a country, scikit gradient boosting regression model.',
            'long_description': ''
        }
        #ModelList.append(model)

        model = {
            'modelname': 'fatalities003_nl_conflicthistory_hurdle_lgb',
            'algorithm': HurdleRegression(clf_name='LGBMClassifier', reg_name='LGBMRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'conflict_ln',
            'queryset': "fatalities003_conflict_history",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities003_nl_conflicthistory_long_xgb',
            'algorithm': XGBRegressor(n_estimators=100, learning_rate=0.05, n_jobs=nj),
            'depvar': "ged_sb_dep",
            'data_train':    'conflictlong_ln',
            'queryset': "fatalities003_conflict_history_long",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)
        
        
        
        model = {
            'modelname':        'fatalities003_nl_conflicthistory_nonlog_hurdle_lgb',
            'algorithm': HurdleRegression(clf_name='LGBMClassifier', reg_name='LGBMRegressor'),
            'depvar':           "ged_sb_dep",
            'data_train':       'conflict_nonlog',
            'queryset':         "fatalities003_conflict_history_nonlog",
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'A collection of variables that together map the conflict history of a country, random forests regression model.' ,
            'long_description': 'A collection of variables that together map the conflict history of a country. The features include lagged dependent variables for each conflict type as coded by the UCDP (state-based, one-sided, or non-state) for up to each of the preceding six months, decay functions of time since conflict caused 5, 100, and 500 deaths in a month, for each type of violence, whether ACLED (https://doi.org/10.1177/0022343310378914 recorded similar violence, and whether there was recent violence in any neighboring countries.'
        }
        #ModelList.append(model)

        model = {
            'modelname':  'fatalities003_nl_vdem_hurdle_xgb',
            'algorithm': HurdleRegression(clf_name='XGBClassifier', reg_name='XGBRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'vdem_short',
            'queryset':  "fatalities003_vdem_short",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname':  'fatalities003_nl_wdi_rf',
            'algorithm': XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar': "ged_sb_dep",
            'data_train':    'wdi_short',
            'queryset':  "fatalities003_wdi_short",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname':  'fatalities003_nl_topics_rf',
            'algorithm': XGBRFRegressor(n_estimators=250, n_jobs=nj),
            'depvar': "ged_sb_dep",
            'data_train':    'topics_003',
            'queryset':   "fatalities003_topics",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname':  'fatalities003_nl_topics_xgb',
            'algorithm': XGBRegressor(n_estimators=80, learning_rate=0.05, n_jobs=nj),
            'depvar': "ged_sb_dep",
            'data_train':    'topics_003',
            'queryset':   "fatalities003_topics",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)
        model = {
            'modelname':  'fatalities003_nl_topics_hurdle_lgb',
            'algorithm': HurdleRegression(clf_name='LGBMClassifier', reg_name='LGBMRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'topics_003',
            'queryset':   "fatalities003_topics",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname':  'fatalities003_nl_joint_broad_rf',
            'algorithm': XGBRFRegressor(n_estimators=250, n_jobs=nj),
            'depvar':     "ged_sb_dep",
            'data_train':    'joint_broad',
            'queryset':   'fatalities003_joint_broad',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities003_nl_joint_broad_hurdle_rf',
            'algorithm': HurdleRegression(clf_name='RFClassifier', reg_name='RFRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'joint_broad',
            'queryset': 'fatalities003_joint_broad',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)
        
        model = {
            'modelname':  'fatalities003_joint_narrow_xgb',
            'algorithm':  XGBRFRegressor(n_estimators=250, n_jobs=nj),
            'depvar':     "ged_sb_dep",
            'data_train':    'joint_narrow',
            'queryset':   'fatalities003_joint_narrow',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities003_nl_joint_narrow_hurdle_xgb',
            'algorithm': HurdleRegression(clf_name='XGBClassifier', reg_name='XGBRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'joint_narrow',
            'queryset': 'fatalities003_joint_narrow',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname': 'fatalities003_nl_joint_narrow_hurdle_lgb',
            'algorithm': HurdleRegression(clf_name='LGBMClassifier', reg_name='LGBMRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'joint_narrow',
            'queryset': 'fatalities003_joint_narrow',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        # PCA models: need to implement a PCA preprocessing function first.
        model = {
            'modelname':      'fatalities003_nl_all_pca3_xgb',
            'algorithm':      XGBRegressor(n_estimators=100, learning_rate=0.05, n_jobs=nj),
            'depvar':         "ged_sb_dep",
            'data_train':     'all_features',
            'queryset':      'fatalities003_all_features',
            'preprocessing': 'pca_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        ModelList.append(model)

        model = {
            'modelname':     'fatalities003_nl_aquastat_rf',
            'algorithm':     XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':        "ged_sb_dep",
            'data_train':    'aquastat',
            'queryset':      'fatalities003_aquastat',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        #ModelList.append(model)

        model = {
            'modelname':     'fatalities003_nl_faostat_rf',
            'algorithm':     XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':        "ged_sb_dep",
            'data_train':    'faostat',
            'queryset':      'fatalities003_faostat',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
        #ModelList.append(model)

        model = {
            'modelname':        'fatalities003_faoprices_rf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           'ln_ged_sb_dep',
            'data_train':       'faoprices',
            'queryset':         'fatalities003_faoprices',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      '',
            'long_description': ''
        }
        #ModelList.append(model)

        model = {
            'modelname':        'fatalities003_imfweo_rf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           "ln_ged_sb_dep",
            'data_train':       'imfweo',
            'queryset':         'fatalities003_imfweo',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      '',
            'long_description': ''
        }
        #ModelList.append(model)

        model = {
            'modelname':        'fat_hh20_Markov_glm',
            'algorithm':        'Rscript',
            'depvar':           "ln_ged_sb_dep",
            'data_train':       'joint_narrow',
            'queryset':         'fatalities003_joint_narrow',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      '',
            'long_description': ''
        }
        #ModelList.append(model)

        model = {
            'modelname':        'fat_hh20_Markov_rf',
            'algorithm':        'Rscript',
            'depvar':           "ln_ged_sb_dep",
            'data_train':       'joint_narrow',
            'queryset':         'fatalities003_joint_narrow',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      '',
            'long_description': ''
        }
        #ModelList.append(model)

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

