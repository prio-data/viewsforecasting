#!/usr/bin/env python
# coding: utf-8

# # ViEWS 3 ensembles: surrogate models, future predictions
# Fatalities project, cm level

# In[1]:


# Basics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
# sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
# Views 3
from viewser.operations import fetch
from viewser import Queryset, Column
import views_runs
from views_partitioning import data_partitioner, legacy
from stepshift import views
import views_dataviz
from views_runs import storage, ModelMetadata
from views_runs.storage import store, retrieve, fetch_metadata
from views_forecasts.extensions import *

# Mapper
import geopandas as gpd

from views_dataviz.map import mapper, utils
from views_dataviz import color
from views_dataviz.map.presets import ViewsMap

import sqlalchemy as sa
from ingester3.config import source_db_path

import sqlalchemy as sa
from ingester3.config import source_db_path

# Other packages
import pickle as pkl

#Parallelization
from joblib import Parallel, delayed, cpu_count
from functools import partial
from genetic2 import *

from pathlib import Path

def TrainSurrogateModels(data_df, Ensemble_df, EndOfHistory, SurrogateModelSteps, NumberOfMonths, Plotpath):
    ''' Trains surrogate models.... '''
#    print('In TrainSurrogateModels')

    # Expand the predictions dataset with predictors that are lagged appropriately

    monthrange = [*(range((EndOfHistory + 1),(EndOfHistory + 1 + NumberOfMonths)))]
    for step in SurrogateModelSteps:
        # Columns to use in surrogate models, with name in predictions dataset (item 0) and in source dataset (item 1)
        colnames = [
            ['libdem_s_' + str(step),'vdem_v2x_libdem'],
            ['rule_s_' + str(step),'vdem_v2x_rule'],
            ['depvar_s_' + str(step),'ln_ged_sb_dep'],
            ['pop_s_' + str(step),'wdi_sp_pop_totl'],
            ['imr_s_' + str(step),'wdi_sp_dyn_imrt_in'],
            ['nb_conflict_s_' + str(step),'splag_1_decay_ged_sb_5'],
            ['topic_conflict_s_' + str(step),'topic10_conflict_t1'],
            ['topic_conflict_stock_s_' + str(step),'topic10_conflict_t1_stock'],
            ['water_efficiency_s_' + str(step),'general_efficiency_t48'],
        ]
        for col in colnames:
            Ensemble_df[col[0]] = np.nan
            # Reverse stepshifting:
            for m in monthrange:
                Ensemble_df.loc[m, col[0]] = np.array(data_df[col[1]].loc[m-step])




    # Surrogate models
    from pygam import LogisticGAM, LinearGAM, s, te
    from mpl_toolkits import mplot3d

    SurrogateModelList = []
    log_scale_value = np.array([np.log1p(0), np.log1p(1), np.log1p(10), np.log1p(100), np.log1p(1000), np.log1p(10000)])
    log_scale_naming = ['0','1', '10', '100', '1000','10000']


    for step in SurrogateModelSteps:
        IV_list = [
        {
            'Name':             'Conflict history',
            'Shortname':        'CH',
            'Columns':          ['ln_ged_sb_dep'],
            'Data':             Ensemble_df[[f'depvar_s_{step}']],
            'GAM':              LinearGAM(s(0,n_splines=10)),
            'Predictors':       ['Conflict history'],
            'scale_value':  log_scale_value, 
            'scale_naming': log_scale_naming,
            'rotation':         30
        },
        {
            'Name':      'Democracy',
            'Shortname': 'Dem',
            'Columns':    ['vdem_v2x_libdem'],
            'Data':      Ensemble_df[[f'libdem_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=7)),
            'Predictors': ['Liberal democracy'],
            'scale_value':  [0, 0.25, 0.5, 0.75, 1], 
            'scale_naming': [0, 0.25, 0.5, 0.75, 1],
            'rotation':         30
        },
        {
            'Name':      'Rule of law',
            'Shortname': 'Rule',
            'Columns':    ['vdem_v2x_rule'],
            'Data':      Ensemble_df[[f'rule_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=7)),
            'Predictors': ['Rule of law'],
            'scale_value':  [0, 0.25, 0.5, 0.75, 1], 
            'scale_naming': [0, 0.25, 0.5, 0.75, 1],
            'rotation':         30
        },
        {
            'Name':      'Population',
            'Shortname': 'Pop',
            'Columns':    ['wdi_sp_pop_totl'],
            'Data':      Ensemble_df[[f'pop_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=10)),
            'Predictors': ['Population'],
            'scale_value':  [], 
            'scale_naming': [],
            'rotation':         30
        },
        {
            'Name':      'Infant mortality',
            'Shortname': 'IMR',
            'Columns':    ['wdi_sp_dyn_imrt_in'],
            'Data':      Ensemble_df[[f'imr_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=5)),
            'Predictors': ['Infant mortality'],
            'scale_value':  [0,20,40,60,80,100], 
            'scale_naming': [0,20,40,60,80,100],
            'rotation':         30
        },
        {
            'Name':      'Neighborhood conflict',
            'Shortname': 'NCH',
            'Columns':    ['splag_1_decay_ged_sb_5'],
            'Data':      Ensemble_df[[f'nb_conflict_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=5)),
            'Predictors': ['Conflict in neighborhood'],
            'scale_value':  log_scale_value, 
            'scale_naming': log_scale_naming,
            'rotation':         30
        },
        {
            'Name':      'Topics: conflict and conflict stock',
            'Shortname': 'Topic10',
            'Columns':    ['topic10_conflict_t1','topic10_conflict_t1_stock'],
            'Data':      Ensemble_df[[f'topic_conflict_s_{step}',f'topic_conflict_stock_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=5) + s(1,n_splines=5)),
            'Predictors': ['Share of conflict in news','Share of conflict in news, stock'],
            'scale_value':  [0, 0.25, 0.5, 0.75, 1], 
            'scale_naming': [0, 0.25, 0.5, 0.75, 1],
            'rotation':         30
        },

        {
            'Name':      'Water services efficiency',
            'Shortname': 'Water',
            'Columns':    ['general_efficiency_t48'],
            'Data':      Ensemble_df[[f'water_efficiency_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=5)),
            'Predictors': ['General efficiency of water services'],
            'scale_value':  [0,20,40,60,80,100], 
            'scale_naming': [0,20,40,60,80,100],
            'rotation':         30
        },
        ]


        Other_models = [
        {
            'Name':      'Infant mortality and conflict history',
            'Shortname': 'IMRCH',
            'Columns':    ['wdi_sp_dyn_imrt_in','ln_ged_sb_dep'],
            'Data':      Ensemble_df[[f'imr_s_{step}',f'depvar_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=10) + s(1,n_splines=10)),
            'Predictors': ['Infant mortality','Conflict, t-1'],
            'scale_value':  log_scale_value, 
            'scale_naming': log_scale_naming,
            'rotation':         30
        },
        {
            'Name':       'Population and conflict history',
            'Shortname':  'PopCH',
            'Columns':    ['wdi_sp_pop_totl','ln_ged_sb_dep'],
            'Data':       Ensemble_df[[f'pop_s_{step}',f'depvar_s_{step}']],
            'GAM':        LinearGAM(s(0,n_splines=10) + s(1,n_splines=10)),
            'Predictors': ['Population','Conflict, t-1'],
            'scale_value':  log_scale_value, 
            'scale_naming': log_scale_naming,
            'rotation':         30
        },
        {
            'Name':      'Democracy and conflict history',
            'Shortname': 'DemCH',
            'Columns':    ['vdem_v2x_libdem','ln_ged_sb_dep'],
            'Data':      Ensemble_df[[f'libdem_s_{step}',f'depvar_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=10) + s(1,n_splines=10)),
            'Predictors': ['Liberal democracy','Conflict, t-1'],
            'scale_value':  log_scale_value, 
            'scale_naming': log_scale_naming,
            'rotation':         30
        },
        {
            'Name':      'Democracy and infant mortality',
            'Shortname': 'DIMR',
            'Columns':    ['vdem_v2x_libdem','wdi_sp_dyn_imrt_in'],
            'Data':      Ensemble_df[[f'libdem_s_{step}',f'imr_s_{step}']],
            'GAM':       LinearGAM(s(0,n_splines=5) + s(1,n_splines=5)),
            'Predictors': ['Liberal democracy','Infant mortality'],
            'scale_value':  log_scale_value, 
            'scale_naming': log_scale_naming,
            'rotation':         30
        },
        ]
        
        Prediction = Ensemble_df[f'step_pred_{step}']
        for IVset in IV_list:
            ModelDict = {
                'Modelname':   's' + str(step) + ' ' + IVset['Name'],
                'Shortname':   IVset['Shortname'],
                'Step':        step,
                'Columns':     IVset['Columns'],
                'IVs':         IVset['Data'],
                'Prediction':  Prediction,
                'GAM':         IVset['GAM'],
                'GAM_fit':     IVset['GAM'].fit(IVset['Data'], Prediction),
                'Predcolname': 's_pred_m' + IVset['Shortname'] + '_' + str(step),
            }
            print(ModelDict['Modelname'])
            Ensemble_df[ModelDict['Predcolname']]= ModelDict['GAM'].predict(ModelDict['IVs'])
            Ensemble_df[ModelDict['Predcolname']].describe()
            ModelDict['VarianceExplained'] = np.corrcoef(Prediction, Ensemble_df[ModelDict['Predcolname']])[0][1]**2
            ModelDict['GAM_summary'] = ModelDict['GAM'].summary
            ModelDict['filename'] = Plotpath + 'Surrogate_s' + str(step) + '_' + IVset['Shortname'] + '.png'
            if len(IVset['Data'].columns) == 1:
                plt.close()
                plt.scatter(IVset['Data'],Ensemble_df[ModelDict['Predcolname']],s=50)
                plt.ylim(0, 8)
                plt.xlabel(IVset['Predictors'][0])
                plt.ylabel('Predicted number of fatalities')
                plt.xticks(IVset['scale_value'],IVset['scale_naming'],rotation=IVset['rotation'])
                plt.yticks(log_scale_value, log_scale_naming, rotation=30)
                var = ModelDict['VarianceExplained']
                plt.title(ModelDict['Modelname'] + ', variance explained: ' + f'{var:.3f}')
                plt.savefig(ModelDict['filename'], dpi=300)

            if len(IVset['Data'].columns) == 2:
                plt.close()
                fig = plt.figure()
                ax = plt.axes(projection='3d')
                X = IVset['Data'].iloc[:, 0]
                Y = IVset['Data'].iloc[:, 1]
                Z = Ensemble_df[ModelDict['Predcolname']]
                ax.scatter3D(X, Y, Z, c=Z, cmap='jet');#
                ax.set_zlim3d(0, 8)
                ax.set_zlabel('Predicted fatalities')
                ax.set_ylabel(IVset['Predictors'][1])
                ax.set_xlabel(IVset['Predictors'][0])
                ax.set_zticks(log_scale_value)
                ax.set_zticklabels(log_scale_naming)
                var = ModelDict['VarianceExplained']
                plt.title(ModelDict['Modelname'] + ', variance explained: ' + f'{var:.3f}')
                horizontal_angle = 300
                vertical_angle  = 30
                ax.view_init(vertical_angle, horizontal_angle)    
                plt.savefig(ModelDict['filename'], dpi=300)
            SurrogateModelList.append(ModelDict)

    return(SurrogateModelList)

