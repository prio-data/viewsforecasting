this_parent <- dirname(getwd())
markov_path <- '/Tools/markov/'
this_path=paste(this_parent,'/Tools/markov/',sep="")

source(paste(this_path,'package_checker.R',sep=""))
source(paste(this_path,'vmm_fatalities211210.R',sep=""))
source(paste(this_path,'models2.R',sep=""))
library(ranger)
library(tidyverse)
library(magrittr)
library(arrow)

cat('\n', 'Packages loaded, starting script','\n')

args = commandArgs(trailingOnly=TRUE)

cur_month <- as.numeric(args[1])
data_path <- args[2]
save_path <- args[3]

#s = as.numeric(commandArgs(trailingOnly=TRUE)[1])
train_period_calib <- 121:444
train_period_full <- 121:(cur_month)
calib_period <- 445:(cur_month)
test_period <- (cur_month+1):(cur_month+36)



## Dataprep
tictoc::tic()
cm <- read_parquet(data_path)
vars <- colnames(cm)[c(1:5,8:39)]
#rs_f <- NULL

for(s in 1:36){
  
  tictoc::tic()
  cm2 <- cm %>% group_by(country_id) %>%
    mutate(target_month_id = month_id + s,
           ged_best_sb = exp(ln_ged_sb)-1,
           ged_best_sb_target = lead(ged_best_sb,s),
           ln_ged_best_sb = log(ged_best_sb+1),
           ln_ged_best_sb_target = log(ged_best_sb_target+1),
           ln_ged_best_sb_lag = lag(ln_ged_best_sb),
           ln_ged_best_sb_lag = case_when(is.na(ln_ged_best_sb_lag) ~ 0,
                                          T ~ ln_ged_best_sb_lag),
           markov_state = as.factor(case_when(ged_best_sb==0 & lag(ged_best_sb) == 0 ~ 'zero',
                                              ged_best_sb == 0 ~ 'risk',
                                              lag(ged_best_sb) == 0 ~ 'risk',
                                              T ~ 'conflict')),
           markov_state2 = factor(case_when(ged_best_sb==0 & lag(ged_best_sb) == 0 ~ 'zero',
                                            ged_best_sb == 0 ~ 'risk_d',
                                            lag(ged_best_sb) == 0 ~ 'risk_e',
                                            T ~ 'conflict'),levels = c('zero','risk_d','risk_e','conflict')),
           markov_state3 = as.factor(case_when(ged_best_sb==0 ~ 'zero',
                                               T ~ 'conflict')),
           markov_state_target = factor(case_when(ged_best_sb==0 & lag(ged_best_sb,s) == 0 ~ 'zero',
                                                  ged_best_sb == 0 ~ 'risk_d',
                                                  lag(ged_best_sb,s) == 0 ~ 'risk_e',
                                                  T ~ 'conflict'),levels = c('zero','risk_d','risk_e','conflict')),
           #lead_markov_state = lead(markov_state),
           #lead_markov_state2_1 = lead(markov_state2,1),
           #lag_markov_state3 = lag(markov_state3),
           #lead_markov_state3 = lead(markov_state3),
           #lag_markov_state = lag(markov_state),
           #lag_markov_state2 = lag(markov_state2),
           lead_markov_state_target = lead(markov_state_target,s)
    ) %>% ungroup() %>%
    select(ends_with('_id'),starts_with('ged_best_sb'),starts_with("ln_ged_best_sb"),all_of(vars),contains('markov')) %>% 
    select(-contains('benchmark'))
  
  cm2_train_full <- cm2 %>% filter(target_month_id %in% train_period_full) %>% na.omit()
  cm2_train_calib <- cm2 %>% filter(target_month_id %in% train_period_calib) %>% na.omit()
  cm2_test <- cm2 %>% filter(target_month_id %in% test_period) %>% na.omit()
  cm2_calib <- cm2 %>% filter(target_month_id %in% calib_period) %>% na.omit()
  
  #ch2 <- c('ln_ged_best_sb',confhist_2019)
  
  
  #f1 <- as.formula(paste('ln_ged_best_sb_target~',paste(vars,collapse = '+'),sep=''))
  
  #r1 <- ranger(f1,data = cm2_train)
  
  vmm_test_glm <- train_and_predict_vmm_fatalities(cm2_train_full,vars,cm2_test,'ln_ged_best_sb_target',target_state = "lead_markov_state_target")
  vmm_calib_glm <- train_and_predict_vmm_fatalities(cm2_train_calib,vars,cm2_calib,'ln_ged_best_sb_target',target_state = "lead_markov_state_target")
  
  #vmm_test2 <- train_and_predict_vmm_fatalities(cm2_train,vars,cm2_test,'ln_ged_best_sb_target',target_state = "lead_markov_state_target",rf_cont = T)
  #vmm_test3 <- train_and_predict_vmm_fatalities(cm2_train,vars,cm2_test,'ln_ged_best_sb_target',target_state = "lead_markov_state_target",rf_cat = T)
  vmm_test_rf <- train_and_predict_vmm_fatalities(cm2_train_full,vars,cm2_test,'ln_ged_best_sb_target',target_state = "lead_markov_state_target",rf_cont = T,rf_cat = T)
  vmm_calib_rf <- train_and_predict_vmm_fatalities(cm2_train_calib,vars,cm2_calib,'ln_ged_best_sb_target',target_state = "lead_markov_state_target",rf_cont = T,rf_cat = T)
  tictoc::toc()
  stp <- paste("step_",s,sep="")
  nms <- c('month_id','country_id',stp)
  
  res <- list(test_glm=vmm_test_glm,
              test_rf=vmm_test_rf,
              calib_glm =vmm_calib_glm,
              calib_rf=vmm_calib_rf)
  
  # rs <- eval_vmm_paper(res)
  # 
  # rs_f <- bind_rows(rs_f,rs)
  # print(rs)
  cat(s,"\n")
  if(s == 1){
    
    calib_pred_glm <- vmm_calib_glm %>% select(target_month_id,country_id,weighted_prediction) %>% set_names(nms)
    calib_pred_rf <- vmm_calib_rf%>% select(target_month_id,country_id,weighted_prediction)  %>% set_names(nms)
    
    test_pred_glm <- vmm_test_glm %>% select(target_month_id,country_id,weighted_prediction)  %>% set_names(nms)
    test_pred_rf <- vmm_test_rf%>% select(target_month_id,country_id,weighted_prediction) %>% set_names(nms)
    
  }else{
    calib_pred_glm <- calib_pred_glm %>% left_join(vmm_calib_glm %>% select(target_month_id,country_id,weighted_prediction) %>% set_names(nms))
    calib_pred_rf <- calib_pred_rf %>% left_join(vmm_calib_rf%>% select(target_month_id,country_id,weighted_prediction)  %>% set_names(nms))
    
    test_pred_glm <- test_pred_glm %>% left_join(vmm_test_glm %>% select(target_month_id,country_id,weighted_prediction) %>% set_names(nms))
    test_pred_rf <- test_pred_rf %>% left_join(vmm_test_rf%>% select(target_month_id,country_id,weighted_prediction)  %>% set_names(nms))
    
  }
  
}



calib_pred_glm <- calib_pred_glm %>% set_names(c('month_id','country_id',paste('step_pred_',1:36,sep="")))
calib_pred_rf <-calib_pred_rf %>% set_names(c('month_id','country_id',paste('step_pred_',1:36,sep="")))
test_pred_glm <- test_pred_glm %>% set_names(c('month_id','country_id',paste('step_pred_',1:36,sep="")))
test_pred_rf <- test_pred_rf %>% set_names(c('month_id','country_id',paste('step_pred_',1:36,sep="")))

# test_pred_glm2 <- test_pred_glm %>% set_names(c('month_id','country_id',paste('step_pred_',1:36,sep="")))
# test_pred_rf2 <- test_pred_rf %>% set_names(c('month_id','country_id',paste('step_pred_',1:36,sep="")))
# 
# for(i in 1:36){
#   test_pred_glm[(test_pred_glm$month_id-i) >= cur_month+1 ,i+2] <- NA
#   test_pred_rf[(test_pred_rf$month_id-i) >= cur_month+1 ,i+2] <- NA
# }

test_pred_glm_out <- test_pred_glm %>% pivot_longer(3:38,values_to = "step_combined") %>%
  mutate(step = str_remove(name,'step_pred_'),
         step = as.numeric(step)) %>%
  filter(month_id - step == cur_month) %>% select(1:2,4)


test_pred_rf_out <- test_pred_rf %>% pivot_longer(3:38,values_to = "step_combined") %>%
  mutate(step = str_remove(name,'step_pred_'),
         step = as.numeric(step)) %>%
  filter(month_id - step == cur_month)%>% select(1:2,4)




write_csv(test_pred_glm_out,paste(save_path,"vmm_glm_hh20_",cur_month,'.csv',sep=""))
write_csv(test_pred_rf_out,paste(save_path,"vmm_rf_hh20_",cur_month,'.csv',sep=""))


# 
# write_csv(calib_pred_glm,'predictions/vmm_glm_hh20_0307_alt_calib.csv')
# write_csv(calib_pred_rf,'predictions/vmm_rf_hh20_0307_alt_calib.csv')
# write_csv(test_pred_glm,'predictions/vmm_glm_hh20_0307_alt_fut.csv')
# write_csv(test_pred_rf,'predictions/vmm_rf_hh20_0307_alt_fut.csv')
# 
# 
















































