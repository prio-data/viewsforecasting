


vmm_run <- function(data,s,model_type,train_start,train_end,test_start,test_end, return_only_prediction = T, predict_type = c('known','future'), end_of_history = NULL){
  target_var_name <- colnames(data)[1]
  ## Prep data
  data <- data %>% group_by(country_id) %>%
    mutate(target_month_id = month_id + s,
           markov_state2 = factor(case_when(!!sym(target_var_name)==0 & lag(!!sym(target_var_name)) == 0 ~ 'zero',
                                            !!sym(target_var_name) == 0 ~ 'risk_d',
                                            lag(!!sym(target_var_name)) == 0 ~ 'risk_e',
                                            T ~ 'conflict'),levels = c('zero','risk_d','risk_e','conflict')),
           markov_state_target = factor(case_when(!!sym(target_var_name)==0 & lag(!!sym(target_var_name),s) == 0 ~ 'zero',
                                                  !!sym(target_var_name) == 0 ~ 'risk_d',
                                                  lag(!!sym(target_var_name),s) == 0 ~ 'risk_e',
                                                  T ~ 'conflict'),levels = c('zero','risk_d','risk_e','conflict')),
           lead_markov_state_target = lead(markov_state_target,s),
           target_outcome = lead(!!sym(target_var_name),s),
           .before=1
    ) %>% ungroup()
  
  ## Divide into test and train
  train_period <- train_start:train_end
  test_period <- test_start:test_end
  data_train <- data %>% filter(target_month_id %in% train_period) %>% na.omit()
  data_test <- data %>% filter(target_month_id %in% test_period) %>% na.omit()
  
  ## Extract var names for vmm function
  vars <- data %>% select(7:ncol(data),-month_id,-country_id) %>% colnames()
  
  
  
  if(model_type == 'glm'){
    vmm_test <- train_and_predict_vmm_fatalities(data_train,
                                                 vars,
                                                 data_test,
                                                 'target_outcome',
                                                 target_state = "lead_markov_state_target")
  }else if(model_type == 'rf'){
    vmm_test <- train_and_predict_vmm_fatalities(data_train,
                                                 vars,
                                                 data_test,
                                                 'target_outcome',
                                                 target_state = "lead_markov_state_target",
                                                 rf_cont = T,
                                                 rf_cat = T)
  }
  if(predict_type == 'future'){
  vmm_test <- vmm_test %>% mutate(weighted_prediction = case_when(month_id > end_of_history ~ NA_real_,
                                                                  T ~ weighted_prediction))
  }
  if(return_only_prediction){
    return(vmm_test %>% mutate(step = s) %>% select(country_id,target_month_id,step,weighted_prediction)) %>%
      set_names(c('country_id','month_id','weighted_prediction'))
  }else{
    return(vmm_test %>% mutate(step = s))
  }
  
}