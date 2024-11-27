| Model                                  | Included variable name    | Database variable name                 | Transformations                                   |
|:---------------------------------------|:--------------------------|:---------------------------------------|:--------------------------------------------------|
| fatalities002_pgm_conflict_sptime_dist | 'ln_ged_sb_dep'           | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'ops.ln'", "'missing.replace_na'"]              |
| fatalities002_pgm_conflict_sptime_dist | 'ged_gte_1'               | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'bool.gte'"]                                    |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k1_ged_sb'   | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k1_ged_os'   | 'priogrid_month.ged_os_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k1_ged_ns'   | 'priogrid_month.ged_ns_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k10_ged_sb'  | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k10_ged_os'  | 'priogrid_month.ged_os_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k10_ged_ns'  | 'priogrid_month.ged_ns_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k001_ged_sb' | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k001_ged_os' | 'priogrid_month.ged_os_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_sptime_dist | 'sptime_dist_k001_ged_ns' | 'priogrid_month.ged_ns_best_sum_nokgi' | ["'spatial.sptime_dist'", "'missing.replace_na'"] |