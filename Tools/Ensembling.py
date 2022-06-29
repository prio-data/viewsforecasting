# This script file collects a set of routines used in the ensembling and calibration of models

# Importing modules
# Basics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
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




# Calibrate to conform to mean and standard deviation

# Calibration function
def mean_sd_calibrated(y_true_calpart,y_pred_calpart,y_pred_test,shift, threshold=0):
    ''' 
    Calibrates predictions. Expects the input columns from calibration partition to be without infinity values
    '''
    expand = y_true_calpart.loc[y_true_calpart>=threshold].std() / y_pred_calpart.loc[y_pred_calpart>=threshold].std()
    shiftsize = 0
    expanded = y_pred_test.copy()
    expanded.loc[expanded>=threshold] = expanded * expand
    if shift==True:
        shiftsize = y_true_calpart.loc[y_true_calpart>=threshold].mean() - y_pred_calpart.loc[y_pred_calpart>=threshold].mean()
        shifted = expanded
        shifted.loc[shifted>=threshold] = shifted + shiftsize
        calibrated_pred = shifted 
    if shift==False:
        calibrated_pred = expanded       
#    print('Calibration --', 'threshold:',threshold,'Shift:',shiftsize,'Expand:',expand)
    return (calibrated_pred,expand,shiftsize)

# GAM-based calibration function
def gam_calibrated(y_true_calpart,y_pred_calpart,y_pred_test,n_splines):
    ''' 
    Calibrates predictions using GAM.
    Expects the input columns from calibration partition to be without infinity values
    '''
    from pygam import LogisticGAM, LinearGAM, s, te
    gam = LinearGAM(s(0, constraints='monotonic_inc',n_splines = n_splines)).fit(y_pred_calpart, y_true_calpart)

    calibrated_pred = gam.predict(y_pred_test)
#    gam_summary = gam.summary()
    return (calibrated_pred, gam)


# Retrieving the predictions for calibration and test partitions
# The ModelList contains the predictions organized by model

def RetrieveStoredPredictions(ModelList,steps,EndOfHistory,dev_id):
    ''' This function retrieves the predictions stored in ViEWS prediction storage for all models in the list passed to it.
    It assumes that each element in the list is a dictionary that contains a model['modelname'] '''
    i=0
    stepcols = ['ln_ged_sb_dep']
    for step in steps:
        stepcols.append('step_pred_' + str(step))
    level = 'cm'
    for model in ModelList:
        print(i, model['modelname'])
        stored_modelname_calib = level + '_' + model['modelname'] + '_calib'
        stored_modelname_test = level + '_' + model['modelname'] + '_test'
        stored_modelname_future = level +  '_' + model['modelname'] + '_f' + str(EndOfHistory)
        model['predictions_calib_df'] = pd.DataFrame.forecasts.read_store(stored_modelname_calib, run=dev_id)[stepcols]
        model['predictions_calib_df'].replace([np.inf, -np.inf], 0, inplace=True)
        model['predictions_test_df'] = pd.DataFrame.forecasts.read_store(stored_modelname_test, run=dev_id)[stepcols]
        model['predictions_test_df'].replace([np.inf, -np.inf], 0, inplace=True)
        i = i + 1
    print('All done')
    return(ModelList)

def RetrieveStoredPredictions_pgm(ModelList, steps, EndOfHistory, run_id, level, get_future):
    ''' This function retrieves the predictions stored in ViEWS prediction storage for all models in the list passed to it.
    It assumes that each element in the list is a dictionary that contains a model['modelname'] '''
    i = 0
    stepcols = ['ln_ged_sb_dep']
    for step in steps:
        stepcols.append('step_pred_' + str(step))
    for model in ModelList:
        print(i, model['modelname'])
        stored_modelname_calib = level + '_' + model['modelname'] + '_calib'
        stored_modelname_test = level + '_' + model['modelname'] + '_test'
        stored_modelname_future = level + '_' + model['modelname'] + '_f' + str(EndOfHistory)
        model['predictions_calib_df'] = pd.DataFrame.forecasts.read_store(stored_modelname_calib, run=run_id)[
                stepcols]
        model['predictions_calib_df'].replace([np.inf, -np.inf], 0, inplace=True)
        model['predictions_test_df'] = pd.DataFrame.forecasts.read_store(stored_modelname_test, run=run_id)[
                stepcols]
        model['predictions_test_df'].replace([np.inf, -np.inf], 0, inplace=True)
        if get_future:
            model['predictions_future_df'] = pd.DataFrame.forecasts.read_store(stored_modelname_future, run=run_id)
            model['predictions_future_df'].replace([np.inf, -np.inf], 0, inplace=True)
        i = i + 1
    print('All done')
    return (ModelList)

    # Calibration
def CalibratePredictions(ModelList, FutureStart, steps):
    '''
    Function that adds dfs with calibrated predictions to ModelList
    '''

    print('Calibrating models')

    stepcols = ['ln_ged_sb_dep']
    for step in steps:
        stepcols.append('step_pred_' + str(step))
        
    for model in ModelList:   
        model['calib_df_cal_expand'] = model['predictions_calib_df'].copy()
        model['test_df_cal_expand'] = model['predictions_test_df'].copy()
    #    if IncludeFuture:
    #        model['future_df_cal_expand'] = model['predictions_future_df'].copy()
        model['calib_df_calibrated'] = model['predictions_calib_df'].copy()
        model['test_df_calibrated'] = model['predictions_test_df'].copy()
    #    if IncludeFuture:
    #        model['future_df_calibrated'] = model['predictions_future_df'].copy()
        print(model['modelname'])
        model['calibration_gams'] = [] # Will hold calibration GAM objects, one for each step
        for col in stepcols[1:]:
            thisstep = int(col[10:])
            thismonth = FutureStart + thisstep
            calibration_gam_dict = {
                'Step': thisstep,
                'GAM': []
            }
            # Remove from model dfs rows where [col] has infinite values (due to the 2011 split of Sudan)
            df_calib = model['predictions_calib_df'][~np.isinf(model['predictions_calib_df'][col])].fillna(0)
            df_test = model['predictions_test_df'][~np.isinf(model['predictions_test_df'][col])].fillna(0)
    #        if IncludeFuture:
    #            df_future = model['predictions_future_df'][~np.isinf(model['predictions_future_df']['step_combined'])].fillna(0)

            (model['calib_df_cal_expand'][col],model['expanded'],model['shiftsize']) = mean_sd_calibrated(
                y_true_calpart = df_calib['ln_ged_sb_dep'], 
                y_pred_calpart = df_calib[col], 
                y_pred_test = df_calib[col], 
                shift=False, 
                threshold = 0
            )
            (model['test_df_cal_expand'][col],model['expanded'],model['shiftsize']) = mean_sd_calibrated(
                y_true_calpart = df_calib['ln_ged_sb_dep'], 
                y_pred_calpart = df_calib[col], 
                y_pred_test = df_test[col], 
                shift=False, 
                threshold = 0
            )
            if model['modelname'] == 'fat_hh20_Markov_glm' or model['modelname'] == 'fat_hh20_Markov_rf':
                model['calib_df_calibrated'][col] = model['calib_df_cal_expand'][col]
                model['test_df_calibrated'][col] = model['test_df_cal_expand'][col]
            else:
                (model['calib_df_calibrated'][col], calibration_gam_dict['calibration_GAM']) = gam_calibrated(
                        y_true_calpart = df_calib['ln_ged_sb_dep'], 
                        y_pred_calpart = df_calib[col], 
                        y_pred_test = df_calib[col], 
                        n_splines = 15
                )
                #print(model['calibration_gam'].summary())
                (model['test_df_calibrated'][col], gam) = gam_calibrated(
                        y_true_calpart = df_calib['ln_ged_sb_dep'], 
                        y_pred_calpart = df_calib[col], 
                        y_pred_test = df_test[col], 
                        n_splines = 15
                )
            model['calibration_gams'].append(calibration_gam_dict)
    return(ModelList)


# calibration of pgm predictions using cm predictions:
def calibrate_pg_with_c(df_pgm, df_cm, column, df_pg_id_c_id=None, log_feature=False, super_calibrate=False):
    try:
        assert df_pgm.index.names[0] == 'month_id'
    except AssertionError:
        raise ValueError(f"Expected pgm df to have month_id as 1st index")

    try:
        assert df_pgm.index.names[1] in ['priogrid_gid', 'priogrid_id', 'pg_id']
    except AssertionError:
        raise ValueError(f"Expected pgm df to have one of priogrid_gid, priogrid_id, pg_id as 2nd index")

    try:
        assert df_cm.index.names[0] == 'month_id'
    except AssertionError:
        raise ValueError(f"Expected cm df to have month_id as 1st index")

    try:
        assert df_cm.index.names[1] in ['country_id', 'c_id']
    except AssertionError:
        raise ValueError(f"Expected cm df to have one of country_id, c_id as 2nd index")

    try:
        assert column in df_pgm.columns
    except AssertionError:
        raise ValueError(f"Specified column not in pgm df")

    try:
        assert column in df_cm.columns
    except AssertionError:
        raise ValueError(f"Specified column not in cm df")

    input_months_cm = list(set(df_cm.index.get_level_values(0)))
    input_months_pgm = list(set(df_pgm.index.get_level_values(0)))

    input_months_cm.sort()
    input_months_pgm.sort()

    try:
        assert input_months_cm == input_months_pgm
    except AssertionError:
        raise ValueError(f"Inconsistent months found in input dfs")

    input_countries = list(set(df_cm.index.get_level_values(1)))
    input_pgs = list(set(df_pgm.index.get_level_values(1)))
    input_pgs.sort()

    if df_pg_id_c_id is None:
        print('Fetching pd-month-->country-month df from service')
        df_pg_id_c_id = fetch_df_pg_id_c_id()

    pg_size = len(input_pgs)

    normalised = np.zeros((df_pgm[column].size))

    if log_feature:
        df_to_calib = pd.DataFrame(index=df_pgm.index, columns=[column, ], data=np.exp(df_pgm[column].values) - 1)
        df_calib_from = pd.DataFrame(index=df_cm.index, columns=[column, ], data=np.exp(df_cm[column].values) - 1)
    else:
        df_to_calib = pd.DataFrame(index=df_pgm.index, columns=[column, ], data=df_pgm[column].values)
        df_calib_from = pd.DataFrame(index=df_cm.index, columns=[column, ], data=df_cm[column].values)

    for imonth, month in enumerate(input_months_pgm):

        istart = imonth * pg_size
        iend = istart + pg_size

        normalised_month = np.zeros((pg_size))

        df_data_month_pgm = pd.DataFrame(df_to_calib[column].loc[month])

        values_month_pgm = df_to_calib[column].loc[month].values.reshape(pg_size)

        df_data_month_cm = pd.DataFrame(df_calib_from[column].loc[month])

        map_month = df_pg_id_c_id.loc[month].values.reshape(pg_size)

        input_countries = list(set(df_data_month_cm.index.get_level_values(0)))

        for country in input_countries:
            month_country = df_data_month_cm[column].loc[country]
            mask = (map_month == country)

            nmask = np.count_nonzero(mask)

            pg_sum = np.sum(values_month_pgm[mask])

            value_month_cm = df_calib_from[column].loc[month, country]

            if pg_sum > 0:
                normalisation = value_month_cm / pg_sum * np.ones((nmask))

                normalised_month[mask] = values_month_pgm[mask] * normalisation

        if super_calibrate:
            sum_month_cm = np.sum(df_data_month_cm[column])
            if np.sum(normalised_month) > 0:
                normalisation = sum_month_cm / np.sum(normalised_month)
                normalised_month *= normalisation

        normalised[istart:iend] = normalised_month

    if log_feature:
        normalised = np.log(normalised + 1)

    df_out = pd.DataFrame(index=df_pgm.index, columns=[column, ], data=normalised)

    return df_out


# helper function for pgm-cm calibration, which fetches country-ids for pg-ids
def fetch_df_pg_id_c_id():
    qs = (Queryset("jed_pgm_cm", "priogrid_month")
          .with_column(Column("country_id", from_table="country_month", from_column="country_id")

                       )
          )

    df_pg_id_c_id = qs.publish().fetch()

    return df_pg_id_c_id