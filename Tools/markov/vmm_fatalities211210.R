library(tidyverse)

formula_creator <- function(model_ivs,target=NULL){
  if(!is.null(target)){
    return(as.formula(paste(target,"~",paste(model_ivs,collapse='+'))))
  }else{
    return(as.formula(paste("~",paste(model_ivs,collapse='+'))))
    
  }
}

p_matrix_for_individual <- function(trained_logits,nd){
  pm <- matrix(0,4,4)
  colnames(pm) <- rownames(pm) <- c('conflict','risk_d','risk_e','zero')
  pm[1,1] <- 1-predict(trained_logits$conflict,newdata=nd,type='r')
  pm[1,2] <- predict(trained_logits$conflict,newdata=nd,type='r')
  pm[2,3] <- 1 - predict(trained_logits$risk_d,newdata=nd,type='r')
  pm[2,4] <- predict(trained_logits$risk_d,newdata=nd,type='r')
  pm[3,1] <- 1 - predict(trained_logits$risk_e,newdata=nd,type='r')
  pm[3,2] <- predict(trained_logits$risk_e,newdata=nd,type='r')
  pm[4,3] <- 1-predict(trained_logits$zero,newdata=nd,type='r')
  pm[4,4] <- predict(trained_logits$zero,newdata=nd,type='r')
  return(pm)
}

p_row_from_multinom <- function(trained_multinoms,nd){
  preds <- trained_multinoms %>% map(~predict(.x,newdata=nd,type='probs'))
  return(preds[[nd$markov_state2]])
}

p_row_from_rf <- function(trained_rf,nd){
  preds <- trained_rf %>% map(~predict(.x,data=nd)$predictions)
  return(preds[[nd$markov_state2]])
}


p_matrix_to_probs_steps_ahead <- function(trained_logits,nd,steps=1){
  start_state <- nd$markov_state2
  p_matrix <- p_matrix_for_individual(trained_logits,nd)
  if(steps == 1){
    return(p_matrix[start_state,])
  }else{
    p_matrix_2 <- p_matrix
    for(i in 2:steps){
      p_matrix_2 <- p_matrix_2 %*% p_matrix
    }
    return(p_matrix_2[start_state,])
  }
}

train_models_logits <- function(data,model_ivs,target_state){
  groups_state <- group_keys(data %>% group_by(markov_state2))
  data2 <- group_split(data, markov_state2)
  models_state <- data2 %>% map(~glm(formula_creator(model_ivs,target_state),family='binomial',data=.x)) %>% set_names(paste(groups_state[[1]]))
  return(models_state)
}

train_models_multinom <- function(data,model_ivs,step=2){
  target_state <- paste('lead_markov_state2_',step,sep='')
  groups_state <- group_keys(data %>% group_by(markov_state2))
  data2 <- group_split(data, markov_state2)
  models_state <- data2 %>% map(~multinom(formula_creator(model_ivs,target_state),family='binomial',data=.x)) %>% set_names(paste(groups_state[[1]]))
  return(models_state)
}

train_models_rf_one <- function(data,model_ivs,target_state){
  groups_state <- group_keys(data %>% group_by(markov_state2))
  data2 <- group_split(data, markov_state2)
  models_state <- data2 %>% map(~ranger(formula_creator(model_ivs,target_state),data=.x,probability = T)) %>% set_names(paste(groups_state[[1]]))
  return(models_state)
}

train_models_rf <- function(data,model_ivs,step=2){
  target <- paste('lead_markov_state2_',step,sep='')
  groups_state <- group_keys(data %>% group_by(markov_state2))
  data2 <- group_split(data, markov_state2)
  models_state <- data2 %>% map(~ranger(formula_creator(model_ivs,target),data=.x,probability = T)) %>% set_names(paste(groups_state[[1]]))
  return(models_state)
}


#data <- train
train_models_ols <- function(data,model_ivs,target = 'delta_s1',target_state='lead_markov_state_target'){
  groups_state <- group_keys(data %>% group_by(markov_state2,!!sym(target_state)))
  data2 <- group_split(data, markov_state2,!!sym(target_state))
  models_state <- data2 %>% map(~lm(formula_creator(model_ivs,target),data=.x)) %>% set_names(paste(groups_state[[1]],groups_state[[2]],sep="_"))
  return(models_state)
}

train_models_rf_cont <- function(data,model_ivs,target = 'delta_s1',target_state = 'lead_markov_state_target'){
  groups_state <- group_keys(data %>% group_by(markov_state2,!!sym(target_state)))
  data2 <- group_split(data, markov_state2,!!sym(target_state))
  #groups_state <- groups_state[c(1,3,5,7),]
  #data2 <- data2[c(1,3,5,7)]
  models_state <- data2 %>% map(~ranger(formula_creator(model_ivs,target),data=.x)) %>% set_names(paste(groups_state[[1]],groups_state[[2]],sep="_"))
  return(models_state)
}

train_models_ols_step <- function(data,model_ivs,step=2){
  target <- paste('delta_s',step,sep='')
  lead_target <- paste('lead_markov_state2_',step,sep='')
  data <- data %>% mutate(dynm = case_when(!!sym(lead_target) %in% c('conflict','risk_e') ~ 'esc',
                                           T ~ 'deesc'))
  groups_state <- group_keys(data %>% group_by(markov_state2,dynm))
  data2 <- group_split(data, markov_state2,dynm)
  data2 <- data2[which(groups_state$dynm=='esc')]
  groups_state <- groups_state[which(groups_state$dynm=='esc'),]
  models_state <- data2 %>% map(~lm(formula_creator(model_ivs,target),data=.x)) %>% set_names(paste(groups_state[[1]]))
  return(models_state)
}

train_models_rf_reg_step <- function(data,model_ivs,step=2){
  target <- paste('delta_s',step,sep='')
  lead_target <- paste('lead_markov_state2_',step,sep='')
  data <- data %>% mutate(dynm = case_when(!!sym(lead_target) %in% c('conflict','risk_e') ~ 'esc',
                                           T ~ 'deesc'))
  groups_state <- group_keys(data %>% group_by(markov_state2,dynm))
  data2 <- group_split(data, markov_state2,dynm)
  data2 <- data2[which(groups_state$dynm=='esc')]
  groups_state <- groups_state[which(groups_state$dynm=='esc'),]
  models_state <- data2 %>% map(~ranger(formula_creator(model_ivs,target),data=.x)) %>% set_names(paste(groups_state[[1]]))
  return(models_state)
}


predict_models_ols_step <- function(trained_models_ols,nd,step=1){
  out <- matrix(0,nrow(nd),2)
  colnames(out) <- c(paste('hat_ds',step,'_esc',sep=""),paste('hat_ds',step,'_deesc',sep=""))
  out[which(nd$markov_state2=='conflict'),1] <-  predict(trained_models_ols$conflict,newdata = nd[which(nd$markov_state2=='conflict'),])
  out[which(nd$markov_state2=='conflict'),2] <-  -nd[which(nd$markov_state2=='conflict'),]$ln_ged_best_sb
  out[which(nd$markov_state2=='risk_e'),1] <-  predict(trained_models_ols$risk_e,newdata = nd[which(nd$markov_state2=='risk_e'),])
  out[which(nd$markov_state2=='risk_e'),2] <-  -nd[which(nd$markov_state2=='risk_e'),]$ln_ged_best_sb
  out[which(nd$markov_state2=='risk_d'),1] <-  predict(trained_models_ols$risk_d,newdata = nd[which(nd$markov_state2=='risk_d'),])
  out[which(nd$markov_state2=='risk_d'),2] <-  0
  out[which(nd$markov_state2=='zero'),1] <-  predict(trained_models_ols$zero,newdata = nd[which(nd$markov_state2=='zero'),])
  out[which(nd$markov_state2=='zero'),2] <-  0
  return(out)
}

predict_models_rf_step <- function(trained_models_rf,nd,step=1){
  out <- matrix(0,nrow(nd),2)
  colnames(out) <- c(paste('hat_ds',step,'_esc',sep=""),paste('hat_ds',step,'_deesc',sep=""))
  out[which(nd$markov_state2=='conflict'),1] <-  predict(trained_models_rf$conflict,data = nd[which(nd$markov_state2=='conflict'),])$predictions
  out[which(nd$markov_state2=='conflict'),2] <-  -nd[which(nd$markov_state2=='conflict'),]$ln_ged_best_sb
  out[which(nd$markov_state2=='risk_e'),1] <-  predict(trained_models_rf$risk_e,data = nd[which(nd$markov_state2=='risk_e'),])$predictions
  out[which(nd$markov_state2=='risk_e'),2] <-  -nd[which(nd$markov_state2=='risk_e'),]$ln_ged_best_sb
  out[which(nd$markov_state2=='risk_d'),1] <-  predict(trained_models_rf$risk_d,data = nd[which(nd$markov_state2=='risk_d'),])$predictions
  out[which(nd$markov_state2=='risk_d'),2] <-  0
  out[which(nd$markov_state2=='zero'),1] <-  predict(trained_models_rf$zero,data = nd[which(nd$markov_state2=='zero'),])$predictions
  out[which(nd$markov_state2=='zero'),2] <-  0
  return(out)
}

predict_weighted_ds <- function(probability_states,predicted_ds,step=1){
  weighted_ds <- probability_states[,1]*predicted_ds[,1]+
        probability_states[,2]*predicted_ds[,2]+
        probability_states[,3]*predicted_ds[,1]+
        probability_states[,4]*predicted_ds[,2]
  
out <- cbind(probability_states,predicted_ds,weighted_ds)
colnames(out) <- c('p_conflict','p_risk_d','p_risk_e','p_zero',colnames(predicted_ds),paste('hat_ds',step,'_weighted',sep=''))
return(out)
}

# 
# train <- cm2_train
# model_ivs <- vars
# target <- "ln_ged_best_sb_target"
# target_state <- 'lead_markov_state_target'
# test <- cm2_test

train_and_predict_vmm_fatalities <- function(train,model_ivs,test,target,target_state,rf_cont=F,rf_cat = F){
  if(!rf_cat){
  trained_logits <- train_models_logits(train,model_ivs,target_state=target_state)
  trans_zz <- 1 - predict(trained_logits$zero,newdata=test,type='r')
  trans_dz <- 1 - predict(trained_logits$risk_d,newdata=test,type='r')
  trans_ze <- predict(trained_logits$zero,newdata=test,type='r')
  trans_de <- predict(trained_logits$risk_d,newdata=test,type='r')
  trans_cd <- 1 - predict(trained_logits$conflict,newdata=test,type='r')
  trans_ed <- 1 - predict(trained_logits$risk_e,newdata=test,type='r')
  trans_cc <- predict(trained_logits$conflict,newdata=test,type='r')
  trans_ec <- predict(trained_logits$risk_e,newdata=test,type='r')
  }else{
    trained_rf_cat <- train_models_rf_one(train,model_ivs,target_state = target_state)
    trans_zz <- predict(trained_rf_cat$zero,data=test)$predictions[,'zero']
    trans_dz <- predict(trained_rf_cat$risk_d,data=test)$predictions[,'zero']
    trans_ze <- predict(trained_rf_cat$zero,data=test)$predictions[,'risk_e']
    trans_de <- predict(trained_rf_cat$risk_d,data=test)$predictions[,'risk_e']
    trans_cd <- predict(trained_rf_cat$conflict,data=test)$predictions[,'risk_d']
    trans_ed <- predict(trained_rf_cat$risk_e,data=test)$predictions[,'risk_d']
    trans_cc <- predict(trained_rf_cat$conflict,data=test)$predictions[,'conflict']
    trans_ec <-  predict(trained_rf_cat$risk_e,data=test)$predictions[,'conflict']
  }
  if(!rf_cont){
  trained_ols <- train_models_ols(train,model_ivs,target = target)
  predicted_cc <- predict(trained_ols$conflict_conflict,newdata=test)
  predicted_de <- predict(trained_ols$risk_d_risk_e,newdata=test)
  predicted_ec <- predict(trained_ols$risk_e_conflict,newdata=test)
  predicted_ze <- predict(trained_ols$zero_risk_e,newdata=test)
  predicted_cc[predicted_cc<0] <- 0
  predicted_de[predicted_de<0] <- 0
  predicted_ec[predicted_ec<0] <- 0
  predicted_ze[predicted_ze<0] <- 0
  }else{
    trained_rf <- train_models_rf_cont(train,model_ivs,target = target)
    predicted_cc <- predict(trained_rf$conflict_conflict,data=test)$predictions
    predicted_de <- predict(trained_rf$risk_d_risk_e,data=test)$predictions
    predicted_ec <- predict(trained_rf$risk_e_conflict,data=test)$predictions
    predicted_ze <- predict(trained_rf$zero_risk_e,data=test)$predictions
  }
  test <- test %>% mutate(
    p_lead_zero = case_when(markov_state2 == 'zero' ~ trans_zz,
                            markov_state2 == 'risk_d' ~trans_dz,
                            T ~ 0),
    p_lead_risk_e = case_when(markov_state2 == 'zero' ~ trans_ze,
                              markov_state2 == 'risk_d' ~ trans_de,
                              T ~ 0),
    p_lead_risk_d = case_when(markov_state2 == 'conflict' ~ trans_cd,
                              markov_state2 == 'risk_e' ~ trans_ed,
                              T ~ 0),
    p_lead_conflict = case_when(markov_state2 == 'conflict' ~ trans_cc,
                            markov_state2 == 'risk_e' ~ trans_ec,
                            T ~ 0),
    p_ds1_cc = predicted_cc,
    p_ds1_cd = 0,
    p_ds1_de = predicted_de,
    p_ds1_dz = 0,
    p_ds1_ec = predicted_ec,
    p_ds1_ed = 0,
    p_ds1_ze = predicted_ze,
    p_ds1_zz = 0,
    weighted_prediction = case_when(markov_state2 == 'conflict' ~ p_lead_conflict * p_ds1_cc + p_lead_risk_d * p_ds1_cd,
                                    markov_state2 == 'risk_d' ~ p_lead_risk_e * p_ds1_de + p_lead_zero * p_ds1_dz,
                                    markov_state2 == 'risk_e' ~ p_lead_conflict * p_ds1_ec + p_lead_risk_d * p_ds1_ed,
                                    markov_state2 == 'zero' ~ p_lead_risk_e * p_ds1_ze + p_lead_zero * p_ds1_zz)
  )
  
  return(test)
}


train_predict_vmm_steps <- function(train,model_ivs,test,step,use_multinom = F,use_rf=F,keep_data=T,return_only_wtd=F){
  target <- paste('delta_s',step,sep="")
  train <- train %>% select(all_of(c(target,model_ivs)),contains('markov')) %>% na.omit()
  if(step==1 & use_multinom){
    use_multinom <- F
  }
  if(use_rf){
    trained_rf <- train_models_rf_reg_step(train,model_ivs,step)
    pred_ds <-  predict_models_rf_step(trained_rf,test,step)
  }else{
  trained_ols <- train_models_ols_step(train,model_ivs,step)
  pred_ds <- foreach(i = 1:nrow(test),.combine=rbind) %do%
    predict_models_ols_step(trained_ols,test[i,],step)
  }
    if(use_multinom){
    trained_class <- train_models_multinom(train,model_ivs,step)
    prob_states <- foreach(i = 1:nrow(test),.combine=rbind) %do%
      p_row_from_multinom(trained_class,test[i,])
    }else if(use_rf){
      trained_class <- train_models_rf(train,model_ivs,step)
      prob_states <- foreach(i = 1:nrow(test),.combine=rbind) %do%
        p_row_from_rf(trained_class,test[i,])
  }else{
    trained_class <- train_models_logits(train,model_ivs)
    prob_states <- foreach(i = 1:nrow(test),.combine=rbind) %do%
      p_matrix_to_probs_steps_ahead(trained_class,test[i,],step)
  }
  if(return_only_wtd){
    return(predict_weighted_ds(prob_states,pred_ds,step)[,7])
  }
  if(!keep_data){
  return(predict_weighted_ds(prob_states,pred_ds,step))
  }else{
    return(bind_cols(test,as_tibble(predict_weighted_ds(prob_states,pred_ds,step))))
  }
  
  
}

