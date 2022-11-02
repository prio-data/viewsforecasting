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
        nj = 4
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
            'modelname':        'fat_dev_mc_media_baseline_xgbrf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           'ln_ged_sb_dep',
            'data_train':       'media_baseline',
            'queryset':         'fat_dev_mc_media_baseline',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Baseline model with a few conflict history features as well as log population, random forests regression model.',
            'long_description':  'A very simple model with only five data columns (each column representing one feature): The number of fatalities in the same country at $t-1$, three decay functions of time since there was at least five fatalities in a single month, for each of the UCDP conflict types -- state-based, one-sided, or non-state conflict -- and log population size (Hegre2020RP,Pettersson2021JPR).The features in the baseline are included in all the models described below. This ensures that all models in the ensemble provides at least moderately good predictions, while guaranteeing diversity in feature sets and modelling approaches.'
        }
        ModelList.append(model)
        
        model = {
            'modelname':        'fat_dev_mc_media_topics_xgbrf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           'ln_ged_sb_dep',
            'data_train':       'media_topics',
            'queryset':         'fat_dev_mc_media_topics',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Topics model by malika and chandler. data up to July 2022',
            'long_description':  'A simple random forests regression model using topics data. includes topic shares time lagged to account for July update, one year lag from that adjusted value, running average and spatial lag.'
        }
        ModelList.append(model)
        
        model = {
            'modelname':        'fat_dev_mc_media_google_internet_hurdle',
            'algorithm':        hur_regressor,
            'depvar':           'ln_ged_sb_dep',
            'data_train':       'media_google_internet',
            'queryset':         'fat_dev_mc_media_google_internet',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Google and internet model by malika and chandler. data up to August 2022',
            'long_description':  'A hurdle regression model using google and internet data. Includes population data, internet per population appropriately lagged, and google internet indices appropriately lagged for conflict and war themes.'
        }
        ModelList.append(model)
        
        model = {
            'modelname':        'fat_dev_mc_media_all_features_xgbrf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           'ln_ged_sb_dep',
            'data_train':       'media_all_features',
            'queryset':         'fat_dev_mc_media_all_features',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Google and internet model by malika and chandler. data up to August 2022',
            'long_description':  'the everything model.'
        }
        ModelList.append(model)

    else:
        raise Exception(f"Unrecognised level {level}: allowed values are cm only for now")

    for model in ModelList:
        model['predstore_calib'] = level + '_' + model['modelname'] + '_calib'
        model['predstore_test'] = level + '_' + model['modelname'] + '_test'

    return ModelList

