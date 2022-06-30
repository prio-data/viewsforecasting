| Model name                            | Dependent variable   | Queryset                            | Algorithm                     | PCA   |
|:--------------------------------------|:---------------------|:------------------------------------|:------------------------------|:------|
| fatalities002_baseline_rf             | ln_ged_sb_dep        | fatalities002_baseline              | XGBRFRegressor                | False |
| fat_conflicthistory_rf                | ln_ged_sb_dep        | fatalities002_conflict_history      | XGBRFRegressor                | False |
| fat_conflicthistory_gbm               | ln_ged_sb_dep        | fatalities002_conflict_history      | GradientBoostingRegressor     | False |
| fat_conflicthistory_hurdle_lgb        | ln_ged_sb_dep        | fatalities002_conflict_history      | HurdleRegression              | False |
| fat_conflicthistory_long_xgb          | ln_ged_sb_dep        | fatalities002_conflict_history_long | XGBRegressor                  | False |
| fat_vdem_hurdle_xgb                   | ln_ged_sb_dep        | hh_fatalities_vdem_short            | HurdleRegression              | False |
| fat_wdi_rf                            | ln_ged_sb_dep        | hh_fatalities_wdi_short             | XGBRFRegressor                | False |
| fatalities002_topics_rf               | ln_ged_sb_dep        | fatalities002_topics                | XGBRFRegressor                | False |
| fat_topics_rf                         | ln_ged_sb_dep        | hh_topic_model_short                | XGBRFRegressor                | False |
| fatalities002_topics_hurdle_lgb       | ln_ged_sb_dep        | fatalities002_topics                | HurdleRegression              | False |
| fat_topics_histgbm                    | ln_ged_sb_dep        | hh_topic_model_short                | HistGradientBoostingRegressor | False |
| fat_broad_xgb                         | ln_ged_sb_dep        | hh_broad                            | XGBRFRegressor                | False |
| fatalities002_greatest_hits_hurdle_rf | ln_ged_sb_dep        | fatalities002_greatest_hits         | HurdleRegression              | False |
| fat_hh20_hurdle_rf                    | ln_ged_sb_dep        | hh_20_features                      | HurdleRegression              | False |
| fat_hh20_hurdle_xgb                   | ln_ged_sb_dep        | hh_20_features                      | HurdleRegression              | False |
| fat_hh20_hurdle_lgb                   | ln_ged_sb_dep        | hh_20_features                      | HurdleRegression              | False |
| fat_all_pca3_xgb                      | ln_ged_sb_dep        | hh_all_features                     | XGBRegressor                  | True  |
| fatalities002_aquastat_rf             | ln_ged_sb_dep        | fatalities002_aquastat              | XGBRFRegressor                | False |
| fatalities002_faostat_rf              | ln_ged_sb_dep        | Fatalities002_faostat               | XGBRFRegressor                | False |
| fatalities002_faoprices_rf            | ln_ged_sb_dep        | Fatalities002_faoprices             | XGBRFRegressor                | False |
| fatalities002_imfweo_rf               | ln_ged_sb_dep        | Fatalities001_imfweo                | XGBRFRegressor                | False |
| fat_hh20_Markov_glm                   | ln_ged_sb_dep        | hh_20_features                      | Rscript                       | False |
| fat_hh20_Markov_rf                    | ln_ged_sb_dep        | hh_20_features                      | Rscript                       | False |