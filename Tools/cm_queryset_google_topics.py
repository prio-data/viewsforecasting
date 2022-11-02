#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Basics
import numpy as np

# Views 3
from viewser.operations import fetch
from viewser import Queryset, Column



# In[2]:


print("Baseline queryset pushed forward from the fatalities002, new updated version.\n Topics has been slightly changed to reflect the new time lag. Note in the future we should be able to tlag by 1 only as for example, by September 7th we should have all data for October. So technically ahead of the ucdp update schedule. For right now, though, we have data through July so given that we are running the model in October I lagged the value by 3 instead of 1. I converted the 1 year lag to 15 months, and then replaced the running average by 3 month lag with stock over 12. Note that the running average is not the exact version as is calculated by Rauh and Muller team but a stand in. Additional variables will be added.\n Google trends has similarly been lagged to reflect the last available data is August. There might be something wrong with my querysets where the NAs are getting autofilled with 0s when querying. So, I am setting the google_index value by tlag 2. \n Internet usage is available at country-year level, but through 2020 only. So lag by 2 years or 24 months.\n I have borrowed the population from features where t12 lag wdi_cy version has been used.\n Something interesting to note, queryset for google trends does not seem to have NAs inserted, but NAs appear in the datagrip. there does not seem to be an automatic fill zeros so I am not sure what caused the queryset on this data to insert the zeroes. Could not test and figure out more reasons. I have additionally made to sure to use the missing fill on all the querysets.")


# In[ ]:


def get_cm_querysets():

    qs_baseline = (Queryset("fat_dev_mc_media_baseline", "country_month")

                   # target variable
                   .with_column(Column("ln_ged_sb_dep", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )

                   # timelag 0 of target variable
                   .with_column(Column("ln_ged_sb", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                                .transform.ops.ln()
                                .transform.missing.fill()
                                )
                   # Decay functions
                   # sb
                   .with_column(Column("decay_ged_sb_5", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                .transform.missing.fill()
                                )
                   # os
                   .with_column(Column("decay_ged_os_5", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.missing.replace_na()
                                .transform.missing.fill()
                                )
                   # Spatial lag decay
                   .with_column(Column("splag_1_decay_ged_sb_5", from_table="ged2_cm",
                                       from_column="ged_sb_best_sum_nokgi")
                                .transform.missing.replace_na()
                                .transform.bool.gte(5)
                                .transform.temporal.time_since()
                                .transform.temporal.decay(24)
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                .transform.missing.fill()
                                )

                   # From 
                   
                   .with_column(Column("wdi_sp_pop_totl", from_table="wdi_cy", from_column="wdi_sp_pop_totl")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill()
                                )

                   .with_theme("fatalities")
                   .describe("""Fatalities conflict history, cm level
    
                   Predicting ln(fatalities) using conflict predictors, ultrashort
    
                             """)
                   )

    data = qs_baseline.publish().fetch()

    print(f"fat_dev_mc_media_baseline; "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )

    
    ###################################################################################################################
    # Mueller & Rauh topic model features
    # this is a version used for MC presentation

    qs_topics_stub = (Queryset("fat_dev_mc_media_topics_stub", "country_month")

                      # Topic 0, religious tensions: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic0_religion_t3', from_table='topic_cm', from_column='topic_religion')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic0_religion_t15', from_table='topic_cm', from_column='topic_religion')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic0_religion_t3_stock', from_table='topic_cm',
                                          from_column='topic_religion')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )
                      .with_column(Column('splag_topic1_religion_t3_stock', from_table='topic_cm',
                                          from_column='topic_religion')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 1, politics, original: tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic1_politics_t3', from_table='topic_cm', from_column='topic_politics')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic1_politics_t15', from_table='topic_cm', from_column='topic_politics')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic1_politics_t3_stock', from_table='topic_cm',
                                          from_column='topic_politics')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic2_politics_t3_stock', from_table='topic_cm',
                                          from_column='topic_politics')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 2, diplomacy and sanctions: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic2_sanctions_3', from_table='topic_cm', from_column='topic_sanctions')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic2_sanctions_t15', from_table='topic_cm', from_column='topic_sanctions')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic2_sanctions_t3_stock', from_table='topic_cm',
                                          from_column='topic_sanctions')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic2_sanctions_t3_stock', from_table='topic_cm',
                                          from_column='topic_sanctions')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 3, civilian life: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic3_life_t3', from_table='topic_cm', from_column='topic_life')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic3_life_t15', from_table='topic_cm', from_column='topic_life')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )
                      .with_column(Column('topic3_life_t3_stock', from_table='topic_cm', from_column='topic_life')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic3_life_t3_stock', from_table='topic_cm', from_column='topic_life')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(15)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 4, energy and industry: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic4_energy_t3', from_table='topic_cm', from_column='topic_energy')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic4_energy_t15', from_table='topic_cm', from_column='topic_energy')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic4_energy_t3_stock', from_table='topic_cm', from_column='topic_energy')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic4_energy_t3_stock', from_table='topic_cm',
                                          from_column='topic_energy')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 5, media and reporting: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic5_media_t3', from_table='topic_cm', from_column='topic_media')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic5_media_t15', from_table='topic_cm', from_column='topic_media')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic5_media_t3_stock', from_table='topic_cm', from_column='topic_media')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic5_media_t3_stock', from_table='topic_cm',
                                          from_column='topic_media')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 6, economics: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic6_economics_t3', from_table='topic_cm', from_column='topic_economics')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic6_economics_t15', from_table='topic_cm', from_column='topic_economics')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic6_economics_t3_stock', from_table='topic_cm',
                                          from_column='topic_economics')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic6_economics_t3_stock', from_table='topic_cm',
                                          from_column='topic_economics')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 7, health and emergencies: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic7_health_t3', from_table='topic_cm', from_column='topic_health')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic7_health_t15', from_table='topic_cm', from_column='topic_health')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic7_health_t3_stock', from_table='topic_cm', from_column='topic_health')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic7_health_t3_stock', from_table='topic_cm',
                                          from_column='topic_health')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 8, chinese politics: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic8_china_t3', from_table='topic_cm', from_column='topic_china')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic8_china_t15', from_table='topic_cm', from_column='topic_china')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic8_china_t3_stock', from_table='topic_cm', from_column='topic_china')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic8_china_t3_stock', from_table='topic_cm',
                                          from_column='topic_china')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 9, foreign policy: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic9_foreign_t3', from_table='topic_cm', from_column='topic_foreign')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic9_foreign_t15', from_table='topic_cm', from_column='topic_foreign')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic9_foreign_t3_stock', from_table='topic_cm',
                                          from_column='topic_foreign')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic9_foreign_t3_stock', from_table='topic_cm',
                                          from_column='topic_foreign')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 10, armed conflict: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic10_conflict_t3', from_table='topic_cm', from_column='topic_conflict')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic10_conflict_t15', from_table='topic_cm', from_column='topic_conflict')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic10_conflict_t3_stock', from_table='topic_cm',
                                          from_column='topic_conflict')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic10_conflict_t3_stock', from_table='topic_cm',
                                          from_column='topic_conflict')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 11, diplomacy: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic11_diplomacy_t3', from_table='topic_cm', from_column='topic_diplomacy')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic11_diplomacy_t15', from_table='topic_cm', from_column='topic_diplomacy')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic11_diplomacy_t3_stock', from_table='topic_cm',
                                          from_column='topic_diplomacy')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic11_diplomacy_t3_stock', from_table='topic_cm',
                                          from_column='topic_diplomacy')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 12, power and negotiation: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic12_power_t3', from_table='topic_cm', from_column='topic_power')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic12_power_t15', from_table='topic_cm', from_column='topic_power')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic12_power_t3_stock', from_table='topic_cm', from_column='topic_power')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic12_power_t3_stock', from_table='topic_cm',
                                          from_column='topic_power')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 13, sports: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic13_sports_t3', from_table='topic_cm', from_column='topic_sports')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic13_sports_t15', from_table='topic_cm', from_column='topic_sports')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic13_sports_t3_stock', from_table='topic_cm', from_column='topic_sports')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic13_sports_t3_stock', from_table='topic_cm',
                                          from_column='topic_sports')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )

                      # Topic 14, judiciary and abuses: original, tlag1, 12 month moving average on tlag1
                      .with_column(Column('topic14_judiciary_t3', from_table='topic_cm', from_column='topic_judiciary')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic14_judiciary_t15', from_table='topic_cm', from_column='topic_judiciary')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(15)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('topic14_judiciary_t3_stock', from_table='topic_cm',
                                          from_column='topic_judiciary')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   )

                      .with_column(Column('splag_topic14_judiciary_t3_stock', from_table='topic_cm',
                                          from_column='topic_judiciary')
                                   .transform.missing.fill()
                                   .transform.missing.replace_na()
                                   .transform.temporal.tlag(3)
                                   .transform.missing.fill()
                                   .transform.temporal.moving_average(12)
                                   .transform.missing.fill()
                                   .transform.spatial.countrylag(1, 1, 0, 0)
                                   .transform.missing.replace_na()
                                   .transform.missing.fill()
                                   )
                      .with_theme("fatalities")
                      .describe("""Predicting ln(fatalities), cm level
    
                                Stub queryset with Mueller & Rauh topic model features
    
                                """)
                      )

    data = qs_topics_stub.publish().fetch()

    print(f"fat_dev_mc_media_topics_stub; "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )
    
    ###Google trends and internet use queryset###

    qs_google_internet_stub = (Queryset("fat_dev_mc_media_google_internet_stub", "country_month")

                   # population
                   .with_column(Column("wdi_sp_pop_totl", from_table = "wdi_cy", from_column = "wdi_sp_pop_totl")
                                .transform.missing.fill()
                                .transform.temporal.tlag(12)
                                .transform.missing.fill())  

                   #google trends
                   .with_column(Column("google_index_conflict_t2", from_table="google_trend_cm", from_column="google_index_conflict")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )
                    
                   .with_column(Column("google_index_conflict_t14", from_table="google_trend_cm", from_column="google_index_conflict")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(14)
                                .transform.missing.fill()
                                )
                    .with_column(Column("google_index_conflict_t2_ra", from_table="google_trend_cm", from_column="google_index_conflict")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                .transform.temporal.moving_average(12)
                                .transform.missing.fill()
                                )
                    .with_column(Column("google_index_conflict_t2_ra_splag", from_table="google_trend_cm", from_column="google_index_conflict")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(3)
                                .transform.missing.fill()
                                .transform.temporal.moving_average(12)
                                .transform.missing.fill()
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                .transform.missing.fill()
                                )
                    .with_column(Column("google_index_war_t2", from_table="google_trend_cm", from_column="google_index_war")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                )
                    
                   .with_column(Column("google_index_war_t14", from_table="google_trend_cm", from_column="google_index_war")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(14)
                                .transform.missing.fill()
                                )
                    .with_column(Column("google_index_war_t2_ra", from_table="google_trend_cm", from_column="google_index_war")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(2)
                                .transform.missing.fill()
                                .transform.temporal.moving_average(12)
                                .transform.missing.fill()
                                )
                    .with_column(Column("google_index_war_t2_ra_splag", from_table="google_trend_cm", from_column="google_index_war")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(3)
                                .transform.missing.fill()
                                .transform.temporal.moving_average(12)
                                .transform.missing.fill()
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                .transform.missing.fill()
                                )
                    #internet usage
                    .with_column(Column("internet_t24", from_table="internet_usage_our_world_data_cy", from_column="owd_pop_internet_percent")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(24)
                                .transform.missing.fill()
                                )
                    
                   .with_column(Column("internet_t36", from_table="internet_usage_our_world_data_cy", from_column="owd_pop_internet_percent")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(36)
                                .transform.missing.fill()
                                )
                    .with_column(Column("internet_t24_ra", from_table="internet_usage_our_world_data_cy", from_column="owd_pop_internet_percent")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(24)
                                .transform.missing.fill()
                                .transform.temporal.moving_average(12)
                                .transform.missing.fill()
                                )
                    .with_column(Column("internet_t24_ra_splag", from_table="internet_usage_our_world_data_cy", from_column="owd_pop_internet_percent")
                                .transform.missing.fill()
                                .transform.missing.replace_na()
                                .transform.temporal.tlag(24)
                                .transform.missing.fill()
                                .transform.temporal.moving_average(12)
                                .transform.missing.fill()
                                .transform.spatial.countrylag(1, 1, 0, 0)
                                .transform.missing.replace_na()
                                .transform.missing.fill()
                                )

                   .with_theme("fatalities")
                   .describe("""Fatalities conflict history, cm level
    
                   Predicting ln(fatalities) using conflict predictors, ultrashort
    
                             """)
                   )

    data = qs_google_internet_stub.publish().fetch()

    print(f"fat_dev_mc_media_google_internet_stub; "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )
    
    # topics model

    qs_topics = (Queryset("fat_dev_mc_media_topics", "country_month")
                 .with_theme("fatalities")
                 .describe("""Predicting ln(fatalities), cm level

                           """)

                 )

    qs_topics.operations = qs_baseline.operations[0:] + qs_topics_stub.operations[0:]

    data = qs_topics.publish().fetch()
    
    
    #google and internet models

    qs_google_internet = (Queryset("fat_dev_mc_media_google_internet", "country_month")
                 .with_theme("fatalities")
                 .describe("""Predicting ln(fatalities), cm level

                           """)

                 )

    qs_google_internet.operations = qs_baseline.operations[0:] + qs_google_internet_stub.operations[0:]

    data = qs_google_internet.publish().fetch()
    
    
    
    ###################################################################################################################
    # All features model

    qs_all_features = (Queryset("fat_dev_mc_media_all_features", "country_month")
                       .with_theme("fatalities")
                       .describe("""Predicting ln(fatalities), cm level
    
                                 """)
                       )

    qs_all_features.operations = qs_baseline.operations[0:] \
        + qs_topics_stub.operations[0:] \
        + qs_google_internet_stub.operations[0:] \

    data = qs_all_features.publish()
    
    qslist = [
        qs_baseline,
        qs_topics,
        qs_google_internet, 
        qs_all_features]

    return qslist

