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
        'modelname':        'fatalities002_baseline_rf',
        'algorithm':        XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':           'ln_ged_sb_dep',
        'data_train':       'baseline002',
        'queryset':         'fatalities002_baseline',
        'preprocessing':    'float_it',
        'level':            'cm',
        'description':      'Baseline model with a few conflict history features as well as log population, random forests regression model.',
        'long_description':  'A very simple model with only five data columns (each column representing one feature): The number of fatalities in the same country at $t-1$, three decay functions of time since there was at least five fatalities in a single month, for each of the UCDP conflict types -- state-based, one-sided, or non-state conflict -- and log population size (Hegre2020RP,Pettersson2021JPR).The features in the baseline are included in all the models described below. This ensures that all models in the ensemble provides at least moderately good predictions, while guaranteeing diversity in feature sets and modelling approaches.'
    }
    ModelList.append(model)

    model = {
        'modelname':        'fatalities002_conflicthistory_rf',
        'algorithm':        XGBRFRegressor(n_estimators=250,n_jobs=nj),
        'depvar':           "ln_ged_sb_dep",
        'data_train':       'conflict_ln',
        'queryset':         "fatalities002_conflict_history",
        'preprocessing':    'float_it',
        'level':            'cm',
        'description':      'A collection of variables that together map the conflict history of a country, random forests regression model.' ,
        'long_description': 'A collection of variables that together map the conflict history of a country. The features include lagged dependent variables for each conflict type as coded by the UCDP (state-based, one-sided, or non-state) for up to each of the preceding six months, decay functions of time since conflict caused 5, 100, and 500 deaths in a month, for each type of violence, whether ACLED (https://doi.org/10.1177/0022343310378914 recorded similar violence, and whether there was recent violence in any neighboring countries.'
    }
    ModelList.append(model)

    # Model: GED logged dependent variable, logged conflict history variables, gradient boosting
    model = {
        'modelname':        'fatalities002_conflicthistory_gbm',
        'algorithm':        GradientBoostingRegressor(n_estimators=200), 
        'depvar':           'ln_ged_sb_dep',
        'data_train':       'conflict_ln',
        'queryset':         "fatalities002_conflict_history",
        'preprocessing':    'float_it',
        'level':            'cm',
        'description':      'A collection of variables that together map the conflict history of a country, scikit gradient boosting regression model.', 
        'long_description': ''
    }
    ModelList.append(model)       
        

    model = {
        'modelname': 'fatalities002_conflicthistory_hurdle_lgb',
        'algorithm': HurdleRegression(clf_name = 'LGBMClassifier', reg_name = 'LGBMRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'conflict_ln',
        'queryset': "fatalities002_conflict_history",
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname': 'fatalities002_conflicthistory_long_xgb',
        'algorithm': XGBRegressor(n_estimators=100,learning_rate=0.05,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'conflictlong_ln',
        'queryset': "fatalities002_conflict_history_long",
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname':  'fatalities002_vdem_hurdle_xgb',
        'algorithm': HurdleRegression(clf_name = 'XGBClassifier', reg_name = 'XGBRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'vdem_short',
        'queryset':  "fatalities002_vdem_short",
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname':  'fatalities002_wdi_rf',
        'algorithm': XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'wdi_short',
        'queryset':  "fatalities002_wdi_short",
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname':  'fatalities002_topics_rf',
        'algorithm': XGBRFRegressor(n_estimators=250,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'topics_002',
        'queryset':   "fatalities002_topics",
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname':  'fatalities002_topics_xgb',
        'algorithm': XGBRegressor(n_estimators=80,learning_rate=0.05,n_jobs=nj),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'topics_002',
        'queryset':   "fatalities002_topics",
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)
    model = {
        'modelname':  'fatalities002_topics_hurdle_lgb',
        'algorithm': HurdleRegression(clf_name = 'LGBMClassifier', reg_name = 'LGBMRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'topics_002',
        'queryset':   "fatalities002_topics",
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)


    model = {
        'modelname':  'fatalities002_joint_broad_rf',
        'algorithm': XGBRFRegressor(n_estimators=250,n_jobs=nj),
        'depvar':     "ln_ged_sb_dep",
        'data_train':    'joint_broad',
        'queryset':   'fatalities002_joint_broad',
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname': 'fatalities002_joint_broad_hurdle_rf',
        'algorithm': HurdleRegression(clf_name = 'RFClassifier', reg_name = 'RFRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'joint_broad',
        'queryset': 'fatalities002_joint_broad',
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname':  'fatalities002_joint_narrow_xgb',
        'algorithm':  XGBRFRegressor(n_estimators=250,n_jobs=nj),
        'depvar':     "ln_ged_sb_dep",
        'data_train':    'joint_narrow',
        'queryset':   'fatalities002_joint_narrow',
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname': 'fatalities002_joint_narrow_hurdle_xgb',
        'algorithm': HurdleRegression(clf_name = 'XGBClassifier', reg_name = 'XGBRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'joint_narrow',
        'queryset': 'fatalities002_joint_narrow',
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)


    model = {
        'modelname': 'fatalities002_joint_narrow_hurdle_lgb',
        'algorithm': HurdleRegression(clf_name = 'LGBMClassifier', reg_name = 'LGBMRegressor'),
        'depvar': "ln_ged_sb_dep",
        'data_train':    'joint_narrow',
        'queryset': 'fatalities002_joint_narrow',
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)


    # PCA models: need to implement a PCA preprocessing function first.
    model = {
        'modelname':      'fatalities002_all_pca3_xgb',
        'algorithm':      XGBRegressor(n_estimators=100,learning_rate=0.05,n_jobs=nj),
        'depvar':         "ln_ged_sb_dep",
        'data_train':     'pca_all',
        'queryset':      'fatalities002_all_features',
        'preprocessing': 'pca_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)


    model = {
        'modelname':     'fatalities002_aquastat_rf',
        'algorithm':     XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':        "ln_ged_sb_dep",
        'data_train':    'aquastat',
        'queryset':      'fatalities002_aquastat',
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname':     'fatalities002_faostat_rf',
        'algorithm':     XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':        "ln_ged_sb_dep",
        'data_train':    'faostat',
        'queryset':      'Fatalities002_faostat',
        'preprocessing': 'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description':      ''
    }
    ModelList.append(model)

    model = {
        'modelname':        'fatalities002_faoprices_rf',
        'algorithm':        XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':           'ln_ged_sb_dep',
        'data_train':       'faoprices',
        'queryset':         'Fatalities002_faoprices',
        'preprocessing':    'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description': ''
    }
    ModelList.append(model)

    model = {
        'modelname':        'fatalities002_imfweo_rf',
        'algorithm':        XGBRFRegressor(n_estimators=300,n_jobs=nj),
        'depvar':           "ln_ged_sb_dep",
        'data_train':       'imfweo',
        'queryset':         'Fatalities001_imfweo',
        'preprocessing':    'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description': ''
    }
    ModelList.append(model)

    model = {
        'modelname':        'fat_hh20_Markov_glm',
        'algorithm':        'Rscript',
        'depvar':           "ln_ged_sb_dep",
        'data_train':       'hh20',
        'queryset':         'hh_20_features',
        'preprocessing':    'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description': ''
    }
    ModelList.append(model)

    model = {
        'modelname':        'fat_hh20_Markov_rf',
        'algorithm':        'Rscript',
        'depvar':           "ln_ged_sb_dep",
        'data_train':       'hh20',
        'queryset':         'hh_20_features',
        'preprocessing':    'float_it',
        'level':            'cm',
        'description':      '', 
        'long_description': ''
    }
    ModelList.append(model)

    for model in ModelList:
        model['predstore_calib'] = level +  '_' + model['modelname'] + '_calib'
        model['predstore_test'] = level +  '_' + model['modelname'] + '_test'   

    return(ModelList)

