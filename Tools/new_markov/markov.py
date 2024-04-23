from viewser import Queryset, Column
import pandas as pd
from . import markov_params
#from markov_params import *
import os
import subprocess
import shutil

def compute_markov(partitioner_dict, EndOfHistory, depvar, predict_type, model_type):
    os.makedirs('tmps', exist_ok=True)
    os.makedirs('results', exist_ok=True)

    qs2 = Queryset(markov_params.qs,'country_month')

    data = qs2.fetch()
    data = data.fillna(0)
    data.to_parquet('tmps/tmp_data.parquet')

    pd.DataFrame({'s':markov_params.steps}).to_parquet('tmps/tmp_steps.parquet')

    if predict_type == 'future':
        pars = {"model_type":model_type,"predict_type":predict_type,"end_of_history":EndOfHistory, 'save_name':markov_params.save_name, 'save_path':markov_params.save_path}
    elif predict_type == 'test':
        pars = {"model_type":model_type,"predict_type":predict_type, 'save_name':markov_params.save_name, 'save_path':markov_params.save_path}
        pd.DataFrame(partitioner_dict).to_parquet('tmps/tmp_partitions.parquet') 
    elif predict_type == 'calib':
        pars = {"model_type":model_type,"predict_type":predict_type, 'save_name':markov_params.save_name, 'save_path':markov_params.save_path}
        pd.DataFrame(partitioner_dict).to_parquet('tmps/tmp_partitions.parquet')
    else:
        raise ValueError(f'Unrecognised predict type: {predict_type}')
        

    pd.DataFrame(pd.Series(pars,dtype='string')).transpose().to_parquet('tmps/tmp_pars.parquet')


    subprocess.call(["Rscript","../Tools/new_markov/omm_fatalities_flex_pywrap.R"])


    if predict_type == 'future':

        df = pd.read_parquet('tmps/tmp_sc_'+model_type+'.parquet').set_index(['month_id','country_id'])
        df[depvar]=data[depvar]

    else:
    
        df = pd.read_parquet('tmps/tmp_ss_'+model_type+'.parquet').set_index(['month_id','country_id'])
        df[depvar]=data[depvar]

    if markov_params.cleenup:
        shutil.rmtree('tmps')
        
    return df
  
