| Model                              | Included variable name   | Database variable name           | Transformations                               |
|:-----------------------------------|:-------------------------|:---------------------------------|:----------------------------------------------|
| fatalities002_pgm_conflict_treelag | 'ln_ged_sb_dep'          | 'ged2_pgm.ged_sb_best_sum_nokgi' | ["'ops.ln'", "'missing.replace_na'"]          |
| fatalities002_pgm_conflict_treelag | 'ged_gte_1'              | 'ged2_pgm.ged_sb_best_sum_nokgi' | ["'bool.gte'"]                                |
| fatalities002_pgm_conflict_treelag | 'treelag_1_sb'           | 'ged2_pgm.ged_sb_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_1_ns'           | 'ged2_pgm.ged_ns_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_1_os'           | 'ged2_pgm.ged_os_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_2_sb'           | 'ged2_pgm.ged_sb_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_2_ns'           | 'ged2_pgm.ged_ns_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |
| fatalities002_pgm_conflict_treelag | 'treelag_2_os'           | 'ged2_pgm.ged_os_best_sum_nokgi' | ["'spatial.treelag'", "'missing.replace_na'"] |