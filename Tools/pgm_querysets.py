# # Specifying querysets for use in Predicting Fatalities project
# ## pgm level
# 
# 

# ## Importing modules

# Basics
import numpy as np
from viewser import Queryset, Column

'''



THIS IS SOME BLANK SPACE TO TEST THE GITHUB WORKFLOW



'''
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


def get_pgm_querysets():

    qs_baseline = (Queryset("fatalities002_pgm_baseline", "priogrid_month")

               # target variable
               .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.ops.ln()
                             )

                # timelag 0 of target variable
                .with_column(Column("ln_ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.ops.ln()
                             .transform.missing.fill()
                             )

                # Decay functions
                # sb
                .with_column(Column("decay_ged_sb_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(24)
                             .transform.missing.replace_na()
                             )

                .with_column(Column("decay_ged_sb_25", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(25)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(24)
                            .transform.missing.replace_na()
                             )
                # os
                .with_column(Column("decay_ged_os_1", from_loa="priogrid_month", from_column="ged_os_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(24)
                             .transform.missing.replace_na()
                             )

                # Spatial lag
                .with_column(Column("splag_1_1_sb_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(24)
                             .transform.spatial.lag(1, 1, 0, 0)
                             .transform.missing.replace_na()
                             )

#                # Spatial lag decay
                .with_column(Column("splag_1_decay_ged_sb_1", from_loa="priogrid_month",
                                   from_column="ged_sb_best_sum_nokgi")
                             .transform.missing.replace_na()
                             .transform.bool.gte(1)
                             .transform.temporal.time_since()
                             .transform.temporal.decay(24)
                             .transform.spatial.lag(1, 1, 0, 0)
                             .transform.missing.replace_na()
                             )

               # Log population as control
               .with_column(Column("ln_pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum")
                            .transform.ops.ln()
                            .transform.missing.fill()
                            .transform.missing.replace_na()
                            )

               .with_theme("fatalities")
               .describe("""Fatalities conflict history, cm level

                         Predicting ln(fatalities) using conflict predictors, ultrashort

                        """)
               )

    qs_conflict_long = (Queryset("fatalities002_pgm_conflictlong", "priogrid_month")

                    # target variable
                    .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.ops.ln()
                                 )

                    # timelags 0 of conflict variables, ged_best versions

                    .with_column(Column("ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("ged_os", from_loa="priogrid_month", from_column="ged_os_best_sum_nokgi")
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("ged_ns", from_loa="priogrid_month", from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 )

                    # Spatial lag
                    .with_column(Column("splag_1_1_sb_1", from_loa="priogrid_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(1)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.spatial.lag(1, 1, 0, 0)
                                 .transform.missing.replace_na()
                                 )

                    # Spatial lag decay
                    .with_column(Column("splag_1_decay_ged_sb_1", from_loa="priogrid_month",
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
                    .with_column(Column("decay_ged_sb_5", from_loa="priogrid_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_sb_25", from_loa="priogrid_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(25)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_sb_100", from_loa="priogrid_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(100)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_sb_500", from_loa="priogrid_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(500)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    # os
                    .with_column(Column("decay_ged_os_5", from_loa="priogrid_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_os_25", from_loa="priogrid_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(25)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_os_100", from_loa="priogrid_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(100)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_os_500", from_loa="priogrid_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(500)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )
                    # ns
                    .with_column(Column("decay_ged_ns_5", from_loa="priogrid_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_ns_25", from_loa="priogrid_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(25)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_ns_100", from_loa="priogrid_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(100)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_ns_500", from_loa="priogrid_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(500)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    # Log population as control
                    .with_column(Column("ln_pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 )

                    .with_theme("fatalities")
                    .describe("""fatalities longer conflict history, pgm level

                              Predicting ln(ged_best_sb) using conflict predictors, longer version

                              """)
                    )

    qs_escwa_drought = (Queryset("fatalities002_pgm_escwa_drought", "priogrid_month")

                    # target variable
                    .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.ops.ln()
                                 )

                    # timelag 0 of target variable
                    .with_column(Column("ln_ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.ops.ln()
                                 )

                    .with_column(Column("decay_ged_sb_1", from_loa="priogrid_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(1)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_os_1", from_loa="priogrid_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(1)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_ns_1", from_loa="priogrid_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(1)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(12)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("greq_1_excluded", from_loa="priogrid_year", from_column="excluded")
                                 .transform.bool.gte(1)
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("pgd_nlights_calib_mean", from_loa="priogrid_year",
                                        from_column="nlights_calib_mean")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("wdi_nv_agr_totl_kd", from_loa="country_year", from_column="wdi_nv_agr_totl_kd")
                                 .transform.missing.replace_na(0)
                                 .transform.temporal.tlag(12)
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("pgd_imr_mean", from_loa="priogrid_year", from_column="imr_mean")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("ln_pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum")
                                 .transform.missing.replace_na(0)
                                 .transform.ops.ln()
                                 )

                    .with_column(Column("ln_pgd_ttime_mean", from_loa="priogrid_year", from_column="ttime_mean")
                                 .transform.missing.replace_na(0)
                                 .transform.ops.ln()
                                 )

                    .with_column(Column("pgd_urban_ih", from_loa="priogrid_year", from_column="urban_ih")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("count_moder_drought_prev10", from_loa="priogrid_month",
                                        from_column="count_moder_drought_prev10")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("cropprop", from_loa="priogrid_month", from_column="cropprop")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("growseasdummy", from_loa="priogrid_month",
                                        from_column="growseasdummy")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("spei1_gs_prev10", from_loa="priogrid_month",
                                        from_column="spei1_gs_prev10")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("spei1_gs_prev10_anom", from_loa="priogrid_month",
                                        from_column="spei1_gs_prev10_anom")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("spei1_gsm_cv_anom", from_loa="priogrid_month",
                                        from_column="spei1_gsm_cv_anom")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("spei1_gsm_detrend", from_loa="priogrid_month",
                                        from_column="spei1_gsm_detrend")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("spei1gsy_lowermedian_count", from_loa="priogrid_month",
                                        from_column="spei1gsy_lowermedian_count")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("spei_48_detrend", from_loa="priogrid_month",
                                        from_column="spei_48_detrend")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("tlag1_dr_mod_gs", from_loa="priogrid_month",
                                        from_column="tlag1_dr_mod_gs")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("tlag1_dr_moder_gs", from_loa="priogrid_month",
                                        from_column="tlag1_dr_moder_gs")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("tlag1_dr_sev_gs", from_loa="priogrid_month",
                                        from_column="tlag1_dr_sev_gs")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("tlag1_spei1_gsm", from_loa="priogrid_month",
                                        from_column="tlag1_spei1_gsm")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("tlag_12_crop_sum", from_loa="priogrid_month",
                                        from_column="tlag_12_crop_sum")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("tlag_12_harvarea_maincrops", from_loa="priogrid_month",
                                        from_column="tlag_12_harvarea_maincrops")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("tlag_12_irr_maincrops", from_loa="priogrid_month",
                                        from_column="tlag_12_irr_maincrops")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_column(Column("tlag_12_rainf_maincrops", from_loa="priogrid_month",
                                        from_column="tlag_12_rainf_maincrops")
                                 .transform.missing.replace_na(0)
                                 )

                    .with_theme("fatalities")
                    .describe("""Fatalities, escwa drought and vulnerability, pgm level

                              Predicting number of fatalities with features from the escwa drought and 
                              vulnerability themes

                              """)
                    )

    qs_natsoc = (Queryset("fatalities002_pgm_natsoc", "priogrid_month")

             # target variable
             .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                          .transform.missing.replace_na()
                          .transform.ops.ln()
                          )

             # timelag 0 of target variable
             .with_column(Column("ln_ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                          .transform.ops.ln()
                          .transform.missing.fill()
                          )

             # Decay functions
             # sb
             .with_column(Column("decay_ged_sb_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                          .transform.missing.replace_na()
                          .transform.bool.gte(1)
                          .transform.temporal.time_since()
                          .transform.temporal.decay(24)
                          .transform.missing.replace_na()
                          )

             .with_column(Column("decay_ged_sb_25", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                          .transform.missing.replace_na()
                          .transform.bool.gte(25)
                          .transform.temporal.time_since()
                          .transform.temporal.decay(24)
                          .transform.missing.replace_na()
                          )

             # os
             .with_column(Column("decay_ged_os_1", from_loa="priogrid_month", from_column="ged_os_best_sum_nokgi")
                          .transform.missing.replace_na()
                          .transform.bool.gte(1)
                          .transform.temporal.time_since()
                          .transform.temporal.decay(24)
                          .transform.missing.replace_na()
                          )

             # Spatial lag
             .with_column(Column("splag_1_1_sb_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                          .transform.missing.replace_na()
                          .transform.bool.gte(1)
                          .transform.temporal.time_since()
                          .transform.temporal.decay(24)
                          .transform.spatial.lag(1, 1, 0, 0)
                          .transform.missing.replace_na()
                          )

             # Spatial lag decay
             .with_column(Column("splag_1_decay_ged_sb_1", from_loa="priogrid_month",
                                 from_column="ged_sb_best_sum_nokgi")
                          .transform.missing.replace_na()
                          .transform.bool.gte(1)
                          .transform.temporal.time_since()
                          .transform.temporal.decay(24)
                          .transform.spatial.lag(1, 1, 0, 0)
                          .transform.missing.replace_na()
                          )

             # Log population as control
             .with_column(Column("ln_pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum")
                          .transform.ops.ln()
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             # from priogrid table:

             .with_column(Column("ln_ttime_mean", from_loa="priogrid_year", from_column="ttime_mean")
                          .transform.ops.ln()
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("ln_gcp_mer", from_loa="priogrid_year", from_column="gcp_mer")
                          .transform.ops.ln()
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("imr_mean", from_loa="priogrid_year", from_column="imr_mean")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("ln_bdist3", from_loa="priogrid_year", from_column="bdist3")
                          .transform.ops.ln()
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("ln_capdist", from_loa="priogrid_year", from_column="capdist")
                          .transform.ops.ln()
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("mountains_mean", from_loa="priogrid_year", from_column="mountains_mean")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("dist_diamsec", from_loa="priogrid", from_column="dist_diamsec_s_wgs")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("dist_petroleum", from_loa="priogrid", from_column="dist_petroleum_s_wgs")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("agri_ih", from_loa="priogrid_year", from_column="agri_ih")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("barren_ih", from_loa="priogrid_year", from_column="barren_ih")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("forest_ih", from_loa="priogrid_year", from_column="forest_ih")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("pasture_ih", from_loa="priogrid_year", from_column="pasture_ih")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("savanna_ih", from_loa="priogrid_year", from_column="savanna_ih")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("shrub_ih", from_loa="priogrid_year", from_column="shrub_ih")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("urban_ih", from_loa="priogrid_year", from_column="urban_ih")
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_column(Column("greq_1_excluded", from_loa="priogrid_year", from_column="excluded")
                          .transform.bool.gte(1)
                          .transform.missing.fill()
                          .transform.missing.replace_na()
                          )

             .with_theme("fatalities")
             .describe("""Fatalities natural and social geography, pgm level

                       Predicting ln(fatalities) using natural and social geography features

                       """)
             )
    qs_broad = (Queryset("fatalities002_pgm_broad", "priogrid_month")

            # target variable
            .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.ops.ln()
                         )

            # timelags 0 of conflict variables, ged_best versions

            .with_column(Column("ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            .with_column(Column("ged_os", from_loa="priogrid_month", from_column="ged_os_best_sum_nokgi")
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            .with_column(Column("ged_ns", from_loa="priogrid_month", from_column="ged_ns_best_sum_nokgi")
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            # Spatial lag
            .with_column(Column("splag_1_1_sb_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.bool.gte(1)
                         .transform.temporal.time_since()
                         .transform.temporal.decay(24)
                         .transform.spatial.lag(1, 1, 0, 0)
                         .transform.missing.replace_na()
                         )

            # Decay functions
            # sb
            .with_column(Column("decay_ged_sb_5", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.bool.gte(5)
                         .transform.temporal.time_since()
                         .transform.temporal.decay(12)
                         .transform.missing.replace_na()
                         )
            # os
            .with_column(Column("decay_ged_os_5", from_loa="priogrid_month", from_column="ged_os_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.bool.gte(5)
                         .transform.temporal.time_since()
                         .transform.temporal.decay(12)
                         .transform.missing.replace_na()
                         )

            # ns
            .with_column(Column("decay_ged_ns_5", from_loa="priogrid_month", from_column="ged_ns_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.bool.gte(5)
                         .transform.temporal.time_since()
                         .transform.temporal.decay(12)
                         .transform.missing.replace_na()
                         )

            # Trees

            .with_column(Column("treelag_1_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.spatial.treelag(0.7, 1)
                         )

            .with_column(Column("treelag_2_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.spatial.treelag(0.7, 2)
                         )
            # sptime

            # continuous, sptime_dist, nu=1
            .with_column(Column("sptime_dist_k1_ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.spatial.sptime_dist('distances', 1, 1.0, 0.0)
                         )

            .with_column(Column("sptime_dist_k10_ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.spatial.sptime_dist('distances', 1, 10.0, 0.0)
                         )

            .with_column(Column("sptime_dist_k001_ged_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                         .transform.missing.replace_na()
                         .transform.spatial.sptime_dist('distances', 1, 0.01, 0.0)
                         )

            # From natsoc
            .with_column(Column("ln_ttime_mean", from_loa="priogrid_year", from_column="ttime_mean")
                         .transform.ops.ln()
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            .with_column(Column("ln_bdist3", from_loa="priogrid_year", from_column="bdist3")
                         .transform.ops.ln()
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            .with_column(Column("ln_capdist", from_loa="priogrid_year", from_column="capdist")
                         .transform.ops.ln()
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            .with_column(Column("dist_diamsec", from_loa="priogrid", from_column="dist_diamsec_s_wgs")
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            .with_column(Column("imr_mean", from_loa="priogrid_year", from_column="imr_mean")
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            # From drought
            .with_column(Column("tlag1_dr_mod_gs", from_loa="priogrid_month",
                                from_column="tlag1_dr_mod_gs")
                         .transform.missing.replace_na(0)
                         )

            .with_column(Column("spei1_gs_prev10_anom", from_loa="priogrid_month",
                                from_column="spei1_gs_prev10_anom")
                         .transform.missing.replace_na(0)
                         )

            .with_column(Column("tlag_12_crop_sum", from_loa="priogrid_month",
                                from_column="tlag_12_crop_sum")
                         .transform.missing.replace_na(0)
                         )

            .with_column(Column("spei1gsy_lowermedian_count", from_loa="priogrid_month",
                                from_column="spei1gsy_lowermedian_count")
                         .transform.missing.replace_na(0)
                         )

            # Log population as control
            .with_column(Column("ln_pop_gpw_sum", from_loa="priogrid_year", from_column="pop_gpw_sum")
                         .transform.ops.ln()
                         .transform.missing.fill()
                         .transform.missing.replace_na()
                         )

            .with_theme("fatalities")
            .describe("""fatalities broad model, pgm level

                      Predicting ln(ged_best_sb), broad model

                      """)
            )

    qs_conf_history = (Queryset("fatalities002_pgm_conflict_history", "priogrid_month")

                   # target variable
                   .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   # timelags 1-12 of target variable
                   .with_column(Column("ln_ged_sb_tlag_1", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_2", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_3", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(3)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_4", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(4)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_5", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(5)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_6", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(6)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_7", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(7)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_8", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(8)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_9", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(9)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_10", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(10)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_11", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(11)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_12", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   # 12-month decay dummy of target variable
                   .with_column(Column("ln_ged_sb_decay_12_time_since", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.temporal.decay(12)
                                .transform.bool.gte(1)
                                .transform.missing.fill()
                                )

                   # (1,1) spatially-lagged 1-timelagged target variable
                   .with_column(Column("ln_ged_sb_tlag_1_splag_1", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.missing.fill()
                                )

                   # (1,1) spatially-lagged target variable
                   .with_column(Column("ln_ged_sb_splag_1", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   # time-lagged by 1 independent variables
                   .with_column(Column("ln_ged_ns_tlag_1", from_loa="priogrid_month",
                                       from_column="ged_ns_best_count_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_os_tlag_1", from_loa="priogrid_month",
                                       from_column="ged_os_best_count_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.missing.fill()
                                )

                   # 12-month decay dummy of independent variables
                   .with_column(Column("ln_ged_ns_decay_12_time_since", from_loa="priogrid_month",
                                       from_column="ged_ns_best_count_nokgi")
                                .transform.temporal.decay(12)
                                .transform.bool.gte(1)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_os_decay_12_time_since", from_loa="priogrid_month",
                                       from_column="ged_os_best_count_nokgi")
                                .transform.temporal.decay(12)
                                .transform.bool.gte(1)
                                .transform.missing.fill()
                                )

                   # (1,1) spatially-lagged independent variables
                   .with_column(Column("ln_ged_ns_splag_1", from_loa="priogrid_month",
                                       from_column="ged_ns_best_count_nokgi")
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_os_splag_1", from_loa="priogrid_month",
                                       from_column="ged_os_best_count_nokgi")
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   # (1,1) spatially-lagged 1-timelagged independent variables
                   .with_column(Column("ln_ged_ns_tlag_1_splag_1", from_loa="priogrid_month",
                                       from_column="ged_ns_best_count_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_os_tlag_1_splag_1", from_loa="priogrid_month",
                                       from_column="ged_os_best_count_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.spatial.lag(1, 1, 0, 0)
                                .transform.missing.fill()
                                )

                   # moving average and sum
                   .with_column(Column("mov_avg_6_ged_best_sb", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.moving_average(6)
                                )

                   .with_column(Column("mov_avg_12_ged_best_sb", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.moving_average(12)
                                )

                   .with_column(Column("mov_avg_36_ged_best_sb", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.moving_average(36)
                                )

                   .with_column(Column("mov_sum_6_ged_best_sb", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.moving_sum(6)
                                )

                   .with_column(Column("mov_sum_12_ged_best_sb", from_loa="priogrid_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.moving_sum(12)
                                )

                   .with_column(Column("mov_sum_36_ged_best_sb", from_loa="priogrid_month",
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

    qs_treelag = (Queryset("fatalities002_pgm_conflict_treelag", "priogrid_month")
              # target variable
              .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                           .transform.missing.replace_na()
                           .transform.ops.ln()
                           )

              # dichotomous version, primarily for downsampling....
              .with_column(Column("ged_gte_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                           .transform.bool.gte(1)
                           )

              .with_column(Column("treelag_1_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                           .transform.missing.replace_na()
                           .transform.spatial.treelag(0.7, 1)
                           )

              .with_column(Column("treelag_1_ns", from_loa="priogrid_month", from_column="ged_ns_best_sum_nokgi")
                           .transform.missing.replace_na()
                           .transform.spatial.treelag(0.7, 1)
                           )

              .with_column(Column("treelag_1_os", from_loa="priogrid_month", from_column="ged_os_best_sum_nokgi")
                           .transform.missing.replace_na()
                           .transform.spatial.treelag(0.7, 1)
                           )

              .with_column(Column("treelag_2_sb", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                           .transform.missing.replace_na()
                           .transform.spatial.treelag(0.7, 2)
                           )

              .with_column(Column("treelag_2_ns", from_loa="priogrid_month", from_column="ged_ns_best_sum_nokgi")
                           .transform.missing.replace_na()
                           .transform.spatial.treelag(0.7, 2)
                           )

              .with_column(Column("treelag_2_os", from_loa="priogrid_month", from_column="ged_os_best_sum_nokgi")
                           .transform.missing.replace_na()
                           .transform.spatial.treelag(0.7, 2)
                           )
              )

    qs_sptime_dist = (Queryset("fatalities002_pgm_conflict_sptime_dist", "priogrid_month")
                  # target variable
                  .with_column(Column("ln_ged_sb_dep", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.ops.ln()
                               )

                  # dichotomous version, primarily for downsampling....
                  .with_column(Column("ged_gte_1", from_loa="priogrid_month", from_column="ged_sb_best_sum_nokgi")
                               .transform.bool.gte(1)
                               )

                  # continuous, sptime_dist, nu=1
                  .with_column(Column("sptime_dist_k1_ged_sb", from_loa="priogrid_month",
                                      from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 1.0, 0.0)
                               )

                  .with_column(Column("sptime_dist_k1_ged_os", from_loa="priogrid_month",
                                      from_column="ged_os_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 1.0, 0.0)
                               )

                  .with_column(Column("sptime_dist_k1_ged_ns", from_loa="priogrid_month",
                                      from_column="ged_ns_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 1.0, 0.0)
                               )

                  .with_column(Column("sptime_dist_k10_ged_sb", from_loa="priogrid_month",
                                      from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 10.0, 0.0)
                               )

                  .with_column(Column("sptime_dist_k10_ged_os", from_loa="priogrid_month",
                                      from_column="ged_os_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 10.0, 0.0)
                               )

                  .with_column(Column("sptime_dist_k10_ged_ns", from_loa="priogrid_month",
                                      from_column="ged_ns_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 10.0, 0.0)
                               )

                  .with_column(Column("sptime_dist_k001_ged_sb", from_loa="priogrid_month",
                                      from_column="ged_sb_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 0.01, 0.0)
                               )

                  .with_column(Column("sptime_dist_k001_ged_os", from_loa="priogrid_month",
                                      from_column="ged_os_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 0.01, 0.0)
                               )

                  .with_column(Column("sptime_dist_k001_ged_ns", from_loa="priogrid_month",
                                      from_column="ged_ns_best_sum_nokgi")
                               .transform.missing.replace_na()
                               .transform.spatial.sptime_dist('distances', 1, 0.01, 0.0)
                               )
                  )

    qslist = [
              qs_baseline,
              qs_conflict_long,
              qs_escwa_drought,
              qs_natsoc,
              qs_broad,
              qs_conf_history,
              qs_treelag,
              qs_sptime_dist
              ]

    return qslist
