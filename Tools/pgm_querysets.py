# # Specifying querysets for use in Predicting Fatalities project
# ## pgm level
# 
# 

# ## Importing modules

# Basics
import numpy as np
from viewser import Queryset, Column


def report(df):
    print()
    print(f"A dataset with {len(df.columns)} columns, with "
          f"data between t {min(df.index.get_level_values(0))} "
          f"and {max(df.index.get_level_values(0))}. "
          f"({len(np.unique(df.index.get_level_values(1)))} units)"
          )
    return

# GED, baseline, ln versions of predictors
# log variables

# should I make the variables: .transform.bool.gte(1)

def get_pgm_querysets():
    
    
    qs_combo_escwa = (Queryset("escwa001_pgm_combo", "priogrid_month")
                      
                      .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.ops.ln()
                                  )
                              
                      .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                  )
                              
                      .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.bool.gte(1)
                                      .transform.temporal.time_since()
                                      .transform.temporal.decay(12)
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.bool.gte(25)
                                      .transform.temporal.time_since()
                                      .transform.temporal.decay(24)
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.bool.gte(1)
                                      .transform.temporal.time_since()
                                      .transform.temporal.decay(12)
                                      .transform.missing.replace_na()
                                  )
                              
#                      .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
#                                      .transform.missing.replace_na()
#                                      .transform.bool.gte(1)
#                                      .transform.temporal.time_since()
#                                      .transform.temporal.decay(24)
#                                      .transform.spatial.lag(1, 1, 0, 0)
#                                      .transform.missing.replace_na()
#                                  )
                      
#                      .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
#                                      .transform.missing.replace_na()
#                                      .transform.bool.gte(1)
#                                      .transform.temporal.time_since()
#                                      .transform.temporal.decay(24)
#                                      .transform.spatial.lag(1, 1, 0, 0)
#                                      .transform.missing.replace_na()
#                                  )
                              
                      .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("ln_ttime_mean", from_table="priogrid_year", from_column="ttime_mean")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("ln_gcp_mer", from_table="priogrid_year", from_column="gcp_mer")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("imr_mean", from_table="priogrid_year", from_column="imr_mean")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("ln_bdist3", from_table="priogrid_year", from_column="bdist3")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("ln_capdist", from_table="priogrid_year", from_column="capdist")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("mountains_mean", from_table="priogrid_year", from_column="mountains_mean")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("dist_diamsec", from_table="priogrid", from_column="dist_diamsec_s_wgs")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
                      .with_column(Column("dist_petroleum", from_table="priogrid", from_column="dist_petroleum_s_wgs")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                              
#                      .with_column(Column("agri_ih", from_table="priogrid_year", from_column="agri_ih")
#                                      .transform.missing.fill()
#                                      .transform.missing.replace_na()
#                                  )
                              
#                      .with_column(Column("barren_ih", from_table="priogrid_year", from_column="barren_ih")
#                                      .transform.missing.fill()
#                                      .transform.missing.replace_na()
#                                  )
                              
#                      .with_column(Column("forest_ih", from_table="priogrid_year", from_column="forest_ih")
#                                      .transform.missing.fill()
#                                      .transform.missing.replace_na()
#                                  )
                              
#                      .with_column(Column("pasture_ih", from_table="priogrid_year", from_column="pasture_ih")
#                                      .transform.missing.fill()
#                                      .transform.missing.replace_na()
#                                  )
                              
#                      .with_column(Column("savanna_ih", from_table="priogrid_year", from_column="savanna_ih")
#                                      .transform.missing.fill()
#                                      .transform.missing.replace_na()
#                                  )
#                              
#                      .with_column(Column("shrub_ih", from_table="priogrid_year", from_column="shrub_ih")
#                                      .transform.missing.fill()
#                                      .transform.missing.replace_na()
#                                  )
#                              
#                      .with_column(Column("urban_ih", from_table="priogrid_year", from_column="urban_ih")
#                                      .transform.missing.fill()
#                                      .transform.missing.replace_na()
#                                  )
                      
                      .with_column(Column("greq_1_excluded", from_table="priogrid_year", from_column="excluded")
                                      .transform.bool.gte(1)
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                  )
                      
                      .with_column(Column("count_moder_drought_prev10", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="count_moder_drought_prev10")
                                     .transform.missing.replace_na(0)
                                  )
         
                      .with_column(Column("cropprop", from_table="hack_temp_escwa_pgm_pgm", from_column="cropprop")
                                     .transform.missing.replace_na(0)
                                  )
                        
                      .with_column(Column("growseasdummy", from_table="hack_temp_escwa_pgm_pgm", from_column="growseasdummy")
                                     .transform.missing.replace_na(0)
                                  )
                                            
#                      .with_column(Column("gwmean", from_table="hack_temp_escwa_pgm_pgm", from_column="gwmean")
#                                     .transform.missing.fill()
#                                  )
                                                
#                      .with_column(Column("knn_dummy", from_table="hack_temp_escwa_pgm_pgm", from_column="knn_dummy")
#                                     .transform.missing.fill()
#                                  )

                      .with_column(Column("spei1_gs_prev10", from_table="hack_temp_escwa_pgm_pgm", from_column="spei1_gs_prev10")
                                     .transform.missing.replace_na(0)
                                  )

                      .with_column(Column("spei1_gs_prev10_anom", from_table="hack_temp_escwa_pgm_pgm", from_column="spei1_gs_prev10_anom")
                                     .transform.missing.replace_na(0)
                                  )

                      .with_column(Column("spei1_gsm_cv_anom", from_table="hack_temp_escwa_pgm_pgm", from_column="spei1_gsm_cv_anom")
                                     .transform.missing.replace_na(0)
                                  )

                      .with_column(Column("spei1_gsm_detrend", from_table="hack_temp_escwa_pgm_pgm", from_column="spei1_gsm_detrend")
                                   .transform.missing.replace_na(0)
                                  )

                      .with_column(Column("spei1gsy_lowermedian_count", from_table="hack_temp_escwa_pgm_pgm", from_column="spei1gsy_lowermedian_count")
                                     .transform.missing.replace_na(0)
                                  )

                      .with_column(Column("spei_48_detrend", from_table="hack_temp_escwa_pgm_pgm", from_column="spei_48_detrend")
                                     .transform.missing.replace_na(0)
                                  )

                      .with_column(Column("tlag1_dr_mod_gs", from_table="hack_temp_escwa_pgm_pgm", from_column="tlag1_dr_mod_gs")
                                     .transform.missing.replace_na(0)
                                  )
                      
                      .with_column(Column("tlag1_dr_moder_gs", from_table="hack_temp_escwa_pgm_pgm", from_column="tlag1_dr_moder_gs")
                                     .transform.missing.replace_na(0)
                                  )
                      
                      .with_column(Column("tlag1_dr_sev_gs", from_table="hack_temp_escwa_pgm_pgm", from_column="tlag1_dr_sev_gs")
                                     .transform.missing.replace_na(0)
                                  )
                      
                      .with_column(Column("tlag1_spei1_gsm", from_table="hack_temp_escwa_pgm_pgm", from_column="tlag1_spei1_gsm")
                                     .transform.missing.replace_na(0)
                                  )
                      
                      .with_column(Column("tlag_12_crop_sum", from_table="hack_temp_escwa_pgm_pgm", from_column="tlag_12_crop_sum")
                                     .transform.missing.replace_na(0)
                                  )
                      
                      .with_column(Column("tlag_12_harvarea_maincrops", from_table="hack_temp_escwa_pgm_pgm", from_column="tlag_12_harvarea_maincrops")
                                     .transform.missing.replace_na(0)
                                  )
                      
                      .with_column(Column("tlag_12_irr_maincrops", from_table="hack_temp_escwa_pgm_pgm", from_column="tlag_12_irr_maincrops")
                                     .transform.missing.replace_na(0)
                                  )
                      
                      .with_column(Column("tlag_12_rainf_maincrops", from_table="hack_temp_escwa_pgm_pgm", from_column="tlag_12_rainf_maincrops")
                                     .transform.missing.replace_na(0)
                                  )
                      
                      .with_theme("escwa")
                      .describe("""Fatalities, escwa combined, pgm level
    
                                  Predicting number of fatalities with features from the escwa combined themes
                                  
                                  """)
                        )
    
    data = qs_combo_escwa.publish().fetch()
    
    report(data)
    
    qs_climate_extremes_escwa = (Queryset("escwa001_pgm_extremes", "priogrid_month")
                                 
                                 .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                              .transform.missing.replace_na()
                                              .transform.ops.ln()
                                             )
                                 
                                 .with_column(Column("r30mm", from_table="climate_year_pgy", from_column="r30mm")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tn10p", from_table="climate_year_pgy", from_column="tn10p")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("r10mm", from_table="climate_year_pgy", from_column="r10mm")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("txm", from_table="climate_year_pgy", from_column="txm")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tmm", from_table="climate_year_pgy", from_column="tmm")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tmge5", from_table="climate_year_pgy", from_column="tmge5")
                                              .transform.missing.replace_na(0)
                                             ) 
                                 
                                 .with_column(Column("ice_days", from_table="climate_year_pgy", from_column="ice_days")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("txge30", from_table="climate_year_pgy", from_column="txge30")
                                              .transform.missing.replace_na(0)
                                             )
                                 .with_column(Column("tnltm20", from_table="climate_year_pgy", from_column="tnltm20")
                                              .transform.missing.replace_na(0)
                                             )
                                 .with_column(Column("tnm", from_table="climate_year_pgy", from_column="tnm")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("spei12", from_table="tbl_ca543climate_pgm", from_column="spei")
                                              .transform.missing.fill()
                                              .transform.temporal.tlag(12)
                                              .transform.missing.fill()
                                              .transform.missing.replace_na()
                                             )
                                 
                                 .with_column(Column("r20mm", from_table="climate_year_pgy", from_column="r20mm")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tmlt10", from_table="climate_year_pgy", from_column="tmlt10")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("consecutive_dry_days_index_per_time_period", from_table="climate_year_pgy", from_column="consecutive_dry_days_index_per_time_period")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("number_of_cdd_periods_with_more_than_5days_per_time_period", from_table="climate_year_pgy", from_column="number_of_cdd_periods_with_more_than_5days_per_time_period")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tnltm2", from_table="climate_year_pgy", from_column="tnltm2")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("su", from_table="climate_year_pgy", from_column="su")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tx90p", from_table="climate_year_pgy", from_column="tx90p")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("txx", from_table="climate_year_pgy", from_column="txx")
                                              .transform.missing.replace_na(0)
                                             )
                                 
#                                 .with_column(Column("spei6", from_table="tbl_ca543climate_pgm", from_column="spei")
#                                              .transform.missing.fill()
#                                              .transform.temporal.tlag(6)
#                                              .transform.missing.fill()
#                                              .transform.missing.replace_na()
#                                             )
                                 
                                 .with_column(Column("tmge10", from_table="climate_year_pgy", from_column="tmge10")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tr", from_table="climate_year_pgy", from_column="tr")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("rx5day", from_table="climate_year_pgy", from_column="rx5day")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tn90p", from_table="climate_year_pgy", from_column="tn90p")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("spei3", from_table="tbl_ca543climate_pgm", from_column="spei")
                                              .transform.missing.fill()
                                              .transform.temporal.tlag(3)
                                              .transform.missing.fill()
                                              .transform.missing.replace_na()
                                             )
                                 
                                 .with_column(Column("txn", from_table="climate_year_pgy", from_column="txn")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("rx7day", from_table="climate_year_pgy", from_column="rx7day")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("txgt50p", from_table="climate_year_pgy", from_column="txgt50p")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("txge35", from_table="climate_year_pgy", from_column="txge35")
                                              .transform.missing.replace_na(0)
                                             )          
                                 .with_column(Column("tx10p", from_table="climate_year_pgy", from_column="tx10p")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("consecutive_wet_days_index_per_time_period", from_table="climate_year_pgy", from_column="consecutive_wet_days_index_per_time_period")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("number_of_cwd_periods_with_more_than_5days_per_time_period", from_table="climate_year_pgy", from_column="number_of_cwd_periods_with_more_than_5days_per_time_period")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("prcptot", from_table="climate_year_pgy", from_column="prcptot")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("txn", from_table="climate_year_pgy", from_column="txn")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("fd", from_table="climate_year_pgy", from_column="fd")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tnn", from_table="climate_year_pgy", from_column="tnn")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tnlt2", from_table="climate_year_pgy", from_column="tnlt2")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("dtr", from_table="climate_year_pgy", from_column="dtr")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_column(Column("tmlt5", from_table="climate_year_pgy", from_column="tmlt5")
                                              .transform.missing.replace_na(0)
                                             )
                                 
                                 .with_theme("escwa")
                                 .describe("""Fatalities, escwa climate extremes, pgm level Predicting number of fatalities with features from the escwa climate extreme themes""")
                                )
    
    data = qs_climate_extremes_escwa.publish().fetch()
    
    report(data)
    
    qs_naturalsocial_escwa = (Queryset("escwa001_pgm_naturalsocial", "priogrid_month")
                              .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.ops.ln()
                                      )
                              
                              .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      )
                              
                              .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.bool.gte(1)
                                      .transform.temporal.time_since()
                                      .transform.temporal.decay(24)
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.bool.gte(25)
                                      .transform.temporal.time_since()
                                      .transform.temporal.decay(24)
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.bool.gte(1)
                                      .transform.temporal.time_since()
                                      .transform.temporal.decay(24)
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.bool.gte(1)
                                      .transform.temporal.time_since()
                                      .transform.temporal.decay(24)
                                      .transform.spatial.lag(1, 1, 0, 0)
                                      .transform.missing.replace_na()
                                      )
                              .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                      .transform.missing.replace_na()
                                      .transform.bool.gte(1)
                                      .transform.temporal.time_since()
                                      .transform.temporal.decay(24)
                                      .transform.spatial.lag(1, 1, 0, 0)
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("ln_ttime_mean", from_table="priogrid_year", from_column="ttime_mean")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("ln_gcp_mer", from_table="priogrid_year", from_column="gcp_mer")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("imr_mean", from_table="priogrid_year", from_column="imr_mean")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("ln_bdist3", from_table="priogrid_year", from_column="bdist3")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("ln_capdist", from_table="priogrid_year", from_column="capdist")
                                      .transform.ops.ln()
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("mountains_mean", from_table="priogrid_year", from_column="mountains_mean")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("dist_diamsec", from_table="priogrid", from_column="dist_diamsec_s_wgs")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("dist_petroleum", from_table="priogrid", from_column="dist_petroleum_s_wgs")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("agri_ih", from_table="priogrid_year", from_column="agri_ih")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("barren_ih", from_table="priogrid_year", from_column="barren_ih")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("forest_ih", from_table="priogrid_year", from_column="forest_ih")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("pasture_ih", from_table="priogrid_year", from_column="pasture_ih")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("savanna_ih", from_table="priogrid_year", from_column="savanna_ih")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("shrub_ih", from_table="priogrid_year", from_column="shrub_ih")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("urban_ih", from_table="priogrid_year", from_column="urban_ih")
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_column(Column("greq_1_excluded", from_table="priogrid_year", from_column="excluded")
                                      .transform.bool.gte(1)
                                      .transform.missing.fill()
                                      .transform.missing.replace_na()
                                      )
                              
                              .with_theme("escwa")
                              .describe("""Fatalities, escwa natural social, pgm level Predicting number of fatalities with features from the escwa natural social themes""")
                              
                              )
    
    data = qs_naturalsocial_escwa.publish().fetch()
    report(data)
    
    ##
    
    qs_drought_escwa = (Queryset("escwa001_pgm_drought", "priogrid_month")

                        # target variable
                        .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.ops.ln()
                                     )
  
                        .with_column(Column("count_moder_drought_prev10", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="count_moder_drought_prev10")
                                     .transform.missing.replace_na(0)
                                     )
         
                        .with_column(Column("cropprop", from_table="hack_temp_escwa_pgm_pgm", from_column="cropprop")
                                     .transform.missing.replace_na(0)
                                     )
                        
                        .with_column(Column("growseasdummy", from_table="hack_temp_escwa_pgm_pgm", from_column="growseasdummy")
                                     .transform.missing.replace_na(0)
                                     )
                                            
#                        .with_column(Column("gwmean", from_table="hack_temp_escwa_pgm_pgm",
#                                            from_column="gwmean")
#                                     .transform.missing.fill()
#                                     )
                                                
#                        .with_column(Column("knn_dummy", from_table="hack_temp_escwa_pgm_pgm",
#                                            from_column="knn_dummy")
#                                     .transform.missing.fill()
#                                     )

                        .with_column(Column("spei1_gs_prev10", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gs_prev10")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gs_prev10_anom", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gs_prev10_anom")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gsm_cv_anom", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gsm_cv_anom")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gsm_detrend", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gsm_detrend")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1gsy_lowermedian_count", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1gsy_lowermedian_count")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei_48_detrend", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei_48_detrend")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_mod_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_mod_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_moder_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_moder_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_sev_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_sev_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_spei1_gsm", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_spei1_gsm")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_crop_sum", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_crop_sum")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_harvarea_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_harvarea_maincrops")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_irr_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_irr_maincrops")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_rainf_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_rainf_maincrops")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_theme("escwa")
                        .describe("""Fatalities, escwa drought, pgm level
    
                                  Predicting number of fatalities with features from the escwa drought themes
                                  
                                  """)
                        )

    data = qs_drought_escwa.publish().fetch()
    
    report(data)
    
    ###########
    
    
                         


    ###########

    qs_baseline = (Queryset("fatalities002_pgm_baseline", "priogrid_month")

                   # target variable
                   .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.ops.ln()
                                )

                   # timelag 0 of target variable
                   .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   # Decay functions
                   # sb
                   .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(25)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )
                   # os
                   .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   # Spatial lag
                   .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   # Spatial lag decay
                   .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   # Log population as control
                   .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                )

                   .with_theme("fatalities")
                   .describe("""Fatalities conflict history, cm level
    
                             Predicting ln(fatalities) using conflict predictors, ultrashort
    
                            """)
                   )

    data = qs_baseline.publish().fetch()

    report(data)

    # conflictlong

    # With acled2_cm version, ln versions of predictors
    # log variables

    qs_conflict_long = (Queryset("fatalities002_pgm_conflictlong", "priogrid_month")

                        # target variable
                        .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.ops.ln()
                                     )

                        # timelags 0 of conflict variables, ged_best versions

                        .with_column(Column("ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.fill()
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("ged_os", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                                     .transform.missing.fill()
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("ged_ns", from_table="ged2_pgm", from_column="ged_ns_best_sum_nokgi")
                                     .transform.missing.fill()
                                     .transform.missing.replace_na()
                                     )

                        # Spatial lag
                        .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm",
                                            from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(1)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(24)
                                     .transform.spatial.lag(1, 1, 0, 0)
                                     .transform.missing.replace_na()
                                     )

                        # Spatial lag decay
                        .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm",
                                            from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(1)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(24)
                                     .transform.spatial.lag(1, 1, 0, 0)
                                     .transform.missing.replace_na()
                                     )

                        # Decay functions
                        # sb
                        .with_column(Column("decay_ged_sb_5", from_table="ged2_pgm",
                                            from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(5)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm",
                                            from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(25)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_sb_100", from_table="ged2_pgm",
                                            from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(100)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_sb_500", from_table="ged2_pgm",
                                            from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(500)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        # os
                        .with_column(Column("decay_ged_os_5", from_table="ged2_pgm",
                                            from_column="ged_os_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(5)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_os_25", from_table="ged2_pgm",
                                            from_column="ged_os_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(25)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_os_100", from_table="ged2_pgm",
                                            from_column="ged_os_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(100)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_os_500", from_table="ged2_pgm",
                                            from_column="ged_os_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(500)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )
                        # ns
                        .with_column(Column("decay_ged_ns_5", from_table="ged2_pgm",
                                            from_column="ged_ns_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(5)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_ns_25", from_table="ged2_pgm",
                                            from_column="ged_ns_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(25)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_ns_100", from_table="ged2_pgm",
                                            from_column="ged_ns_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(100)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_ns_500", from_table="ged2_pgm",
                                            from_column="ged_ns_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(500)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        # Log population as control
                        .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                                     .transform.ops.ln()
                                     .transform.missing.fill()
                                     .transform.missing.replace_na()
                                     )

                        .with_theme("fatalities")
                        .describe("""fatalities longer conflict history, pgm level
    
                                  Predicting ln(ged_best_sb) using conflict predictors, longer version
    
                                  """)
                        )

    data = qs_conflict_long.publish().fetch()

    report(data)

    # ESCWA drought vulnerability

    qs_escwa_drought = (Queryset("fatalities002_pgm_escwa_drought", "priogrid_month")

                        # target variable
                        .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.ops.ln()
                                     )

                        # timelag 0 of target variable
                        .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.ops.ln()
                                     )

                        .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm",
                                            from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(1)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_os_1", from_table="ged2_pgm",
                                            from_column="ged_os_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(1)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_ns_1", from_table="ged2_pgm",
                                            from_column="ged_ns_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(1)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("greq_1_excluded", from_table="priogrid_year", from_column="excluded")
                                     .transform.bool.gte(1)
                                     .transform.missing.fill()
                                     )

                        .with_column(Column("pgd_nlights_calib_mean", from_table="priogrid_year",
                                            from_column="nlights_calib_mean")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("wdi_nv_agr_totl_kd", from_table="wdi_cy", from_column="wdi_nv_agr_totl_kd")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("pgd_imr_mean", from_table="priogrid_year", from_column="imr_mean")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                                     .transform.missing.replace_na(0)
                                     .transform.ops.ln()
                                     )

                        .with_column(Column("ln_pgd_ttime_mean", from_table="priogrid_year", from_column="ttime_mean")
                                     .transform.missing.replace_na(0)
                                     .transform.ops.ln()
                                     )

                        .with_column(Column("pgd_urban_ih", from_table="priogrid_year", from_column="urban_ih")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("count_moder_drought_prev10", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="count_moder_drought_prev10")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("cropprop", from_table="hack_temp_escwa_pgm_pgm", from_column="cropprop")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("growseasdummy", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="growseasdummy")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gs_prev10", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gs_prev10")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gs_prev10_anom", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gs_prev10_anom")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gsm_cv_anom", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gsm_cv_anom")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gsm_detrend", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gsm_detrend")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1gsy_lowermedian_count", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1gsy_lowermedian_count")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei_48_detrend", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei_48_detrend")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_mod_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_mod_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_moder_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_moder_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_sev_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_sev_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_spei1_gsm", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_spei1_gsm")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_crop_sum", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_crop_sum")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_harvarea_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_harvarea_maincrops")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_irr_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_irr_maincrops")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_rainf_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_rainf_maincrops")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_theme("fatalities")
                        .describe("""Fatalities, escwa drought and vulnerability, pgm level
    
                                  Predicting number of fatalities with features from the escwa drought and 
                                  vulnerability themes
                                  
                                  """)
                        )

    data = qs_escwa_drought.publish().fetch()

    report(data)

    # NATSOC

    # GED, baseline, ln versions of predictors
    # log variables

    qs_natsoc = (Queryset("fatalities002_pgm_natsoc", "priogrid_month")

                 # target variable
                 .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.ops.ln()
                              )

                 # timelag 0 of target variable
                 .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              )

                 # Decay functions
                 # sb
                 .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(25)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.missing.replace_na()
                              )

                 # os
                 .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.missing.replace_na()
                              )

                 # Spatial lag
                 .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.spatial.lag(1, 1, 0, 0)
                              .transform.missing.replace_na()
                              )

                 # Spatial lag decay
                 .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm",
                                     from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.spatial.lag(1, 1, 0, 0)
                              .transform.missing.replace_na()
                              )

                 # Log population as control
                 .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 # from priogrid table:

                 .with_column(Column("ln_ttime_mean", from_table="priogrid_year", from_column="ttime_mean")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("ln_gcp_mer", from_table="priogrid_year", from_column="gcp_mer")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("imr_mean", from_table="priogrid_year", from_column="imr_mean")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("ln_bdist3", from_table="priogrid_year", from_column="bdist3")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("ln_capdist", from_table="priogrid_year", from_column="capdist")
                              .transform.ops.ln()
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("mountains_mean", from_table="priogrid_year", from_column="mountains_mean")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("dist_diamsec", from_table="priogrid", from_column="dist_diamsec_s_wgs")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("dist_petroleum", from_table="priogrid", from_column="dist_petroleum_s_wgs")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("agri_ih", from_table="priogrid_year", from_column="agri_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("barren_ih", from_table="priogrid_year", from_column="barren_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("forest_ih", from_table="priogrid_year", from_column="forest_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("pasture_ih", from_table="priogrid_year", from_column="pasture_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("savanna_ih", from_table="priogrid_year", from_column="savanna_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("shrub_ih", from_table="priogrid_year", from_column="shrub_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("urban_ih", from_table="priogrid_year", from_column="urban_ih")
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_column(Column("greq_1_excluded", from_table="priogrid_year", from_column="excluded")
                              .transform.bool.gte(1)
                              .transform.missing.fill()
                              .transform.missing.replace_na()
                              )

                 .with_theme("fatalities")
                 .describe("""Fatalities natural and social geography, pgm level
     
                           Predicting ln(fatalities) using natural and social geography features
    
                           """)
                 )

    data = qs_natsoc.publish().fetch()

    report(data)

    # Broad

    # Some tree variable definitions:
    thetacrit_spatial = 0.7
    return_values = 'distances'
    n_nearest = 1
    power = 0.0

    qs_broad = (Queryset("fatalities002_pgm_broad", "priogrid_month")

                # target variable
                .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.ops.ln()
                             )

                # timelags 0 of conflict variables, ged_best versions

                .with_column(Column("ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("ged_os", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("ged_ns", from_table="ged2_pgm", from_column="ged_ns_best_sum_nokgi")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                # Spatial lag
                .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(24)
                             .transform.spatial.lag(1, 1, 0, 0)
                             .transform.missing.replace_na()
                             )

                # Decay functions
                # sb
                .with_column(Column("decay_ged_sb_5", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(5)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(12)
                             .transform.missing.replace_na()
                             )
                # os
                .with_column(Column("decay_ged_os_5", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(5)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(12)
                             .transform.missing.replace_na()
                             )

                # ns
                .with_column(Column("decay_ged_ns_5", from_table="ged2_pgm", from_column="ged_ns_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(5)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(12)
                             .transform.missing.replace_na()
                             )

                # Trees

                .with_column(Column("treelag_1_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.treelag(thetacrit_spatial, 1)
                             )

                .with_column(Column("treelag_2_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.treelag(thetacrit_spatial, 2)
                             )
                # sptime

                # continuous, sptime_dist, nu=1
                .with_column(Column("sptime_dist_k1_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                             )

                .with_column(Column("sptime_dist_k1_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                             )

                .with_column(Column("sptime_dist_k1_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                             )

                # From natsoc
                .with_column(Column("ln_ttime_mean", from_table="priogrid_year", from_column="ttime_mean")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("ln_bdist3", from_table="priogrid_year", from_column="bdist3")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("ln_capdist", from_table="priogrid_year", from_column="capdist")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("dist_diamsec", from_table="priogrid", from_column="dist_diamsec_s_wgs")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_column(Column("imr_mean", from_table="priogrid_year", from_column="imr_mean")
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                # From drought
                .with_column(Column("tlag1_dr_mod_gs", from_table="hack_temp_escwa_pgm_pgm",
                                    from_column="tlag1_dr_mod_gs")
                             .transform.missing.replace_na(0)
                             )

                .with_column(Column("spei1_gs_prev10_anom", from_table="hack_temp_escwa_pgm_pgm",
                                    from_column="spei1_gs_prev10_anom")
                             .transform.missing.replace_na(0)
                             )

                .with_column(Column("tlag_12_crop_sum", from_table="hack_temp_escwa_pgm_pgm",
                                    from_column="tlag_12_crop_sum")
                             .transform.missing.replace_na(0)
                             )

                .with_column(Column("spei1gsy_lowermedian_count", from_table="hack_temp_escwa_pgm_pgm",
                                    from_column="spei1gsy_lowermedian_count")
                             .transform.missing.replace_na(0)
                             )

                # Log population as control
                .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             .transform.missing.replace_na()
                             )

                .with_theme("fatalities")
                .describe("""fatalities broad model, pgm level
    
                          Predicting ln(ged_best_sb), broad model
    
                          """)
                )

    data = qs_broad.publish().fetch()

    report(data)

    # Paola's conflict history

    # Define query for pgm level, attribute unique name to queryset

    qs_conf_history = (Queryset("fatalities002_pgm_conflict_history", "priogrid_month")

                       # target variable
                       .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       # timelags 1-12 of target variable
                       .with_column(Column("ln_ged_sb_tlag_1", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(1)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_2", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(2)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_3", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(3)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_4", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(4)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_5", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(5)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_6", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(6)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_7", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(7)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_8", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(8)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_9", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(9)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_10", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(10)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_11", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(11)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_12", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       # 12-month decay dummy of target variable
                       .with_column(Column("ln_ged_sb_decay_12_time_since", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.temporal.decay(12)
                                    .transform.bool.gte(1)
                                    .transform.missing.fill()
                                    )

                       # (1,1) spatially-lagged 1-timelagged target variable
                       .with_column(Column("ln_ged_sb_tlag_1_splag_1", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(1)
                                    .transform.spatial.lag(1, 1, 0, 0)
                                    .transform.missing.fill()
                                    )

                       # (1,1) spatially-lagged target variable
                       .with_column(Column("ln_ged_sb_splag_1", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.spatial.lag(1, 1, 0, 0)
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       # time-lagged by 1 independent variables
                       .with_column(Column("ln_ged_ns_tlag_1", from_table="ged2_pgm",
                                           from_column="ged_ns_best_count_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(1)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_os_tlag_1", from_table="ged2_pgm",
                                           from_column="ged_os_best_count_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(1)
                                    .transform.missing.fill()
                                    )

                       # 12-month decay dummy of independent variables
                       .with_column(Column("ln_ged_ns_decay_12_time_since", from_table="ged2_pgm",
                                           from_column="ged_ns_best_count_nokgi")
                                    .transform.temporal.decay(12)
                                    .transform.bool.gte(1)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_os_decay_12_time_since", from_table="ged2_pgm",
                                           from_column="ged_os_best_count_nokgi")
                                    .transform.temporal.decay(12)
                                    .transform.bool.gte(1)
                                    .transform.missing.fill()
                                    )

                       # (1,1) spatially-lagged independent variables
                       .with_column(Column("ln_ged_ns_splag_1", from_table="ged2_pgm",
                                           from_column="ged_ns_best_count_nokgi")
                                    .transform.spatial.lag(1, 1, 0, 0)
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_os_splag_1", from_table="ged2_pgm",
                                           from_column="ged_os_best_count_nokgi")
                                    .transform.spatial.lag(1, 1, 0, 0)
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       # (1,1) spatially-lagged 1-timelagged independent variables
                       .with_column(Column("ln_ged_ns_tlag_1_splag_1", from_table="ged2_pgm",
                                           from_column="ged_ns_best_count_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(1)
                                    .transform.spatial.lag(1, 1, 0, 0)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_os_tlag_1_splag_1", from_table="ged2_pgm",
                                           from_column="ged_os_best_count_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(1)
                                    .transform.spatial.lag(1, 1, 0, 0)
                                    .transform.missing.fill()
                                    )

                       # moving average and sum
                       .with_column(Column("mov_avg_6_ged_best_sb", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.moving_average(6)
                                    )

                       .with_column(Column("mov_avg_12_ged_best_sb", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.moving_average(12)
                                    )

                       .with_column(Column("mov_avg_36_ged_best_sb", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.moving_average(36)
                                    )

                       .with_column(Column("mov_sum_6_ged_best_sb", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.moving_sum(6)
                                    )

                       .with_column(Column("mov_sum_12_ged_best_sb", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.moving_sum(12)
                                    )

                       .with_column(Column("mov_sum_36_ged_best_sb", from_table="ged2_pgm",
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.moving_sum(36)
                                    )

                       .with_theme("fatalities")
                       .describe("""Fatalities conflict history
    
                                 Predicting ln(fatalities) using conflict predictors
    
                                 """)
                       )

    data = qs_conf_history.publish().fetch()

    report(data)

    # Conflict_treelag_d_1_d_2

    qs_treelag = (Queryset("fatalities002_pgm_conflict_treelag", "priogrid_month")
                  # target variable
                  .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.ops.ln()
                               )

                  # dichotomous version, primarily for downsampling....
                  .with_column(Column("ged_gte_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                               .transform.bool.gte(1)
                               )

                  .with_column(Column("treelag_1_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 1)
                               )

                  .with_column(Column("treelag_1_ns", from_table="ged2_pgm", from_column="ged_ns_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 1)
                               )

                  .with_column(Column("treelag_1_os", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 1)
                               )

                  .with_column(Column("treelag_2_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 2)
                               )

                  .with_column(Column("treelag_2_ns", from_table="ged2_pgm", from_column="ged_ns_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 2)
                               )

                  .with_column(Column("treelag_2_os", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.treelag(thetacrit_spatial, 2)
                               )
                  )

    data = qs_treelag.publish().fetch()

    report(data)

    # Spacetime distances

    qs_sptime_dist = (Queryset("fatalities002_pgm_conflict_sptime_dist", "priogrid_month")
                      # target variable
                      .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.ops.ln()
                                   )

                      # dichotomous version, primarily for downsampling....
                      .with_column(Column("ged_gte_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                   .transform.bool.gte(1)
                                   )

                      # continuous, sptime_dist, nu=1
                      .with_column(Column("sptime_dist_k1_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k10_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k10_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k10_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k01_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )

                      .with_column(Column("sptime_dist_k01_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )

                      .with_column(Column("sptime_dist_k01_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )
                      )

    data = qs_sptime_dist.publish().fetch()

    report(data)
    


    # Full protest model + political institutions III + economic development (country level)

    qs_protest_full = (Queryset("fatalities003_protest_full_elect_econ_national", "priogrid_month")

           # target variable
           .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.ops.ln()
                        )

           # timelag 0 of target variable
           .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )

           # Decay functions
           # sb
           .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )

           .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(25)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )
           # os
           .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )

           # Spatial lag
           .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.spatial.lag(1, 1, 0, 0)
                        .transform.missing.replace_na()
                        )

           # Spatial lag decay
           .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm",
                               from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.spatial.lag(1, 1, 0, 0)
                        .transform.missing.replace_na()
                        )

           # Log population as control
           .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        .transform.missing.replace_na()
                        )




          # Moving average over 24 months
          .with_column(Column("mov_avg_12_ged_best_sb", from_table = "ged2_pgm", from_column = "ged_sb_best_sum_nokgi")
                             .transform.ops.ln()
                             .transform.missing.replace_na()
                             .transform.temporal.moving_average(24)
                             .transform.missing.fill()
                            )

          ## PROTEST FEATURES - Dynamic Local

          .with_column(Column("decay_ts_6_acled_prex_dummy", from_table = "acled2_pgm", from_column = "acled_c3_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_acled_prpe_dummy", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prin_dummy", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prri_dummy", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prpe_dummy", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prex_dummy", from_table = "acled2_pgm", from_column = "acled_c3_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prin_dummy", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prri_dummy", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          # protest with excessive violence against protester (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prex_count", from_table = "acled2_pgm", from_column = "acled_c3_count") 
                             .transform.missing.replace_na()
                            )
          # peaceful protest (interaction codes: 60, 66, or 67.)
          .with_column(Column("acled_prpe_count", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                            )
          # protest with intervention (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prin_count", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                            )
          # protest with riots (interaction codes: inter 1 or 2 has 5)
          .with_column(Column("acled_prri_count", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                            )

          ## PROTEST FEATURES - Dynamic national

          .with_column(Column("decay_ts_6_acled_prex_dummy_cm", from_table = "acled2_cm", from_column = "acled_c3_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_acled_prpe_dummy_cm", from_table = "acled2_cm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prin_dummy_cm", from_table = "acled2_cm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prri_dummy_cm", from_table = "acled2_cm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          # protest with excessive violence against protester (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prex_count_cm", from_table = "acled2_cm", from_column = "acled_c3_count") 
                             .transform.missing.replace_na()
                            )
          # peaceful protest (interaction codes: 60, 66, or 67.)
          .with_column(Column("acled_prpe_count_cm", from_table = "acled2_cm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                            )
          # protest with intervention (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prin_count_cm", from_table = "acled2_cm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                            )
          # protest with riots (interaction codes: inter 1 or 2 has 5)
          .with_column(Column("acled_prri_count_cm", from_table = "acled2_cm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                            )

          # population
          .with_column(Column("wdi_sp_pop_totl", from_table = "wdi_cy", from_column = "wdi_sp_pop_totl")
                             .transform.missing.fill()
                             .transform.missing.extrapolate()
                             .transform.missing.replace_na()
                            )

          ### ECONOMIC DEVELOPMENT, Country level
          .with_column(Column("wdi_ny_gdp_pcap_kd", from_table = "wdi_cy", from_column = "wdi_ny_gdp_pcap_kd")
                             .transform.missing.fill()
                            )
#          .with_column(Column("wdi_ny_gdp_pcap_kd_zg", from_table = "wdi_cy", from_column = "wdi_ny_gdp_pcap_kd_zg")
#                             .transform.missing.fill()
#                            )
#          .with_column(Column("wdi_sl_uem_totl_zs", from_table = "wdi_cy", from_column = "wdi_ny_gdp_pcap_kd_zg")
#                             .transform.missing.fill()
#                            )

          # POL. INSTIUTIONS
          # Electoral democracy.
          .with_column(Column("vdem_v2x_polyarchy_tlag12", from_table = "vdem_v12_cy", from_column = "vdem_v12_v2x_polyarchy")
                             .transform.missing.fill()
                             .transform.temporal.tlag(12)
                             .transform.missing.fill()
                            )

          # Civil liberties
          .with_column(Column("vdem_v2x_civlib_tlag12", from_table = "vdem_v12_cy", from_column = "vdem_v12_v2x_civlib")
                             .transform.missing.fill()
                             .transform.temporal.tlag(12)
                             .transform.missing.fill()
                            )

          #.with_column(Column("vdem_v2clrgunev_tlag12", from_table = "vdem_v12_cy", from_column = "vdem_v2clrgunev")
                             #.transform.missing.fill()
                             #.transform.temporal.tlag(12)
                             #.transform.missing.fill()
                      #)

          .with_column(Column("vdem_v2clrgunev_tlag12", from_table = "tbl_734eevdem_v12_cy", from_column = "vdem_v12_v2clrgunev")
                             .transform.missing.fill()
                             .transform.temporal.tlag(12)
                             .transform.missing.fill()
                      )

          # Elections.
          .with_column(Column("lastelection", from_table = "reign_cm", from_column = "lastelection")
                             .transform.missing.replace_na()
                            )
          .with_column(Column("anticipation", from_table = "reign_cm", from_column = "anticipation")
                             .transform.missing.replace_na()
                            )


          .with_theme("protest_paper")
          .describe("""National dynamic protest model including local dynamic model, economic delveopment (national), political institutions III (full) and extended baseline variables, pgm level

                Predicting armed conflict (dummy) using protest data, extended baseline

                """)
        )


    data = qs_protest_full.publish().fetch()

    report(data)

    # Protest

    qs_protest_dynamic = (Queryset("fatalities003_protest_pr_dynamic_national", "priogrid_month")

           # target variable
           .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.ops.ln()
                        )

           # timelag 0 of target variable
           .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )

           # Decay functions
           # sb
           .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )

           .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(25)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )
           # os
           .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )

           # Spatial lag
           .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.spatial.lag(1, 1, 0, 0)
                        .transform.missing.replace_na()
                        )

           # Spatial lag decay
           .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm",
                               from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.spatial.lag(1, 1, 0, 0)
                        .transform.missing.replace_na()
                        )

           # Log population as control
           .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        .transform.missing.replace_na()
                        )


         ## 24 months 
        .with_column(Column("decay_ts_24_ged_sb_dummy", from_table = "ged2_pgm", from_column = "ged_sb_best_sum_nokgi")
             .transform.missing.replace_na()
             .transform.bool.gte(1)
             .transform.temporal.time_since()
             .transform.temporal.decay(24)
             .transform.missing.fill()
            )


          # Moving average over 24 months
          .with_column(Column("mov_avg_12_ged_best_sb", from_table = "ged2_pgm", from_column = "ged_sb_best_sum_nokgi")
                             .transform.ops.ln()
                             .transform.missing.replace_na()
                             .transform.temporal.moving_average(24)
                             .transform.missing.fill()
                            )

          ## PROTEST FEATURES - Dynamic Local

          .with_column(Column("decay_ts_6_acled_prex_dummy", from_table = "acled2_pgm", from_column = "acled_c3_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_acled_prpe_dummy", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prin_dummy", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prri_dummy", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prpe_dummy", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prex_dummy", from_table = "acled2_pgm", from_column = "acled_c3_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prin_dummy", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prri_dummy", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          # protest with excessive violence against protester (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prex_count", from_table = "acled2_pgm", from_column = "acled_c3_count") 
                             .transform.missing.replace_na()
                            )
          # peaceful protest (interaction codes: 60, 66, or 67.)
          .with_column(Column("acled_prpe_count", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                            )
          # protest with intervention (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prin_count", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                            )
          # protest with riots (interaction codes: inter 1 or 2 has 5)
          .with_column(Column("acled_prri_count", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                            )

          ## PROTEST FEATURES - Dynamic national

          .with_column(Column("decay_ts_6_acled_prex_dummy_cm", from_table = "acled2_cm", from_column = "acled_c3_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_acled_prpe_dummy_cm", from_table = "acled2_cm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prin_dummy_cm", from_table = "acled2_cm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prri_dummy_cm", from_table = "acled2_cm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          # protest with excessive violence against protester (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prex_count_cm", from_table = "acled2_cm", from_column = "acled_c3_count") 
                             .transform.missing.replace_na()
                            )
          # peaceful protest (interaction codes: 60, 66, or 67.)
          .with_column(Column("acled_prpe_count_cm", from_table = "acled2_cm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                            )
          # protest with intervention (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prin_count_cm", from_table = "acled2_cm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                            )
          # protest with riots (interaction codes: inter 1 or 2 has 5)
          .with_column(Column("acled_prri_count_cm", from_table = "acled2_cm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                            )

          # population
          .with_column(Column("wdi_sp_pop_totl", from_table = "wdi_cy", from_column = "wdi_sp_pop_totl")
                             .transform.missing.fill()
                             .transform.missing.extrapolate()
                             .transform.missing.replace_na()
                            )



          .with_theme("protest_paper")
          .describe("""National dynamic protest model including local dynamic model and extended baseline variables, pgm level

                Predicting armed conflict (dummy) using protest data, extended baseline

                """)
        )


    data = qs_protest_dynamic.publish().fetch()

    report(data)
    

    # ACLED

    qs_acled = (Queryset("fatalities003_acled", "priogrid_month")

           # target variable
           .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.ops.ln()
                        )

           # timelag 0 of target variable
           .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )

           # Decay functions
           # sb
           .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )

           .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(25)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )
           # os
           .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.missing.replace_na()
                        )

           # Spatial lag
           .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.spatial.lag(1, 1, 0, 0)
                        .transform.missing.replace_na()
                        )

           # Spatial lag decay
           .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm",
                               from_column="ged_sb_best_sum_nokgi")
                        .transform.missing.replace_na()
                        .transform.bool.gte(1)
                        .transform.temporal.time_since()
                        .transform.temporal.decay(24)
                        .transform.spatial.lag(1, 1, 0, 0)
                        .transform.missing.replace_na()
                        )

           # Log population as control
           .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        .transform.missing.replace_na()
                        )
          ## ACLED conflict features
                
           # timelag 0 of target variable
           .with_column(Column("acled_sb_fat", from_table="acled2_pgm", from_column="acled_sb_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
          .with_column(Column("decay_ts_6_acled_sb_100", from_table = "acled2_pgm", from_column = "acled_sb_fat")
                             .transform.missing.replace_na()
                             .transform.bool.gte(100)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_sb_1", from_table = "acled2_pgm", from_column = "acled_sb_fat")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
           .with_column(Column("acled_ns_fat", from_table="acled2_pgm", from_column="acled_ns_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_os_fat", from_table="acled2_pgm", from_column="acled_os_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_ns_fat", from_table="acled2_pgm", from_column="acled_ns_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
#           .with_column(Column("acled_c1_fat", from_table="acled2_pgm", from_column="acled_c1_fat")
#                        .transform.ops.ln()
#                        .transform.missing.fill()
#                        )
#                       .transform.ops.ln()
#                        .transform.missing.fill()
#                        )
#           .with_column(Column("acled_c3_fat", from_table="acled2_pgm", from_column="acled_c3_fat")
#                        .transform.ops.ln()
#                        .transform.missing.fill()
#                        )
#           .with_column(Column("acled_c4_fat", from_table="acled2_pgm", from_column="acled_c4_fat")
#                        .transform.ops.ln()
#                        .transform.missing.fill()
#                        )
#           .with_column(Column("acled_c5_fat", from_table="acled2_pgm", from_column="acled_c5_fat")
#                        .transform.ops.ln()
#                        .transform.missing.fill()
#                        )
           .with_column(Column("acled_st_abd_fat", from_table="acled2_pgm", from_column="acled_st_abd_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_st_agg_fat", from_table="acled2_pgm", from_column="acled_st_agg_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_st_arr_fat", from_table="acled2_pgm", from_column="acled_st_arr_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_st_chg_fat", from_table="acled2_pgm", from_column="acled_st_chg_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_st_wea_fat", from_table="acled2_pgm", from_column="acled_st_wea_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_st_hqb_fat", from_table="acled2_pgm", from_column="acled_st_hqb_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_st_loo_fat", from_table="acled2_pgm", from_column="acled_st_loo_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_st_ter_fat", from_table="acled2_pgm", from_column="acled_st_ter_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_st_oth_fat", from_table="acled2_pgm", from_column="acled_st_oth_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_bat_gov_fat", from_table="acled2_pgm", from_column="acled_bat_gov_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_bat_reb_fat", from_table="acled2_pgm", from_column="acled_bat_reb_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
           .with_column(Column("acled_bat_fat", from_table="acled2_pgm", from_column="acled_bat_fat")
                        .transform.ops.ln()
                        .transform.missing.fill()
                        )
               

          ## ACLED PROTEST FEATURES - Dynamic Local

          .with_column(Column("decay_ts_6_acled_prex_dummy", from_table = "acled2_pgm", from_column = "acled_c3_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_acled_prpe_dummy", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prin_dummy", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          .with_column(Column("decay_ts_6_acled_prri_dummy", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prpe_dummy", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prex_dummy", from_table = "acled2_pgm", from_column = "acled_c3_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prin_dummy", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )

          .with_column(Column("decay_ts_6_splag_1_2_acled_prri_dummy", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.spatial.lag(1,2,0,0)
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(6)
                             .transform.missing.fill()
                            )
          # protest with excessive violence against protester (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prex_count", from_table = "acled2_pgm", from_column = "acled_c3_count") 
                             .transform.missing.replace_na()
                            )
          # peaceful protest (interaction codes: 60, 66, or 67.)
          .with_column(Column("acled_prpe_count", from_table = "acled2_pgm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                            )
          # protest with intervention (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prin_count", from_table = "acled2_pgm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                            )
          # protest with riots (interaction codes: inter 1 or 2 has 5)
          .with_column(Column("acled_prri_count", from_table = "acled2_pgm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                            )


          # protest with excessive violence against protester (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prex_count_cm", from_table = "acled2_cm", from_column = "acled_c3_count") 
                             .transform.missing.replace_na()
                            )
          # peaceful protest (interaction codes: 60, 66, or 67.)
          .with_column(Column("acled_prpe_count_cm", from_table = "acled2_cm", from_column = "acled_c1_count")
                             .transform.missing.replace_na()
                            )
          # protest with intervention (interaction codes: 16, 26, 36, 46, 56, 68.)
          .with_column(Column("acled_prin_count_cm", from_table = "acled2_cm", from_column = "acled_c2_count")
                             .transform.missing.replace_na()
                            )
          # protest with riots (interaction codes: inter 1 or 2 has 5)
          .with_column(Column("acled_prri_count_cm", from_table = "acled2_cm", from_column = "acled_c5_count")
                             .transform.missing.replace_na()
                            )



          .with_theme("fatalities003")
          .describe("""ACLED features

                """)
        )


    data = qs_acled.publish().fetch()

    report(data)
    
    
    qs_cm_pgm = (Queryset("fatalities002_pgm_country_level", "priogrid_month")

                   # target variable
                   .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.ops.ln()
                                )

                   # timelag 0 of target variable
                   .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   # Decay functions
                   # sb
                   .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_sb_25", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(25)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )
                   # os
                   .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   # Spatial lag
                   .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   # Spatial lag decay
                   .with_column(Column("splag_1_decay_ged_sb_1", from_table="ged2_pgm",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   # Log population as control
                   .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                )

                   # sb
                   .with_column(Column("decay_ged_sb_5", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )
                    .with_column(Column("decay_ged_sb_500", from_table="ged2_cm",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(500)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )
             
                  .with_column(Column("vdem_v2x_libdem", from_table="vdem_v12_cy",
                                      from_column="vdem_v12_v2x_libdem")
                               .transform.missing.fill()
                               .transform.temporal.tlag(12)
                               .transform.missing.fill()
                               )

                   .with_column(Column("vdem_v2x_civlib", from_table="vdem_v12_cy", from_column="vdem_v12_v2x_civlib")
                               .transform.missing.fill()
                               .transform.temporal.tlag(12)
                               .transform.missing.fill()
                               )

                  .with_column(Column("vdem_v2x_clphy", from_table="vdem_v12_cy", from_column="vdem_v12_v2x_clphy")
                               .transform.missing.fill()
                               .transform.temporal.tlag(12)
                               .transform.missing.fill()
                               )

                  .with_column(Column("vdem_v2x_cspart", from_table="vdem_v12_cy",
                                      from_column="vdem_v12_v2x_cspart")
                               .transform.missing.fill()
                               .transform.temporal.tlag(12)
                               .transform.missing.fill()
                               )

                  .with_column(Column("vdem_v2x_rule", from_table="vdem_v12_cy", from_column="vdem_v12_v2x_rule")
                               .transform.missing.fill()
                               .transform.temporal.tlag(12)
                               .transform.missing.fill()
                               )

                 .with_column(Column("wdi_ny_gdp_pcap_kd", from_table="wdi_cy",
                                     from_column="wdi_ny_gdp_pcap_kd")
                              .transform.missing.fill()
                              .transform.temporal.tlag(12)
                              .transform.missing.fill()
                              )

                 .with_column(Column("wdi_sp_dyn_le00_in", from_table="wdi_cy",
                                     from_column="wdi_sp_dyn_le00_in")
                              .transform.missing.fill()
                              .transform.temporal.tlag(12)
                              .transform.missing.fill()
                              )
                 
                 .with_column(Column("wdi_sm_pop_refg_or", from_table="wdi_cy",
                                     from_column="wdi_sm_pop_refg_or")
                              .transform.missing.fill()
                              .transform.temporal.tlag(12)
                              .transform.missing.fill()
                              )

                 .with_column(Column("wdi_sm_pop_netm", from_table="wdi_cy", from_column="wdi_sm_pop_netm")
                              .transform.missing.fill()
                              .transform.temporal.tlag(12)
                              .transform.missing.fill()
                              )

                 .with_column(Column("wdi_sm_pop_totl_zs", from_table="wdi_cy",
                                     from_column="wdi_sm_pop_totl_zs")
                              .transform.missing.fill()
                              .transform.temporal.tlag(12)
                              .transform.missing.fill()
                              )
                 
                   .with_theme("fatalities")
                   .describe("""Fatalities conflict history, cm level
    
                             Predicting ln(fatalities) using conflict predictors, with country-level features
    
                            """)
                   )

    data = qs_cm_pgm.publish().fetch()

    report(data)
    
               
   #ESCWA drought vulnerability

    qs_drought_vulnerability_escwa = (Queryset("escwa001_pgm_drought_vulnerability", "priogrid_month")

                        # target variable
                        .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.ops.ln()
                                     )

                        # timelag 0 of target variable
                        .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.ops.ln()
                                     )

                        .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(1)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_os_1", from_table="ged2_pgm", from_column="ged_os_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(1)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )

                        .with_column(Column("decay_ged_ns_1", from_table="ged2_pgm", from_column="ged_ns_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.bool.gte(1)
                                     .transform.temporal.time_since()
                                     .transform.temporal.decay(12)
                                     .transform.missing.replace_na()
                                     )
                                               
                        .with_column(Column("count_moder_drought_prev10", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="count_moder_drought_prev10")
                                     .transform.missing.replace_na(0)
                                     )

                        
                        .with_column(Column("growseasdummy", from_table="hack_temp_escwa_pgm_pgm", from_column="growseasdummy")
                                     .transform.missing.replace_na(0)
                                     )
                                            
#                        .with_column(Column("gwmean", from_table="hack_temp_escwa_pgm_pgm",
#                                            from_column="gwmean")
#                                     .transform.missing.fill()
#                                     )
                        
                                                
#                        .with_column(Column("knn_dummy", from_table="hack_temp_escwa_pgm_pgm",
#                                            from_column="knn_dummy")
#                                     .transform.missing.fill()
#                                     )
                        
                        .with_column(Column("greq_1_excluded", from_table="priogrid_year", from_column="excluded")
                                     .transform.bool.gte(1)
                                     .transform.missing.fill()
                                     )

                        .with_column(Column("pgd_nlights_calib_mean", from_table="priogrid_year",
                                            from_column="nlights_calib_mean")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("wdi_nv_agr_totl_kd", from_table="wdi_cy", from_column="wdi_nv_agr_totl_kd")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("pgd_imr_mean", from_table="priogrid_year", from_column="imr_mean")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("ln_pop_gpw_sum", from_table="priogrid_year", from_column="pop_gpw_sum")
                                     .transform.missing.replace_na(0)
                                     .transform.ops.ln()
                                     )

                        .with_column(Column("ln_pgd_ttime_mean", from_table="priogrid_year", from_column="ttime_mean")
                                     .transform.missing.replace_na(0)
                                     .transform.ops.ln()
                                     )

                        .with_column(Column("pgd_urban_ih", from_table="priogrid_year", from_column="urban_ih")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("cropprop", from_table="hack_temp_escwa_pgm_pgm", from_column="cropprop")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gs_prev10", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gs_prev10")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gs_prev10_anom", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gs_prev10_anom")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gsm_cv_anom", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gsm_cv_anom")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1_gsm_detrend", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1_gsm_detrend")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei1gsy_lowermedian_count", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei1gsy_lowermedian_count")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("spei_48_detrend", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="spei_48_detrend")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_mod_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_mod_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_moder_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_moder_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_dr_sev_gs", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_dr_sev_gs")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag1_spei1_gsm", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag1_spei1_gsm")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_crop_sum", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_crop_sum")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_harvarea_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_harvarea_maincrops")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_irr_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_irr_maincrops")
                                     .transform.missing.replace_na(0)
                                     )

                        .with_column(Column("tlag_12_rainf_maincrops", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="tlag_12_rainf_maincrops")
                                     .transform.missing.replace_na(0)
                                     )


                        .with_theme("escwa")
                        .describe("""Fatalities, escwa drought and vulnerability, pgm level
    
                                  Predicting number of fatalities with features from the escwa drought and  vulnerability themes
                                  
                                  """)
                        )

    data = qs_drought_vulnerability_escwa.publish().fetch()
    
    report(data)                                     
                              
    # ESCWA space-time model
    qs_spacetime_escwa = (Queryset("escwa001_pgm_spacetime", "priogrid_month")

                      # target variable
                      .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.ops.ln()
                                   )

                      # dichotomous version, primarily for downsampling....
                      .with_column(Column("ged_gte_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                   .transform.bool.gte(1)
                                   )

                      # continuous, sptime_dist, nu=1
                      .with_column(Column("sptime_dist_k1_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k1_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 1.0, power)
                                   )

                      .with_column(Column("sptime_dist_k10_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k10_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k10_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 10.0, power)
                                   )

                      .with_column(Column("sptime_dist_k01_ged_sb", from_table="ged2_pgm",
                                          from_column="ged_sb_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )

                      .with_column(Column("sptime_dist_k01_ged_os", from_table="ged2_pgm",
                                          from_column="ged_os_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )

                      .with_column(Column("sptime_dist_k01_ged_ns", from_table="ged2_pgm",
                                          from_column="ged_ns_best_sum_nokgi")
                                   .transform.missing.replace_na()
                                   .transform.spatial.sptime_dist(return_values, n_nearest, 0.01, power)
                                   )         

                      .with_theme("escwa")
                      .describe("""Fatalities, escwa spacetime, pgm level
    
                                  Predicting number of fatalities with features from the escwa spacetime themes
                                  """)
                        )

    data = qs_spacetime_escwa.publish().fetch()
    
    report(data)
    
    qs_vulnerability_escwa = (Queryset("escwa001_pgm_vulnerability", "priogrid_month")

                 # target variable
                 .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.ops.ln()
                              )

                        # timelag 0 of target variable
                 .with_column(Column("ln_ged_sb", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.ops.ln()
                              )

                 .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(12)
                              .transform.missing.replace_na()
                              )
                              
                 .with_column(Column("splag_1_1_sb_1", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                              .transform.missing.replace_na()
                              .transform.bool.gte(1)
                              .transform.temporal.time_since()
                              .transform.temporal.decay(24)
                              .transform.spatial.lag(1, 1, 0, 0)
                              .transform.missing.replace_na()
                             )
                       
                 .with_column(Column("greq_1_excluded", from_table="priogrid_year", from_column="excluded")
                              .transform.bool.gte(1)
                              .transform.missing.fill()
                              )
                        
                 .with_column(Column("pgd_nlights_calib_mean",from_table="priogrid_year",from_column="nlights_calib_mean")
                              .transform.missing.replace_na(0)
                              )         

                 .with_theme("escwa")
                 .describe("""Fatalities, escwa spacetime, pgm level Predicting number of fatalities with features from the escwa spacetime themes """)
                        )

    data = qs_vulnerability_escwa.publish().fetch()
    
    report(data)
        
    
    qslist = [
              qs_baseline,
              qs_conflict_long,
              qs_escwa_drought,
              qs_natsoc,
              qs_broad,
              qs_conf_history,
              qs_treelag,
              qs_sptime_dist,
              qs_acled,
              qs_protest_dynamic,
              qs_protest_full,
              qs_cm_pgm,
              qs_drought_escwa,
              qs_vulnerability_escwa,
              qs_drought_vulnerability_escwa,
              qs_climate_extremes_escwa,
              qs_spacetime_escwa,
              qs_naturalsocial_escwa,
              qs_combo_escwa,
              ]

    return qslist
