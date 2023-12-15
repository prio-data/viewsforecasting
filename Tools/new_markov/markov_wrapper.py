from viewser import Queryset, Column
import pandas as pd
from markov_params import *
import os
import subprocess
import shutil


os.makedirs('tmps', exist_ok=True)
#os.makedirs('results', exist_ok=True)

qs2 = Queryset(qs,'country_month')

data = qs2.fetch()
data = data.fillna(0)
data.to_parquet('tmps/tmp_data.parquet')

pd.DataFrame({'s':steps}).to_parquet('tmps/tmp_steps.parquet')

if predict_type == 'future':
  pars = {"model_type":model_type,"predict_type":predict_type,"end_of_history":EndOfHistory, 'save_name':save_name, 'save_path':save_path}
elif predict_type == 'test':
  pars = {"model_type":model_type,"predict_type":predict_type, 'save_name':save_name, 'save_path':save_path}
  pd.DataFrame(test_partitioner_dict).to_parquet('tmps/tmp_partitions.parquet')
elif predict_type == 'calib':
  pars = {"model_type":model_type,"predict_type":predict_type, 'save_name':save_name, 'save_path':save_path}
  pd.DataFrame(calib_partitioner_dict).to_parquet('tmps/tmp_partitions.parquet')
elif predict_type == 'custom':
  pars = {"model_type":model_type,"predict_type":predict_type, 'save_name':save_name, 'save_path':save_path}
  pd.DataFrame(custom_partitioner_dict).to_parquet('tmps/tmp_partitions.parquet')

pd.DataFrame(pd.Series(pars,dtype='string')).transpose().to_parquet('tmps/tmp_pars.parquet')


subprocess.call(["Rscript","omm_fatalities_flex_pywrap.R"])

if(predict_type == 'future'):
  if model_type == 'both':
    sc_rf_predictions = pd.read_parquet('tmps/tmp_sc_rf.parquet')
    sc_rf_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_sc_rf_'+str(EndOfHistory)+'.parquet')
    sc_glm_predictions = pd.read_parquet('tmps/tmp_sc_glm.parquet')
    sc_glm_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_sc_glm_'+str(EndOfHistory)+'.parquet')
    ss_rf_predictions = pd.read_parquet('tmps/tmp_ss_rf.parquet')
    ss_rf_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_ss_rf_'+str(EndOfHistory)+'.parquet')  
    ss_glm_predictions = pd.read_parquet('tmps/tmp_ss_glm.parquet')
    ss_glm_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_ss_glm_'+str(EndOfHistory)+'.parquet')  
  else:
    sc_predictions = pd.read_parquet('tmps/tmp_sc_'+model_type+'.parquet')
    sc_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_sc_'+model_type+'_'+str(EndOfHistory)+'.parquet') 
    ss_predictions = pd.read_parquet('tmps/tmp_ss_'+model_type+'.parquet')
    ss_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_ss_'+model_type+'_'+str(EndOfHistory)+'.parquet') 

else:
  if model_type == 'both':
    ss_rf_predictions = pd.read_parquet('tmps/tmp_ss_rf.parquet')
    ss_rf_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_ss_rf_'+predict_type+'.parquet')
    ss_glm_predictions = pd.read_parquet('tmps/tmp_ss_glm.parquet')
    ss_glm_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_ss_glm_'+predict_type+'.parquet')
  else:
    ss_predictions = pd.read_parquet('tmps/tmp_ss.parquet')
    ss_predictions.set_index(['month_id','country_id']).to_parquet(save_path+'markov_'+save_name+'_ss_'+model_type+'_'+predict_type+'.parquet')

if cleenup:
  shutil.rmtree('tmps')
  
