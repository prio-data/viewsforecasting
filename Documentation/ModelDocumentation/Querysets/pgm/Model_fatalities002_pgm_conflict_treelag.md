| Model                              | Included variable name   | Database variable name                 | Transformations                               |
|:-----------------------------------|:-------------------------|:---------------------------------------|:----------------------------------------------|
| fatalities002_pgm_conflict_treelag | 'ln_ged_sb_dep'          | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'ops.ln'", "'missing.replace_na'"]          |
| fatalities002_pgm_conflict_treelag | 'ged_gte_1'              | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'bool.gte'"]                                |
| fatalities002_pgm_conflict_treelag | 'treelag_1_sb'           | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_1_ns'           | 'priogrid_month.ged_ns_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_1_os'           | 'priogrid_month.ged_os_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_2_sb'           | 'priogrid_month.ged_sb_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_2_ns'           | 'priogrid_month.ged_ns_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_2_os'           | 'priogrid_month.ged_os_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |