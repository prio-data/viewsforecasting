

## Set working directory to specified file
# setwd(getSrcDirectory(function(){})[1]) # This does not work, but wd seems to be set to file location regardless so should work anyway...

source("package_checker.R")
source("vmm_fatalities221016.R")
source('vmm_run.R')

library(ranger)
library(tidyverse)
library(magrittr)
library(arrow)

cat('\n', 'Packages loaded, starting script','\n')

### Neeeded
# month_id - hard coded, named var
# country_id - hard coded, named var
# target: first column of data
# data
# train_start
# train_end
# test_start
# test_end
# s
# prediction_type: ss or sc
# model_type: glm or rf
# end_of_history




data <- read_parquet('tmps/tmp_data.parquet')

pars <- read_parquet('tmps/tmp_pars.parquet')

mt <- pars$model_type # This should be read in as var


steps <- read_parquet('tmps/tmp_steps.parquet')$s
predict_type <- pars$predict_type # This should be read in as var
save_name <- pars$save_name
save_path <- pars$save_path

if(predict_type == 'future'){
end_of_history <- as.numeric(pars$end_of_history)
test_start <- end_of_history + steps[1]
test_end <- end_of_history + tail(steps)[1]
train_start <- 121 #
train_end <- end_of_history 
}else{
  partitions <- read_parquet("tmps/tmp_partitions.parquet")
  train_start <- partitions$train[1] # This should be read in as var
  train_end <- partitions$train[2]  # This should be read in as var
  test_start <- partitions$predict[1] 
  test_end <- partitions$predict[2] 
}

if(mt == 'both'){
  mt <- c('rf','glm')
}

for(model_type in mt){

if(model_type == 'glm'){
  unwanted_vars <- c('gleditsch_ward')
  data <- data %>% select(-any_of(unwanted_vars))
}


#tictoc::tic()
vmm_predictions <- steps %>% map(~vmm_run(data,.x,model_type,train_start,train_end,test_start,test_end,predict_type = predict_type, end_of_history = end_of_history)) %>% bind_rows()
#tictoc::toc()

ss_predictions <- vmm_predictions %>% pivot_wider(values_from = 'weighted_prediction',names_from='step',names_prefix = 'step_pred_')



if(predict_type == 'future'){
  sc_predictions <- vmm_predictions %>% filter(target_month_id - step == end_of_history)
  write_parquet(ss_predictions,paste(save_path,'markov_',save_name,'_ss_',model_type,'_',end_of_history,'.parquet',sep=""))
  write_parquet(sc_predictions,paste(save_path,'markov_',save_name,'_sc_',model_type,'_',end_of_history,'.parquet',sep=""))
}else{
  
  write_parquet(ss_predictions,paste(save_path,'markov_',save_name,'_ss_',predict_type,'_',model_type,'.parquet',sep=""))
  for(i in test_start:test_end){
  sc_predictions <- vmm_predictions %>% filter(target_month_id - step == i-1)
  write_parquet(sc_predictions,paste(save_path,'markov_',save_name,'_sc_',i,'_',predict_type,'_',model_type,'.parquet',sep=""))
  }
  
}
}

cat('\n Rscript finished! \n')































