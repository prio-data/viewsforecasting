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


def DefineEnsembleModels(level):
    ModelList = []

    if level == 'cm':
        nj = 12

        model = {
            'modelname':        'escwa001_cflong',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'cflong001',
            'queryset':         'escwa001_cflong',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Long conflict history model',
            'long_description':  '''...'''
        }
        ModelList.append(model)
        model = {
            'modelname':        'escwa001_vdem',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'vdem001',
            'queryset':         'escwa001_vdem',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Varieties of democracy model',
            'long_description':  '''...'''
        }
        ModelList.append(model)
        model = {
            'modelname':        'escwa001_wdi',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'wdi001',
            'queryset':         'escwa001_wdi',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'World development index model',
            'long_description':  '''...'''
        }
        ModelList.append(model)
        model = {
            'modelname':        'escwa001_aquastat',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'aquastat001',
            'queryset':         'escwa001_aquastat',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Aqua Stat model',
            'long_description':  '''...'''
        }
        ModelList.append(model)
        model = {
            'modelname':        'escwa001_food',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'food001',
            'queryset':         'escwa001_food',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Food security model',
            'long_description':  '''...'''
        }
        ModelList.append(model)
        model = {
            'modelname':        'escwa001_imfweo',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'imfweo001',
            'queryset':         'escwa001_imfweo',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'IMF WEO model',
            'long_description':  '''...'''
        }
        ModelList.append(model)
        model = {
            'modelname':        'escwa001_faostat',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'faostat001',
            'queryset':         'escwa001_faostat',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Faostat model',
            'long_description':  '''...'''
        }
        ModelList.append(model)
        model = {
            'modelname':        'escwa001_broad',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'escwabroad001',
            'queryset':         'escwa001_broad',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Broad escwa model',
            'long_description':  '''...'''
        }
        ModelList.append(model)
        model = {
            'modelname':        'escwa001_onset',
            'algorithm':         RandomForestClassifier(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_onset24',
            'data_train':       'escwaonset001',
            'queryset':         'escwa001_onset',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Broad escwa onset model',
            'long_description':  '''...'''
        }
        ModelList.append(model)

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

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
            'long_description':      ''''''

        }
        ModelList.append(model)
    else:
        raise Exception(f"Unrecognised level {level}: allowed values are cm or pgm")

    for model in ModelList:
        model['predstore_calib'] = level + '_' + model['modelname'] + '_calib'
        model['predstore_test'] = level + '_' + model['modelname'] + '_test'

    return ModelList

