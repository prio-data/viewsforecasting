from viewser import Queryset, Column
import pandas as pd
from markov_params import *
import os
import subprocess
import shutil


os.makedirs('tmps', exist_ok=True)
os.makedirs('results', exist_ok=True)

qs2 = Queryset(qs,'country_month')

data = qs2.fetch()
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

if cleenup:
  shutil.rmtree('tmps')
  
