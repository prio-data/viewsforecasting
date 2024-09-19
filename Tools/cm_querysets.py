# # Specifying querysets for use in Predicting Fatalities project
# Fatalities002 version
# ## cm level
# 

# ## Importing modules

# Basics
import numpy as np
from viewser import Queryset, Column

'''


THIS IS SOME BLANK SPACE TO TEST THE GITHUB WORKFLOW















'''

def get_cm_querysets():


#######################################################################################################################
    qs_baseline = (Queryset("fatalities002_baseline", "country_month")

               # target variable
               .with_column(Column("ln_ged_sb_dep", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                            .transform.ops.ln()
                            .transform.missing.fill()
                            )

               # timelag 0 of target variable
               .with_column(Column("ln_ged_sb", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                            .transform.ops.ln()
                            .transform.missing.fill()
                            )
               # Decay functions
               # sb
               .with_column(Column("decay_ged_sb_5", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                            .transform.missing.replace_na()
                            .transform.bool.gte(5)
                            .transform.temporal.time_since()
                            .transform.temporal.decay(24)
                            .transform.missing.replace_na()
                            )
               # os
               .with_column(Column("decay_ged_os_5", from_loa="country_month", from_column="ged_os_best_sum_nokgi")
                            .transform.missing.replace_na()
                            .transform.bool.gte(5)
                            .transform.temporal.time_since()
                            .transform.temporal.decay(24)
                            .transform.missing.replace_na()
                            )
               # Spatial lag decay
               .with_column(Column("splag_1_decay_ged_sb_5", from_loa="country_month",
                                   from_column="ged_sb_best_sum_nokgi")
                            .transform.missing.replace_na()
                            .transform.bool.gte(5)
                            .transform.temporal.time_since()
                            .transform.temporal.decay(24)
                            .transform.spatial.countrylag(1, 1, 0, 0)
                            .transform.missing.replace_na()
                            )

               # From

               .with_column(Column("wdi_sp_pop_totl", from_loa="country_year", from_column="wdi_sp_pop_totl")
                            .transform.missing.fill()
                            .transform.temporal.tlag(12)
                            .transform.missing.fill()
                            .transform.missing.replace_na()
                            )

               .with_theme("fatalities")
               .describe("""Fatalities conflict history, cm level

               Predicting ln(fatalities) using conflict predictors, ultrashort

                         """)
               )

    qs_topics_stub = (Queryset("fatalities002_topics_stub", "country_month")

                  # Topic, tokens
                  .with_column(Column('topic_tokens_t1', from_loa='country_month', from_column='topic_tokens')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_tokens_t2', from_loa='country_month', from_column='topic_tokens')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_tokens_t13', from_loa='country_month', from_column='topic_tokens')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_tokens_t1_splag', from_loa='country_month', from_column='topic_tokens')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )
                  # Topic 0
                  .with_column(Column('topic_ste_theta0_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta0_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta0_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta0_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta0_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta0_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta0_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta0_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 1
                  .with_column(Column('topic_ste_theta1_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta1_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta1_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta1_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta1_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta1_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta1_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta1_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 2
                  .with_column(Column('topic_ste_theta2_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta2_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta2_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta2_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta2_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta2_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta2_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta2_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 3
                  .with_column(Column('topic_ste_theta3_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta3_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta3_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta3_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta3_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta3_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta3_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta3_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 4
                  .with_column(Column('topic_ste_theta4_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta4_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta4_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta4_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta4_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta4_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta4_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta4_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 5
                  .with_column(Column('topic_ste_theta5_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta5_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta5_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta5_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta5_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta5_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta5_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta5_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 6
                  .with_column(Column('topic_ste_theta6_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta6_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta6_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta6_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta6_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta6_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta6_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta6_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 7
                  .with_column(Column('topic_ste_theta7_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta7_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta7_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta7_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta7_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta7_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta7_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta7_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 8
                  .with_column(Column('topic_ste_theta8_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta8_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta8_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta8_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta8_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta8_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta8_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta8_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 9
                  .with_column(Column('topic_ste_theta9_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta9_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta9_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta9_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta9_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta9_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta9_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta9_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 10
                  .with_column(Column('topic_ste_theta10_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta10_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta10_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta10_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta10_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta10_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta10_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta10_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 11
                  .with_column(Column('topic_ste_theta11_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta11_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta11_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta11_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta11_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta11_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta11_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta11_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 12
                  .with_column(Column('topic_ste_theta12_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta12_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta12_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta12_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta12_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta12_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta12_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta12_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 13
                  .with_column(Column('topic_ste_theta13_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta13_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta13_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta13_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta13_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta13_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta13_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta13_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  # Topic 14
                  .with_column(Column('topic_ste_theta14_stock_t1', from_loa='country_month',
                                      from_column='topic_ste_theta14_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(1)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta14_stock_t2', from_loa='country_month',
                                      from_column='topic_ste_theta14_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(2)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta14_stock_t13', from_loa='country_month',
                                      from_column='topic_ste_theta14_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               )

                  .with_column(Column('topic_ste_theta14_stock_t1_splag', from_loa='country_month',
                                      from_column='topic_ste_theta14_stock')
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               .transform.temporal.tlag(13)
                               .transform.missing.fill()
                               .transform.spatial.countrylag(1, 1, 0, 0)
                               .transform.missing.replace_na()
                               )

                  .with_theme("fatalities")
                  .describe("""Predicting ln(fatalities), cm level

                            Stub queryset with Mueller & Rauh topic model features

                            """)
                  )

    qs_aquastat_stub = (Queryset("fatalities002_aquastat_stub", "country_month")

                    # Agricultural water withdrawal as % of total renewable water resources [%]
                    .with_column(Column('agr_withdrawal_pct_t48', from_loa='country_year',
                                        from_column='agr_withdrawal_pct')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # Dam capacity per capita [m3/inhab]
                    .with_column(Column('dam_cap_pcap_t48', from_loa='country_year', from_column='dam_cap_pcap')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # Groundwater: leaving the country to other countries (total) [10^9 m3/year]
                    .with_column(Column('groundwater_export_t48', from_loa='country_year',
                                        from_column='groundwater_export')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # MDG 7.5. Freshwater withdrawal as % of total renewable water resources [%]
                    .with_column(Column('fresh_withdrawal_pct_t48', from_loa='country_year',
                                        from_column='fresh_withdrawal_pct')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # SDG 6.4.1. Industrial Water Use Efficiency [US$/m3]
                    .with_column(Column('ind_efficiency_t48', from_loa='country_year',
                                        from_column='ind_efficiency')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # SDG 6.4.1. Irrigated Agriculture Water Use Efficiency [US$/m3]
                    .with_column(Column('irr_agr_efficiency_t48', from_loa='country_year',
                                        from_column='irr_agr_efficiency')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # SDG 6.4.1. Services Water Use Efficiency [US$/m3]
                    .with_column(Column('services_efficiency_t48', from_loa='country_year',
                                        from_column='services_efficiency')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # SDG 6.4.1. Water Use Efficiency [US$/m3]
                    .with_column(Column('general_efficiency_t48', from_loa='country_year',
                                        from_column='general_efficiency')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # SDG 6.4.2. Water Stress [%]
                    .with_column(Column('water_stress_t48', from_loa='country_year', from_column='water_stress')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # Total internal renewable water resources per capita [m3/inhab/yr]
                    .with_column(Column('renewable_internal_pcap_t48', from_loa='country_year',
                                        from_column='renewable_internal_pcap')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    # Total annual renewable water resources per capita [m3/inhab/year]
                    .with_column(Column('renewable_pcap_t48', from_loa='country_year',
                                        from_column='renewable_pcap')
                                 .transform.missing.fill()
                                 .transform.missing.replace_na()
                                 .transform.temporal.tlag(48)
                                 .transform.missing.fill()
                                 )

                    .with_theme("fatalities")
                    .describe("""Predicting ln(fatalities), cm level

                              Queryset based on the FAO AQUASTAT data

                              """)
                    )

    qs_conflict_stub = (Queryset("fatalities002_cm_conflict_history_stub", "country_month")

                    # Lags
                    .with_column(Column("ln_ged_sb_tlag_1", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 .transform.temporal.tlag(1)
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_ged_sb_tlag_2", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 .transform.temporal.tlag(2)
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_ged_sb_tlag_3", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 .transform.temporal.tlag(3)
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_ged_sb_tlag_4", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 .transform.temporal.tlag(4)
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_ged_sb_tlag_5", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 .transform.temporal.tlag(5)
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_ged_sb_tlag_6", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 .transform.temporal.tlag(6)
                                 .transform.missing.fill()
                                 )
                    # Moving sums
                    .with_column(Column("ln_ged_sb_tsum_24", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.temporal.moving_sum(24)
                                 .transform.ops.ln()
                                 .transform.missing.replace_na()
                                 )

                    # Decay functions
                    # sb

                    .with_column(Column("decay_ged_sb_100", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(100)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_sb_500", from_loa="country_month",
                                        from_column="ged_sb_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(500)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )
                    # os

                    .with_column(Column("decay_ged_os_100", from_loa="country_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(100)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )
                    # ns
                    .with_column(Column("decay_ged_ns_5", from_loa="country_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_ged_ns_100", from_loa="country_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(100)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("ln_ged_sb", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    # Other independent variables
                    .with_column(Column("ln_ged_ns", from_loa="country_month", from_column="ged_ns_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_ged_os", from_loa="country_month", from_column="ged_os_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_acled_sb", from_loa="country_month", from_column="acled_sb_fat")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_acled_sb_count", from_loa="country_month", from_column="acled_sb_count")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    .with_column(Column("ln_acled_os", from_loa="country_month", from_column="acled_os_fat")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 )

                    # time-lagged by 0-2 independent variables
                    .with_column(Column("ln_ged_os_tlag_1", from_loa="country_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.ops.ln()
                                 .transform.missing.fill()
                                 .transform.temporal.tlag(1)
                                 .transform.missing.fill()
                                 )

                    # 12-month decay dummy of independent variables
                    .with_column(Column("decay_acled_sb_5", from_loa="country_month", from_column="acled_sb_fat")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_acled_os_5", from_loa="country_month", from_column="acled_os_fat")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("decay_acled_ns_5", from_loa="country_month", from_column="acled_ns_fat")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.missing.replace_na()
                                 )

                    # Spatial lags of decay functions
                    .with_column(Column("splag_1_decay_ged_os_5", from_loa="country_month",
                                        from_column="ged_os_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.spatial.countrylag(1, 1, 0, 0)
                                 .transform.missing.replace_na()
                                 )

                    .with_column(Column("splag_1_decay_ged_ns_5", from_loa="country_month",
                                        from_column="ged_ns_best_sum_nokgi")
                                 .transform.missing.replace_na()
                                 .transform.bool.gte(5)
                                 .transform.temporal.time_since()
                                 .transform.temporal.decay(24)
                                 .transform.spatial.countrylag(1, 1, 0, 0)
                                 .transform.missing.replace_na()
                                 )

                    # gwnos
                    .with_column(Column("gleditsch_ward", from_loa="country", from_column="gwcode")
                                 )

                    .with_theme("fatalities")
                    .describe("""Fatalities conflict history, cm level

                                  Predicting ln(fatalities) using conflict predictors

                                  """)
                    )

    qs_conflict_ext = (Queryset("fatalities002_cm_conflict_history_ext", "country_month")

                   # Moving sums
                   .with_column(Column("ln_ged_sb_tsum_12", from_loa="country_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.temporal.moving_sum(12)
                                .transform.ops.ln()
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("ln_ged_sb_tsum_48", from_loa="country_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.temporal.moving_sum(48)
                                .transform.ops.ln()
                                .transform.missing.replace_na()
                                )

                   # Spatial lags
                   .with_column(Column("splag_1_ged_sb", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                )

                   .with_column(Column("splag_2_ged_sb", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.spatial.countrylag(1, 2, 0, 0)
                                )

                   .with_column(Column("splag_1_ged_os", from_loa="country_month", from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                )

                   .with_column(Column("splag_1_ged_ns", from_loa="country_month", from_column="ged_ns_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                )
                   # Decay functions
                   # sb
                   .with_column(Column("decay_ged_sb_1", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_sb_25", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(25)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )
                   # os
                   .with_column(Column("decay_ged_os_1", from_loa="country_month", from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_os_5", from_loa="country_month", from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_os_25", from_loa="country_month", from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(25)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_os_500", from_loa="country_month",
                                       from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(500)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )
                   # ns
                   .with_column(Column("decay_ged_ns_1", from_loa="country_month",
                                       from_column="ged_ns_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(1)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_ns_25", from_loa="country_month", from_column="ged_ns_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(25)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_ns_500", from_loa="country_month",
                                       from_column="ged_ns_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(500)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   # Spatial lags of decays
                   .with_column(Column("splag_1_decay_ged_sb_100", from_loa="country_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(100)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("splag_1_decay_ged_os_100", from_loa="country_month",
                                       from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(100)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("splag_1_decay_ged_ns_100", from_loa="country_month",
                                       from_column="ged_ns_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(100)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   # Other independent variables
                   .with_column(Column("ln_acled_prx_count", from_loa="country_month", from_column="acled_prx_count")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_pr_count", from_loa="country_month", from_column="acled_pr_count")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_prx_fat", from_loa="country_month", from_column="acled_prx_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_sb_gov", from_loa="country_month", from_column="acled_bat_gov_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_sb_reb", from_loa="country_month", from_column="acled_bat_reb_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_ns", from_loa="country_month", from_column="acled_ns_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   # time-lagged by 0-2 independent variables
                   .with_column(Column("ln_ged_ns_tlag_1", from_loa="country_month",
                                       from_column="ged_ns_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_ns_tlag_2", from_loa="country_month",
                                       from_column="ged_ns_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_os_tlag_2", from_loa="country_month",
                                       from_column="ged_os_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_sb_tlag_1", from_loa="country_month", from_column="acled_sb_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_sb_tlag_2", from_loa="country_month", from_column="acled_sb_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_os_tlag_1", from_loa="country_month", from_column="acled_os_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_os_tlag_2", from_loa="country_month", from_column="acled_os_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_ns_tlag_1", from_loa="country_month", from_column="acled_ns_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_acled_ns_tlag_2", from_loa="country_month", from_column="acled_os_fat")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )

                   .with_theme("fatalities")
                   .describe("""Fatalities conflict history extensions, cm level

                              Predicting ln(fatalities) using conflict predictors, extended longer conflict history

                             """)
                   )

    qs_vdem_short_stub = (Queryset("fatalities002_vdem_short_stub", "country_month")

                      # Features from vdem
                      .with_column(Column("vdem_v2x_delibdem", from_loa='country_year',
                                          from_column="vdem_v12_v2x_delibdem")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_egaldem", from_loa='country_year',
                                          from_column="vdem_v12_v2x_egaldem")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_libdem", from_loa='country_year',
                                          from_column="vdem_v12_v2x_libdem")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_libdem_48", from_loa='country_year',
                                          from_column="vdem_v12_v2x_libdem")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(60)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_partip", from_loa='country_year',
                                          from_column="vdem_v12_v2x_partip")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_partipdem", from_loa='country_year',
                                          from_column="vdem_v12_v2x_partipdem")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_accountability", from_loa='country_year',
                                          from_column="vdem_v12_v2x_accountability")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_civlib", from_loa='country_year',
                                          from_column="vdem_v12_v2x_civlib")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_clphy", from_loa='country_year',
                                          from_column="vdem_v12_v2x_clphy")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_cspart", from_loa='country_year',
                                          from_column="vdem_v12_v2x_cspart")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_divparctrl", from_loa='country_year',
                                          from_column="vdem_v12_v2x_divparctrl")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_edcomp_thick", from_loa='country_year',
                                          from_column="vdem_v12_v2x_edcomp_thick")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_egal", from_loa='country_year',
                                          from_column="vdem_v12_v2x_egal")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_execorr", from_loa='country_year',
                                          from_column="vdem_v12_v2x_execorr")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_frassoc_thick", from_loa='country_year',
                                          from_column="vdem_v12_v2x_frassoc_thick")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_gencs", from_loa='country_year',
                                          from_column="vdem_v12_v2x_gencs")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_gender", from_loa='country_year',
                                          from_column="vdem_v12_v2x_gender")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_genpp", from_loa='country_year',
                                          from_column="vdem_v12_v2x_genpp")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_horacc", from_loa='country_year',
                                          from_column="vdem_v12_v2x_horacc")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_neopat", from_loa='country_year',
                                          from_column="vdem_v12_v2x_neopat")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_pubcorr", from_loa='country_year',
                                          from_column="vdem_v12_v2x_pubcorr")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_rule", from_loa='country_year',
                                          from_column="vdem_v12_v2x_rule")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_veracc", from_loa='country_year',
                                          from_column="vdem_v12_v2x_veracc")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_ex_military", from_loa='country_year',
                                          from_column="vdem_v12_v2x_ex_military")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_ex_party", from_loa='country_year',
                                          from_column="vdem_v12_v2x_ex_party")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_freexp", from_loa='country_year',
                                          from_column="vdem_v12_v2x_freexp")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xcl_acjst", from_loa='country_year',
                                          from_column="vdem_v12_v2xcl_acjst")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xcl_dmove", from_loa='country_year',
                                          from_column="vdem_v12_v2xcl_dmove")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xcl_prpty", from_loa='country_year',
                                          from_column="vdem_v12_v2xcl_prpty")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xcl_rol", from_loa='country_year',
                                          from_column="vdem_v12_v2xcl_rol")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xcl_slave", from_loa='country_year',
                                          from_column="vdem_v12_v2xcl_slave")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xdd_dd", from_loa='country_year', from_column="vdem_v12_v2xdd_dd")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xdl_delib", from_loa='country_year',
                                          from_column="vdem_v12_v2xdl_delib")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xeg_eqdr", from_loa='country_year',
                                          from_column="vdem_v12_v2xeg_eqdr")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xeg_eqprotec", from_loa='country_year',
                                          from_column="vdem_v12_v2xeg_eqprotec")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xel_frefair", from_loa='country_year',
                                          from_column="vdem_v12_v2xel_frefair")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xel_regelec", from_loa='country_year',
                                          from_column="vdem_v12_v2xel_regelec")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xme_altinf", from_loa='country_year',
                                          from_column="vdem_v12_v2xme_altinf")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xnp_client", from_loa='country_year',
                                          from_column="vdem_v12_v2xnp_client")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xnp_regcorr", from_loa='country_year',
                                          from_column="vdem_v12_v2xnp_regcorr")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xpe_exlecon", from_loa='country_year',
                                          from_column="vdem_v12_v2xpe_exlecon")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xpe_exlpol", from_loa='country_year',
                                          from_column="vdem_v12_v2xpe_exlpol")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xpe_exlgeo", from_loa='country_year',
                                          from_column="vdem_v12_v2xpe_exlgeo")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xpe_exlgender", from_loa='country_year',
                                          from_column="vdem_v12_v2xpe_exlgender")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xpe_exlsocgr", from_loa='country_year',
                                          from_column="vdem_v12_v2xpe_exlsocgr")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xps_party", from_loa='country_year',
                                          from_column="vdem_v12_v2xps_party")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xcs_ccsi", from_loa='country_year',
                                          from_column="vdem_v12_v2xcs_ccsi")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xnp_pres", from_loa='country_year',
                                          from_column="vdem_v12_v2xnp_pres")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2xeg_eqaccess", from_loa='country_year',
                                          from_column="vdem_v12_v2xeg_eqaccess")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("vdem_v2x_diagacc", from_loa='country_year',
                                          from_column="vdem_v12_v2x_diagacc")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )
                      .with_column(Column("vdem_v2clrgunev", from_loa='country_year',
                                          from_column="vdem_v12_v2clrgunev")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      # Spatial lags

                      .with_column(Column("splag_vdem_v2x_libdem", from_loa='country_year',
                                          from_column="vdem_v12_v2x_libdem")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   )

                      .with_column(Column("splag_vdem_v2xcl_dmove", from_loa='country_year',
                                          from_column="vdem_v12_v2xcl_dmove")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   )

                      .with_column(Column("splag_vdem_v2x_accountability", from_loa='country_year',
                                          from_column="vdem_v12_v2x_accountability")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   )

                      .with_column(Column("splag_vdem_v2xpe_exlsocgr", from_loa='country_year',
                                          from_column="vdem_v12_v2xpe_exlsocgr")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   )

                      .with_column(Column("splag_vdem_v2xcl_rol", from_loa='country_year',
                                          from_column="vdem_v12_v2xcl_rol")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   )

                      # From WDI
                      .with_column(Column("wdi_sm_pop_netm", from_loa='country_year', from_column="wdi_sm_pop_netm")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column("wdi_sp_dyn_imrt_in", from_loa='country_year',
                                          from_column="wdi_sp_dyn_imrt_in")
                                   .transform.missing.fill()
                                   .transform.temporal.tlag(12)
                                   .transform.missing.fill()
                                   )

                      .with_theme("fatalities")
                      .describe("""Predicting ln(fatalities), cm level

                                Queryset with cy features from vdem, short

                                """)
                      )

    qs_wdi_short_stub = (Queryset("fatalities002_wdi_short_stub", "country_month")

                     # Features from WDI
                     .with_column(Column("wdi_ag_lnd_frst_k2", from_loa='country_year',
                                         from_column="wdi_ag_lnd_frst_k2")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_dt_oda_odat_pc_zs", from_loa='country_year',
                                         from_column="wdi_dt_oda_odat_pc_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_ms_mil_xpnd_gd_zs", from_loa='country_year',
                                         from_column="wdi_ms_mil_xpnd_gd_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_ms_mil_xpnd_zs", from_loa='country_year',
                                         from_column="wdi_ms_mil_xpnd_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_nv_agr_totl_kd", from_loa='country_year',
                                         from_column="wdi_nv_agr_totl_kd")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_nv_agr_totl_kn", from_loa='country_year',
                                         from_column="wdi_nv_agr_totl_kn")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     # .with_column(Column("wdi_ny_gdp_mktp_kd", from_table="wdi_cy",
                     #                    from_column="wdi_ny_gdp_mktp_kd")
                     #             .transform.missing.fill()
                     #             .transform.temporal.tlag(12)
                     #             .transform.missing.fill()
                     #             )

                     .with_column(Column("wdi_ny_gdp_pcap_kd", from_loa='country_year',
                                         from_column="wdi_ny_gdp_pcap_kd")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sp_dyn_le00_in", from_loa='country_year',
                                         from_column="wdi_sp_dyn_le00_in")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_se_enr_prim_fm_zs", from_loa='country_year',
                                         from_column="wdi_se_enr_prim_fm_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_se_enr_prsc_fm_zs", from_loa='country_year',
                                         from_column="wdi_se_enr_prsc_fm_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_se_prm_nenr", from_loa='country_year',
                                         from_column="wdi_se_prm_nenr")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sh_sta_maln_zs", from_loa='country_year',
                                         from_column="wdi_sh_sta_maln_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sh_sta_stnt_zs", from_loa='country_year',
                                         from_column="wdi_sh_sta_stnt_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sl_tlf_totl_fe_zs", from_loa='country_year',
                                         from_column="wdi_sl_tlf_totl_fe_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sm_pop_refg_or", from_loa='country_year',
                                         from_column="wdi_sm_pop_refg_or")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sm_pop_netm", from_loa='country_year', from_column="wdi_sm_pop_netm")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sm_pop_totl_zs", from_loa='country_year',
                                         from_column="wdi_sm_pop_totl_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     # .with_column(Column("wdi_sp_dyn_tfrt_in", from_table="wdi_cy",
                     # from_column="wdi_sp_dyn_tfrt_in")
                     # .transform.missing.fill()
                     # .transform.temporal.tlag(12)
                     # .transform.missing.fill()
                     # )

                     .with_column(Column("wdi_sp_dyn_imrt_in", from_loa='country_year',
                                         from_column="wdi_sp_dyn_imrt_in")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sh_dyn_mort_fe", from_loa='country_year',
                                         from_column="wdi_sh_dyn_mort_fe")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sp_pop_14_fe_zs", from_loa='country_year',
                                         from_column="wdi_sp_pop_0014_fe_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sp_pop_1564_fe_zs", from_loa='country_year',
                                         from_column="wdi_sp_pop_1564_fe_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sp_pop_65up_fe_zs", from_loa='country_year',
                                         from_column="wdi_sp_pop_65up_fe_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sp_pop_grow", from_loa='country_year', from_column="wdi_sp_pop_grow")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     .with_column(Column("wdi_sp_urb_totl_in_zs", from_loa='country_year',
                                         from_column="wdi_sp_urb_totl_in_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.missing.fill()
                                  )

                     # Spatial lags
                     .with_column(Column("splag_wdi_sl_tlf_totl_fe_zs", from_loa='country_year',
                                         from_column="wdi_sl_tlf_totl_fe_zs")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.spatial.countrylag(1, 1, 0, 0)
                                  .transform.missing.replace_na()
                                  )

                     .with_column(Column("splag_wdi_sm_pop_refg_or", from_loa='country_year',
                                         from_column="wdi_sm_pop_refg_or")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.spatial.countrylag(1, 1, 0, 0)
                                  .transform.missing.replace_na()
                                  )

                     .with_column(Column("splag_wdi_sm_pop_netm", from_loa='country_year',
                                         from_column="wdi_sm_pop_netm")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.spatial.countrylag(1, 1, 0, 0)
                                  .transform.missing.replace_na()
                                  )

                     .with_column(Column("splag_wdi_ag_lnd_frst_k2", from_loa='country_year',
                                         from_column="wdi_ag_lnd_frst_k2")
                                  .transform.missing.fill()
                                  .transform.temporal.tlag(12)
                                  .transform.spatial.countrylag(1, 1, 0, 0)
                                  .transform.missing.replace_na()
                                  )

                     .with_theme("fatalities")
                     .describe("""Predicting ln(fatalities), cm level

                               Queryset with cy features from wdi, short version

                               """)

                     )


    qs_joint_narrow = (Queryset("fatalities002_joint_narrow", "country_month")

                   # target variable
                   .with_column(Column("ln_ged_sb_dep", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   .with_column(Column("gleditsch_ward", from_loa="country", from_column="gwcode")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                )

                   # Baseline features:
                   # lag of target variable
                   .with_column(Column("ln_ged_sb", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   # Decay functions
                   # sb
                   .with_column(Column("decay_ged_sb_5", from_loa="country_month", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )
                   # os
                   .with_column(Column("decay_ged_os_5", from_loa="country_month", from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   # Spatial lag decay
                   .with_column(Column("splag_1_decay_ged_sb_5", from_loa="country_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("wdi_sp_pop_totl", from_loa="country_year", from_column="wdi_sp_pop_totl")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   # More conflict history [hh20]
                   .with_column(Column("ln_ged_sb_tlag_1", from_loa="country_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(1)
                                .transform.missing.fill()
                                )

                   .with_column(Column("ln_ged_sb_tlag_2", from_loa="country_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )

                   .with_column(Column("decay_acled_os_5", from_loa="country_month", from_column="acled_os_fat")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_sb_100", from_loa="country_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(100)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("decay_ged_sb_500", from_loa="country_month",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(500)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                )

                   # Features from reign [hh20]
                   .with_column(Column("reign_tenure_months", from_loa="country_month", from_column="tenure_months")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                )

                   # From WDI [hh20]
                   .with_column(Column("wdi_ag_lnd_frst_k2", from_loa="country_year", from_column="wdi_ag_lnd_frst_k2")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("wdi_nv_agr_totl_kn", from_loa="country_year", from_column="wdi_nv_agr_totl_kn")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("wdi_sh_sta_maln_zs", from_loa="country_year", from_column="wdi_sh_sta_maln_zs")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("wdi_sl_tlf_totl_fe_zs", from_loa="country_year",
                                       from_column="wdi_sl_tlf_totl_fe_zs")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("wdi_sm_pop_refg_or", from_loa="country_year", from_column="wdi_sm_pop_refg_or")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("wdi_sp_dyn_imrt_in", from_loa="country_year", from_column="wdi_sp_dyn_imrt_in")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("wdi_sp_pop_14_fe_zs", from_loa="country_year",
                                       from_column="wdi_sp_pop_0014_fe_zs")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("wdi_sp_pop_grow", from_loa="country_year", from_column="wdi_sp_pop_grow")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   # Spatial lags [hh20]

                   .with_column(Column("splag_wdi_ag_lnd_frst_k2", from_loa="country_year",
                                       from_column="wdi_ag_lnd_frst_k2")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("splag_wdi_sl_tlf_totl_fe_zs", from_loa="country_year",
                                       from_column="wdi_sl_tlf_totl_fe_zs")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("splag_wdi_sm_pop_netm", from_loa="country_year", from_column="wdi_sm_pop_netm")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   # From Vdem
                   .with_column(Column("vdem_v2xcl_dmove", from_loa="country_year", from_column="vdem_v12_v2xcl_dmove")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("vdem_v2xcl_rol", from_loa="country_year", from_column="vdem_v12_v2xcl_rol")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("vdem_v2xeg_eqdr", from_loa="country_year", from_column="vdem_v12_v2xeg_eqdr")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("vdem_v2xpe_exlpol", from_loa="country_year",
                                       from_column="vdem_v12_v2xpe_exlpol")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("vdem_v2xpe_exlsocgr", from_loa="country_year",
                                       from_column="vdem_v12_v2xpe_exlsocgr")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("splag_vdem_v2xpe_exlsocgr", from_loa="country_year",
                                       from_column="vdem_v12_v2xpe_exlsocgr")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   .with_column(Column("splag_vdem_v2xcl_rol", from_loa="country_year",
                                       from_column="vdem_v12_v2xcl_rol")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                )

                   .with_theme("fatalities")
                   .describe("""Predicting ged_dummy_sb, cm level

                             Queryset with features from various sources, 'joint narrow'

                             """)
                   )

    qs_joint_broad_stub = (Queryset("fatalities002_joint_broad_stub", "country_month")

                       .with_column(Column("ln_ged_sb_tlag_1", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(1)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_2", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(2)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_3", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(3)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_4", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(4)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_5", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(5)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_sb_tlag_6", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(6)
                                    .transform.missing.fill()
                                    )

                       # Decay functions
                       # sb

                       .with_column(Column("decay_ged_sb_5", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("decay_ged_sb_100", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(100)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("decay_ged_sb_500", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(500)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )
                       # os

                       .with_column(Column("decay_ged_os_5", from_loa='country_month',
                                           from_column="ged_os_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("decay_ged_os_100", from_loa='country_month',
                                           from_column="ged_os_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(100)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )
                       # ns
                       .with_column(Column("decay_ged_ns_5", from_loa='country_month',
                                           from_column="ged_ns_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("decay_ged_ns_100", from_loa='country_month',
                                           from_column="ged_ns_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(100)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                       # Other independent variables
                       .with_column(Column("ln_ged_ns", from_loa='country_month',
                                           from_column="ged_ns_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_ged_os", from_loa='country_month',
                                           from_column="ged_os_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_acled_sb", from_loa='country_month', from_column="acled_sb_fat")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_acled_sb_count", from_loa='country_month',
                                           from_column="acled_sb_count")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("ln_acled_os", from_loa='country_month', from_column="acled_os_fat")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    )

                       # time-lagged by 0-2 independent variables
                       .with_column(Column("ln_ged_os_tlag_1", from_loa='country_month',
                                           from_column="ged_os_best_sum_nokgi")
                                    .transform.ops.ln()
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(1)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("decay_acled_sb_5", from_loa='country_month', from_column="acled_sb_fat")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("decay_acled_os_5", from_loa='country_month', from_column="acled_os_fat")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("decay_acled_ns_5", from_loa='country_month', from_column="acled_ns_fat")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.missing.replace_na()
                                    )

                       # Spatial lags of decay functions
                       .with_column(Column("splag_1_decay_ged_sb_5", from_loa='country_month',
                                           from_column="ged_sb_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_1_decay_ged_os_5", from_loa='country_month',
                                           from_column="ged_os_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_1_decay_ged_ns_5", from_loa='country_month',
                                           from_column="ged_ns_best_sum_nokgi")
                                    .transform.missing.replace_na()
                                    .transform.bool.gte(5)
                                    .transform.temporal.time_since()
                                    .transform.temporal.decay(24)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       # gwnos
                       .with_column(Column("gleditsch_ward", from_loa="country", from_column="gwcode")
                                    )

                       # Features from topic model

                       # Topic, tokens
                       .with_column(Column('topic_tokens_t1', from_loa='country_month', from_column='topic_tokens')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(1)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column('topic_tokens_t2', from_loa='country_month', from_column='topic_tokens')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(2)
                                    .transform.missing.fill()
                                    )
                       # Topic 4
                       .with_column(Column('topic_ste_theta4_stock_t1', from_loa='country_month',
                                           from_column='topic_ste_theta4_stock')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(1)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column('topic_ste_theta4_stock_t2', from_loa='country_month',
                                           from_column='topic_ste_theta4_stock')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(2)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column('topic_ste_theta4_stock_t13', from_loa='country_month',
                                           from_column='topic_ste_theta4_stock')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(13)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column('topic_ste_theta4_stock_t1_splag', from_loa='country_month',
                                           from_column='topic_ste_theta4_stock')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(13)
                                    .transform.missing.fill()
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       # Topic 5
                       .with_column(Column('topic_ste_theta2_stock_t1', from_loa='country_month',
                                           from_column='topic_ste_theta5_stock')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(1)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column('topic_ste_theta2_stock_t2', from_loa='country_month',
                                           from_column='topic_ste_theta5_stock')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(2)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column('topic_ste_theta2_stock_t13', from_loa='country_month',
                                           from_column='topic_ste_theta5_stock')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(13)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column('topic_ste_theta2_stock_t1_splag', from_loa='country_month',
                                           from_column='topic_ste_theta5_stock')
                                    .transform.missing.fill()
                                    .transform.missing.replace_na()
                                    .transform.temporal.tlag(13)
                                    .transform.missing.fill()
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       # From WDI
                       .with_column(Column("wdi_sm_pop_netm", from_loa='country_year', from_column="wdi_sm_pop_netm")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_sm_pop_refg_or", from_loa='country_year',
                                           from_column="wdi_sm_pop_refg_or")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_dt_oda_odat_pc_zs", from_loa='country_year',
                                           from_column="wdi_dt_oda_odat_pc_zs")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_ms_mil_xpnd_gd_zs", from_loa='country_year',
                                           from_column="wdi_ms_mil_xpnd_gd_zs")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_sl_tlf_totl_fe_zs", from_loa='country_year',
                                           from_column="wdi_sl_tlf_totl_fe_zs")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_nv_agr_totl_kn", from_loa='country_year',
                                           from_column="wdi_nv_agr_totl_kn")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_sp_pop_grow", from_loa='country_year', from_column="wdi_sp_pop_grow")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_se_enr_prim_fm_zs", from_loa='country_year',
                                           from_column="wdi_se_enr_prim_fm_zs")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_sp_urb_totl_in_zs", from_loa='country_year',
                                           from_column="wdi_sp_urb_totl_in_zs")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_sh_sta_maln_zs", from_loa='country_year',
                                           from_column="wdi_sh_sta_maln_zs")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_sp_dyn_imrt_fe_in", from_loa='country_year',
                                           from_column="wdi_sp_dyn_imrt_fe_in")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_ny_gdp_mktp_kd", from_loa='country_year',
                                           from_column="wdi_ny_gdp_mktp_kd")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("wdi_sh_sta_stnt_zs", from_loa='country_year',
                                           from_column="wdi_sh_sta_stnt_zs")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       # Spatial lags
                       .with_column(Column("splag_wdi_sl_tlf_totl_fe_zs", from_loa='country_year',
                                           from_column="wdi_sl_tlf_totl_fe_zs")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_wdi_sm_pop_refg_or", from_loa='country_year',
                                           from_column="wdi_sm_pop_refg_or")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_wdi_sm_pop_netm", from_loa='country_year',
                                           from_column="wdi_sm_pop_netm")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_wdi_ag_lnd_frst_k2", from_loa='country_year',
                                           from_column="wdi_ag_lnd_frst_k2")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       # From Vdem
                       .with_column(Column("vdem_v2x_horacc", from_loa='country_year',
                                           from_column="vdem_v12_v2x_horacc")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xnp_client", from_loa='country_year',
                                           from_column="vdem_v12_v2xnp_client")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2x_veracc", from_loa='country_year',
                                           from_column="vdem_v12_v2x_veracc")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2x_divparctrl", from_loa='country_year',
                                           from_column="vdem_v12_v2x_divparctrl")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xpe_exlpol", from_loa='country_year',
                                           from_column="vdem_v12_v2xpe_exlpol")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2x_diagacc", from_loa='country_year',
                                           from_column="vdem_v12_v2x_diagacc")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xpe_exlgeo", from_loa='country_year',
                                           from_column="vdem_v12_v2xpe_exlgeo")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xpe_exlgender", from_loa='country_year',
                                           from_column="vdem_v12_v2xpe_exlgender")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xpe_exlsocgr", from_loa='country_year',
                                           from_column="vdem_v12_v2xpe_exlsocgr")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2x_ex_party", from_loa='country_year',
                                           from_column="vdem_v12_v2x_ex_party")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2x_genpp", from_loa='country_year',
                                           from_column="vdem_v12_v2x_genpp")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xeg_eqdr", from_loa='country_year',
                                           from_column="vdem_v12_v2xeg_eqdr")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xcl_prpty", from_loa='country_year',
                                           from_column="vdem_v12_v2xcl_prpty")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xeg_eqprotec", from_loa='country_year',
                                           from_column="vdem_v12_v2xeg_eqprotec")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2x_ex_military", from_loa='country_year',
                                           from_column="vdem_v12_v2x_ex_military")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xcl_dmove", from_loa='country_year',
                                           from_column="vdem_v12_v2xcl_dmove")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2x_clphy", from_loa='country_year',
                                           from_column="vdem_v12_v2x_clphy")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2x_hosabort", from_loa='country_year',
                                           from_column="vdem_v12_v2x_hosabort")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       .with_column(Column("vdem_v2xnp_regcorr", from_loa='country_year',
                                           from_column="vdem_v12_v2xnp_regcorr")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.missing.fill()
                                    )

                       # Spatial lags

                       .with_column(Column("splag_vdem_v2x_libdem", from_loa='country_year',
                                           from_column="vdem_v12_v2x_libdem")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_vdem_v2xcl_dmove", from_loa='country_year',
                                           from_column="vdem_v12_v2xcl_dmove")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_vdem_v2x_accountability", from_loa='country_year',
                                           from_column="vdem_v12_v2x_accountability")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_vdem_v2xpe_exlsocgr", from_loa='country_year',
                                           from_column="vdem_v12_v2xpe_exlsocgr")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_column(Column("splag_vdem_v2xcl_rol", from_loa='country_year',
                                           from_column="vdem_v12_v2xcl_rol")
                                    .transform.missing.fill()
                                    .transform.temporal.tlag(12)
                                    .transform.spatial.countrylag(1, 1, 0, 0)
                                    .transform.missing.replace_na()
                                    )

                       .with_theme("fatalities")
                       .describe("""Predicting ln(fatalities), cm level

                                 Queryset with many features from various sources, long version

                                 """)
                       )

    qs_faostat_stub = (Queryset("fatalities002_faostat_stub", "country_month")

                   .with_column(Column("gleditsch_ward", from_loa="country", from_column="gwcode")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                )

                   # From FAOstat
                   .with_column(Column("consumer_prices_food_indices", from_loa="country_month",
                                       from_column="consumer_prices_food_indices")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("consumer_prices_general_indices", from_loa="country_month",
                                       from_column="consumer_prices_general_indices")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("food_price_inflation", from_loa="country_month",
                                       from_column="food_price_inflation")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("avg_adequate_diet", from_loa="country_year",
                                       from_column="avg_adequate_diet")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("avg_animalprotein_pcap_day", from_loa="country_year",
                                       from_column="avg_animalprotein_pcap_day")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("avg_fprod_value", from_loa="country_year",
                                       from_column="avg_fprod_value")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("avg_protein_pcap_day", from_loa="country_year",
                                       from_column="avg_protein_pcap_day")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("gdp_pc_ppp", from_loa="country_year", from_column="gdp_pc_ppp")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("kcal_pcap_day", from_loa="country_year", from_column="kcal_pcap_day")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("kcal_pcap_day_cerotu", from_loa="country_year",
                                       from_column="kcal_pcap_day_cerotu")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pcap_fprod_var", from_loa="country_year", from_column="pcap_fprod_var")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pcap_fsupply_var", from_loa="country_year",
                                       from_column="pcap_fsupply_var")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_arable_land", from_loa="country_year",
                                       from_column="pct_arable_land")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_cereal_import", from_loa="country_year",
                                       from_column="pct_cereal_import")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_fimport_merch", from_loa="country_year",
                                       from_column="pct_fimport_merch")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_modsevere_finsecurity", from_loa="country_year",
                                       from_column="pct_modsevere_finsecurity")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_pop_basicdrink", from_loa="country_year",
                                       from_column="pct_pop_basicdrink")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_pop_basicsani", from_loa="country_year",
                                       from_column="pct_pop_basicsani")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_pop_safedrink", from_loa="country_year",
                                       from_column="pct_pop_safedrink")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_pop_safesani", from_loa="country_year",
                                       from_column="pct_pop_safesani")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_severe_finsecurity", from_loa="country_year",
                                       from_column="pct_severe_finsecurity")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_und5_overweight", from_loa="country_year",
                                       from_column="pct_und5_overweight")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_und5_stunted", from_loa="country_year",
                                       from_column="pct_und5_stunted")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_und5_wasting", from_loa="country_year",
                                       from_column="pct_und5_wasting")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pct_undernourished", from_loa="country_year",
                                       from_column="pct_undernourished")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pol_stability", from_loa="country_year", from_column="pol_stability")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pop_modsevere_finsecurity", from_loa="country_year",
                                       from_column="pop_modsevere_finsecurity")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pop_severe_finsecurity", from_loa="country_year",
                                       from_column="pop_severe_finsecurity")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("pop_undernourished", from_loa="country_year",
                                       from_column="pop_undernourished")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("prev_adult_obesity", from_loa="country_year",
                                       from_column="prev_adult_obesity")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("prev_infant_bfeed", from_loa="country_year",
                                       from_column="prev_infant_bfeed")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("prev_lowbweight", from_loa="country_year",
                                       from_column="prev_lowbweight")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("prev_repr_anemia", from_loa="country_year",
                                       from_column="prev_repr_anemia")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_column(Column("rail_density", from_loa="country_year", from_column="rail_density")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_theme("production")
                   .describe("""Production conflict history, cm level

                             Predicting ged gte 25 with features from FAOstat

                             """)

                   )

    qs_faoprices_stub = (Queryset("fatalities002_faoprices_stub", "country_month")

                     .with_column(Column("gleditsch_ward", from_loa="country", from_column="gwcode")
                                  .transform.missing.fill()
                                  .transform.missing.replace_na()
                                  )

                     # From FAO food price data - prices and 12-month changes
                     .with_column(Column("fao_wheat_price", from_loa="country_month", from_column="wheat_price")
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("delta_fao_wheat_price", from_loa="country_month",
                                         from_column="wheat_price")
                                  .transform.temporal.delta(12)
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("fao_mp_price", from_loa="country_month", from_column="mp_price")
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("delta_fao_mp_price", from_loa="country_month", from_column="mp_price")
                                  .transform.temporal.delta(12)
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("fao_sugar_price", from_loa="country_month", from_column="sugar_price")
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("delta_fao_sugar_price", from_loa="country_month",
                                         from_column="sugar_price")
                                  .transform.temporal.delta(12)
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("fao_meat_price", from_loa="country_month", from_column="meat_price")
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("delta_fao_meat_price", from_loa="country_month",
                                         from_column="meat_price")
                                  .transform.temporal.delta(12)
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("fao_milk_price", from_loa="country_month", from_column="milk_price")
                                  .transform.missing.replace_na(0)
                                  )

                     .with_column(Column("delta_fao_milk_price", from_loa="country_month",
                                         from_column="milk_price")
                                  .transform.temporal.delta(12)
                                  .transform.missing.replace_na(0)
                                  )

                     .with_theme("production")
                     .describe("""Production conflict history, cm level

                               Predicting ged gte 25 with features from FAO food prices

                               """)

                     )

    qs_imfweo_stub = (Queryset("fatalities002_imfweo_stub", "country_month")

                  .with_column(Column("gleditsch_ward", from_loa="country", from_column="gwcode")
                               .transform.missing.fill()
                               .transform.missing.replace_na()
                               )

                  # IMF WEO
                  .with_column(Column("imfweo_ngdp_rpch_tcurrent", from_loa="country_month",
                                      from_column="ngdp_rpch_tcurrent")
                               .transform.missing.replace_na(0)
                               )

                  .with_column(Column("imfweo_ngdp_rpch_tmin1", from_loa="country_month",
                                      from_column="ngdp_rpch_tmin1")
                               .transform.missing.replace_na(0)
                               )

                  .with_column(Column("imfweo_ngdp_rpch_tplus1", from_loa="country_month",
                                      from_column="ngdp_rpch_tplus1")
                               .transform.missing.replace_na(0)
                               )

                  .with_column(Column("imfweo_ngdp_rpch_tplus2", from_loa="country_month",
                                      from_column="ngdp_rpch_tplus2")
                               .transform.missing.replace_na(0)
                               )

                  .with_theme("production")
                  .describe("""Production conflict history, cm level

                            Predicting ged gte 25 with features from IMF/WEO growth forecasts
                            """)
                  )
    ###################################################################################################################

# Combined querysets
    # Topics model and baseline

    qs_topics = Queryset.from_merger([qs_baseline,qs_topics_stub],
                                      name="fatalities002_topics",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and Mueller & Rauh topic model features
    
                             """)

    data = qs_topics.publish().fetch()

    ###################################################################################################################
    # Aquastat model and baseline

    qs_aquastat = Queryset.from_merger([qs_baseline,qs_aquastat_stub],
                                      name="fatalities002_aquastat",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and aquastat features
    
                             """)

    data = qs_aquastat.publish().fetch()
    ###################################################################################################################
    # Conflict history model and baseline

    qs_conflict = Queryset.from_merger([qs_baseline,qs_conflict_stub],
                                      name="fatalities002_conflict_history",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and first set of conflict history features
    
                             """)

    data = qs_conflict.publish().fetch()

    ###################################################################################################################
    # Conflict history model, extension, and baseline

    qs_conflict_long = Queryset.from_merger([qs_conflict,qs_conflict_ext],
                                      name="fatalities002_conflict_history_long",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline, first set and extended set of conflict history features
    
                             """)
    
    data = qs_conflict_long.publish().fetch()

    ###################################################################################################################
    # Vdem short model and baseline

    qs_vdem_short = Queryset.from_merger([qs_baseline,qs_vdem_short_stub],
                                      name="fatalities002_vdem_short",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and short list of vdem features
    
                             """)

    data = qs_vdem_short.publish().fetch()

    ###################################################################################################################
    # WDI short model and baseline

    qs_wdi_short = Queryset.from_merger([qs_baseline,qs_wdi_short_stub],
                                      name="fatalities002_wdi_short",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and short list of wdi features
    
                             """)

    data = qs_wdi_short.publish().fetch()

    ###################################################################################################################
    # joint broad model and baseline

    qs_joint_broad = Queryset.from_merger([qs_baseline,qs_joint_broad_stub],
                                      name="fatalities002_joint_broad",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and broad list of features from all sources
    
                             """)
    
    data = qs_joint_broad.publish().fetch()

    ###################################################################################################################
    # faostat model and baseline

    qs_faostat = Queryset.from_merger([qs_baseline,qs_faostat_stub],
                                      name="fatalities002_faostat",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and faostat features
    
                             """)
    
    data = qs_faostat.publish().fetch()

    ###################################################################################################################
    # faoprices model and baseline

    qs_faoprices = Queryset.from_merger([qs_baseline,qs_faoprices_stub],
                                      name="fatalities002_faoprices",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and faoprices features
    
                             """)
    
    data = qs_faoprices.publish().fetch()

    ##################################################################################################################
    # imfweo model and baseline

    qs_imfweo = Queryset.from_merger([qs_baseline,qs_imfweo_stub],
                                      name="fatalities002_imfweo",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with baseline and imfweo features
    
                             """)
    
    data = qs_imfweo.publish().fetch()

    ###################################################################################################################
    # All features model

    qs_all_features = Queryset.from_merger([qs_baseline,
                                            qs_conflict_stub,
                                            qs_topics_stub,
                                            qs_wdi_short_stub,
                                            qs_vdem_short_stub,
                                            qs_aquastat_stub
                                           ],
                                      name="fatalities002_all_features",
                                      theme="fatalities002",
                                      description="""Predicting ln(fatalities), cm level
    
                             Queryset with all features
    
                             """)

    data = qs_all_features.publish()

    ###################################################################################################################
    # Collecting combined queryset objects in a list

    qslist = [
              qs_baseline,
              qs_topics,
              qs_aquastat,
              qs_conflict,
              qs_conflict_long,
              qs_vdem_short,
              qs_wdi_short,
              qs_all_features,
              qs_joint_narrow,
              qs_joint_broad,
              qs_faostat,
              qs_faoprices,
              qs_imfweo
              ]

    return qslist
