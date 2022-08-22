| Model name                                    | Description   | Dependent variable   | Queryset                               | Algorithm        | Long description   | PCA   |
|:----------------------------------------------|:--------------|:---------------------|:---------------------------------------|:-----------------|:-------------------|:------|
| fatalities002_pgm_baseline_lgbm               |               | ln_ged_sb_dep        | fatalities002_pgm_baseline             | LGBMRegressor    |                    | False |
| fatalities002_pgm_conflictlong_lgbm           |               | ln_ged_sb_dep        | fatalities002_pgm_conflictlong         | LGBMRegressor    |                    | False |
| fatalities002_pgm_conflictlong_hurdle_lgbm    |               | ln_ged_sb_dep        | fatalities002_pgm_conflictlong         | HurdleRegression |                    | False |
| fatalities002_pgm_escwa_drought_hurdle_lgbm   |               | ln_ged_sb_dep        | fatalities002_pgm_escwa_drought        | HurdleRegression |                    | False |
| fatalities002_pgm_escwa_drought_lgbm          |               | ln_ged_sb_dep        | fatalities002_pgm_escwa_drought        | LGBMRegressor    |                    | False |
| fatalities002_pgm_natsoc_hurdle_lgbm          |               | ln_ged_sb_dep        | fatalities002_pgm_natsoc               | HurdleRegression |                    | False |
| fatalities002_pgm_natsoc_lgbm                 |               | ln_ged_sb_dep        | fatalities002_pgm_natsoc               | LGBMRegressor    |                    | False |
| fatalities002_pgm_broad_hurdle_lgbm           |               | ln_ged_sb_dep        | fatalities002_pgm_broad                | HurdleRegression |                    | False |
| fatalities002_pgm_broad_lgbm                  |               | ln_ged_sb_dep        | fatalities002_pgm_broad                | LGBMRegressor    |                    | False |
| fatalities002_pgm_conflict_history_xgb        |               | ln_ged_sb_dep        | fatalities002_pgm_conflict_history     | XGBRegressor     |                    | False |
| fatalities002_pgm_conflict_treelag_hurdle     |               | ln_ged_sb_dep        | fatalities002_pgm_conflict_treelag     | HurdleRegression |                    | False |
| fatalities002_pgm_conflict_sptime_dist_hurdle |               | ln_ged_sb_dep        | fatalities002_pgm_conflict_sptime_dist | HurdleRegression |                    | False |