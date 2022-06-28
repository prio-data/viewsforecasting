# The ModelList is a list of dictionaries that define a range of models for the project

import sys
sys.path.append('../')
sys.path.append('../Tools')
sys.path.append('../Intermediates')
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


def DefineEnsembleModels(level):
    ModelList = []
    nj=12

    model = {
        'modelname':     'fatalities002_baseline_rf',
        'algorithm':     XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':        "ln_ged_sb_dep",
        'data_train':    'baseline002',
        'queryset':      'fatalities002_baseline',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname': 'fat_conflicthistory_rf',
        'algorithm': XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'conflict_ln',
        'queryset': "fat_cm_conflict_history",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    # Model: GED logged dependent variable, logged conflict history variables, gradient boosting
    model = {
        'modelname': 'fat_conflicthistory_gbm',
        'algorithm': GradientBoostingRegressor(), 
        'depvar': "ln_ged_sb_dep",
        'data_train':    'conflict_ln',
        'queryset': "fat_cm_conflict_history",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)       
        

    model = {
        'modelname': 'fat_conflicthistory_hurdle_lgb',
        'algorithm': HurdleRegression(clf_name = 'LGBMClassifier', reg_name = 'LGBMRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'conflict_ln',
        'queryset': "fat_cm_conflict_history",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname': 'fat_conflicthistory_long_xgb',
        'algorithm': XGBRegressor(n_estimators=100,learning_rate=0.05,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'conflictlong_ln',
        'queryset': "hh_fatalities_ged_acled_ln",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':  'fat_vdem_hurdle_xgb',
        'algorithm': HurdleRegression(clf_name = 'XGBClassifier', reg_name = 'XGBRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'vdem_short',
        'queryset':  "hh_fatalities_vdem_short",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':  'fat_wdi_rf',
        'algorithm': XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'wdi_short',
        'queryset':  "hh_fatalities_wdi_short",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':  'fatalities002_topics_rf',
        'algorithm': XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'topics_002',
        'queryset':   "fatalities002_topics",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':  'fat_topics_rf',
        'algorithm': XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'topics_short',
        'queryset':   "hh_topic_model_short",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':  'fatalities002_topics_hurdle_lgb',
        'algorithm': HurdleRegression(clf_name = 'LGBMClassifier', reg_name = 'LGBMRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'topics_002',
        'queryset':   "fatalities002_topics",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':  'fat_topics_histgbm',
        'algorithm': HistGradientBoostingRegressor(max_iter=200),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'topics_short',
        'queryset':   "hh_topic_model_short",
        'preprocessing': 'float_it',
    }
    ModelList.append(model)


    model = {
        'modelname':  'fat_broad_xgb',
        'algorithm':  XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':     "ln_ged_sb_dep",
        'data_train':    'broad',
        'queryset':   'hh_broad',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)


    model = {
        'modelname':  'fatalities002_greatest_hits_hurdle_rf',
        'algorithm':  HurdleRegression(clf_name = 'RFClassifier', reg_name = 'RFRegressor'),
        'depvar':     "ln_ged_sb_dep",
        'data_train':    'gh',
        'queryset':   'fatalities002_greatest_hits',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname': 'fat_hh20_hurdle_rf',
        'algorithm': HurdleRegression(clf_name = 'RFClassifier', reg_name = 'RFRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'hh20',
        'queryset': 'hh_20_features',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname': 'fat_hh20_hurdle_xgb',
        'algorithm': HurdleRegression(clf_name = 'XGBClassifier', reg_name = 'XGBRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'hh20',
        'queryset': 'hh_20_features',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)


    model = {
        'modelname': 'fat_hh20_hurdle_lgb',
        'algorithm': HurdleRegression(clf_name = 'LGBMClassifier', reg_name = 'LGBMRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'hh20',
        'queryset': 'hh_20_features',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)


    # PCA models: need to implement a PCA preprocessing function first.
    model = {
        'modelname':      'fat_all_pca3_xgb',
        'algorithm':      XGBRegressor(n_estimators=100,learning_rate=0.05,n_jobs=nj),
        'depvar':         "ln_ged_sb_dep",
        'data_train':     'pca_all',
        'queryset':      'hh_all_features',
        'preprocessing': 'pca_it',
    }
    ModelList.append(model)


    model = {
        'modelname':     'fatalities002_aquastat_rf',
        'algorithm':     XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':        "ln_ged_sb_dep",
        'data_train':    'aquastat',
        'queryset':      'Fatalities002_aquastat',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':     'fatalities002_faostat_rf',
        'algorithm':     XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':        "ln_ged_sb_dep",
        'data_train':    'faostat',
        'queryset':      'Fatalities002_faostat',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':     'fatalities002_faoprices_rf',
        'algorithm':     XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':        "ln_ged_sb_dep",
        'data_train':    'faoprices',
        'queryset':      'Fatalities002_faoprices',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':     'fatalities002_imfweo_rf',
        'algorithm':     XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':        "ln_ged_sb_dep",
        'data_train':    'imfweo',
        'queryset':      'Fatalities001_imfweo',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':   'fat_hh20_Markov_glm',
        'algorithm': 'Rscript',
        'depvar': "ln_ged_sb_dep",
        'data_train':      'hh20',
        'queryset': 'hh_20_features',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    model = {
        'modelname':   'fat_hh20_Markov_rf',
        'algorithm': 'Rscript',
        'depvar': "ln_ged_sb_dep",
        'data_train':      'hh20',
        'queryset': 'hh_20_features',
        'preprocessing': 'float_it',
    }
    ModelList.append(model)

    for model in ModelList:
        model['predstore_calib'] = level +  '_' + model['modelname'] + '_calib'
        model['predstore_test'] = level +  '_' + model['modelname'] + '_test'   

    return(ModelList)

