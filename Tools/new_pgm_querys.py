


def get_pgm_querysets():
    
    # ESCWA drought
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
                                            
                        .with_column(Column("gwmean", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="gwmean")
                                     .transform.missing.fill()
                                     )
                                                
                        .with_column(Column("knn_dummy", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="knn_dummy")
                                     .transform.missing.fill()
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
                        .describe("""Fatalities, escwa drought, pgm level
    
                                  Predicting number of fatalities with features from the escwa drought themes
                                  
                                  """)
                        )

    data = qs_drought_escwa.publish().fetch()
    
    print(f"escwa001_pgm_drought "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )
    
#################################################################################################################################    
    # ESCWA vulnerability
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

                        .with_column(Column("decay_ged_sb_1", from_table="ged2_pgm",
                                            from_column="ged_sb_best_sum_nokgi")
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
                       
                        .with_column(Column("greq_1_excluded", from_table="priogrid_year", from_column="excluded")
                                     .transform.bool.gte(1)
                                     .transform.missing.fill()
                                     )
                        
                        .with_column(Column("pgd_nlights_calib_mean", from_table="priogrid_year",from_column="nlights_calib_mean")
                                     .transform.missing.replace_na(0)
                                     )         

                        .with_theme("escwa")
                        .describe("""Fatalities, escwa vulnerability, pgm level
    
                                  Predicting number of fatalities with features from the escwa vulnerability themes
                                  
                                  """)
                        )

    data = qs_vulnerability_escwa.publish().fetch()
    
    print(f"escwa001_pgm_vulnerability "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )
                              
 ############################################################################################################################
                              
 # ESCWA drought vulnerability

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
                                            
                        .with_column(Column("gwmean", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="gwmean")
                                     .transform.missing.fill()
                                     )
                        
                                                
                        .with_column(Column("knn_dummy", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="knn_dummy")
                                     .transform.missing.fill()
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
    
                                  Predicting number of fatalities with features from the escwa drought and 
                                  vulnerability themes
                                  
                                  """)
                        )

    data = qs_drought_vulnerability_escwa.publish().fetch()
    
    print(f"escwa001_pgm_drought_vulnerability "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )
    
#################################################################################################################################
################################################################################################################################# 
############################################################################################################################
#################################################################################################################################    
    # ESCWA Climate Extremes
    qs_climate_extremes_escwa = (Queryset("escwa001_pgm_extremes", "priogrid_month")

                        # target variable
                        .with_column(Column("ln_ged_sb_dep", from_table="ged2_pgm", from_column="ged_sb_best_sum_nokgi")
                                     .transform.missing.replace_na()
                                     .transform.ops.ln()
                                     )

                        .with_column(Column("r30mm", from_table="Climate_year_pgy", from_column="r30mm")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                        
                        .with_column(Column("tn10p", from_table="Climate_year_pgy", from_column="tn10p")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                                 
                        .with_column(Column("r10mm", from_table="Climate_year_pgy", from_column="r10mm")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )    
                                 
                        .with_column(Column("txm", from_table="Climate_year_pgy", from_column="txm")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )                                     

                        .with_column(Column("tmm", from_table="Climate_year_pgy", from_column="tmm")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )    
                                 
                        .with_column(Column("tmge5", from_table="Climate_year_pgy", from_column="tmge5")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                        .with_column(Column("ice_days", from_table="Climate_year_pgy", from_column="ice_days")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )    
                                 
                        .with_column(Column("txge30", from_table="Climate_year_pgy", from_column="txge30")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )         
                                 
                        .with_column(Column("tnltm20", from_table="Climate_year_pgy", from_column="tnltm20")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )                                    
                                 
                        .with_column(Column("tnm", from_table="Climate_year_pgy", from_column="tnm")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )      
                                 
                        .with_column(Column("r20mm", from_table="Climate_year_pgy", from_column="r20mm")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )    
                                 
                        .with_column(Column("tmlt10", from_table="Climate_year_pgy", from_column="tmlt10")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )   
                                 
                        .with_column(Column("consecutive_dry_days_index_per_time_period", from_table="Climate_year_pgy", from_column="consecutive_dry_days_index_per_time_period")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                        .with_column(Column("number_of_cdd_periods_with_more_than_5days_per_time_period", from_table="Climate_year_pgy", from_column="number_of_cdd_periods_with_more_than_5days_per_time_period")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 

                        .with_column(Column("tnltm2", from_table="Climate_year_pgy", from_column="tnltm2")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                        .with_column(Column("su", from_table="Climate_year_pgy", from_column="su")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                        .with_column(Column("tx90p", from_table="Climate_year_pgy", from_column="tx90p")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                        .with_column(Column("txx", from_table="Climate_year_pgy", from_column="txx")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                                 
                        .with_column(Column("tmge10", from_table="Climate_year_pgy", from_column="tmge10")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                                 
                        .with_column(Column("tr", from_table="Climate_year_pgy", from_column="tr")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                                 
                        .with_column(Column("rx5day", from_table="Climate_year_pgy", from_column="rx5day")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                                 
                        .with_column(Column("tn90p", from_table="Climate_year_pgy", from_column="tn90p")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                                               
                        .with_column(Column("txn", from_table="Climate_year_pgy", from_column="txn")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                        .with_column(Column("rx7day", from_table="Climate_year_pgy", from_column="rx7day")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                        .with_column(Column("txgt50p", from_table="Climate_year_pgy", from_column="txgt50p")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                        .with_column(Column("txgt35", from_table="Climate_year_pgy", from_column="txgt35")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )          
                                 
                        .with_column(Column("tx10p", from_table="Climate_year_pgy", from_column="tx10p")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )  
                                 
                        .with_column(Column("consecutive_wet_days_index_per_time_period", from_table="Climate_year_pgy", from_column="consecutive_wet_days_index_per_time_period")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )  
                                                
                        .with_column(Column("number_of_cwd_periods_with_more_than_5days_per_time_period", from_table="Climate_year_pgy", from_column="number_of_cwd_periods_with_more_than_5days_per_time_period")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )           
                        
                         .with_column(Column("prcptot", from_table="Climate_year_pgy", from_column="prcptot")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )          
                         
                         .with_column(Column("txn", from_table="Climate_year_pgy", from_column="txn")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )        
                           
                         .with_column(Column("fd", from_table="Climate_year_pgy", from_column="fd")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                                 
                         .with_column(Column("tnn", from_table="Climate_year_pgy", from_column="tnn")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                        
                         .with_column(Column("tnlt2", from_table="Climate_year_pgy", from_column="tnlt2")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )
                                 
                         .with_column(Column("dtr", from_table="Climate_year_pgy", from_column="dtr")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     ) 
                                 
                         .with_column(Column("tmlt5", from_table="Climate_year_pgy", from_column="tmlt5")
                                     .transform.missing.replace_na(0)
                                     .transform.temporal.tlag(12)
                                     .transform.missing.replace_na(0)
                                     )        
                                 
                        .with_theme("escwa")
                        .describe("""Fatalities, escwa climate extremes, pgm level
    
                                  Predicting number of fatalities with features from the escwa climate extreme themes
                                  
                                  """)
                        )

    data = qs_climate_extremes_escwa.publish().fetch()
    
    print(f"escwa001_pgm_extremes "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )
                              
 #################################################################################################################################    
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
                      )         

                        .with_theme("escwa")
                        .describe("""Fatalities, escwa spacetime, pgm level
    
                                  Predicting number of fatalities with features from the escwa spacetime themes
                                  
                                  """)
                        )

    data = qs_spacetime_escwa.publish().fetch()
    
    print(f"escwa001_pgm_spacetime "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )
                              
                     
 #################################################################################################################################    
    # ESCWA natural and social model
    qs_naturalsocial_escwa = (Queryset("escwa001_pgm_naturalsocial", "priogrid_month")

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
                              
                        .with_theme("escwa")
                        .describe("""Fatalities, escwa natural social, pgm level
    
                                  Predicting number of fatalities with features from the escwa natural social themes
                                  
                                  """)
                        )

    data = qs_naturalsocial_escwa.publish().fetch()
    
    print(f"escwa001_pgm_naturalsocial "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )
                              
 ############################################################################################################################      
# ESCWA drought
    qs_combined_escwa = (Queryset("escwa001_pgm_combined", "priogrid_month")

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
                                            
                        .with_column(Column("gwmean", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="gwmean")
                                     .transform.missing.fill()
                                     )
                                                
                        .with_column(Column("knn_dummy", from_table="hack_temp_escwa_pgm_pgm",
                                            from_column="knn_dummy")
                                     .transform.missing.fill()
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
                         
                        .with_theme("escwa")
                        .describe("""Fatalities, escwa drought and natsocial models, pgm level
    
                        Predicting number of fatalities with features from the escwa drought and natural and social models themes
                                  
                                  """)
                        )

    data = qs_combined_escwa.publish().fetch()
    
    print(f"escwa001_pgm_combined "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )    
    