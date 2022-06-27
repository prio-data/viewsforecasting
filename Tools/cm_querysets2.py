# # Specifying querysets for use in Predicting Fatalities project
# Fatalities002 version
# ## cm level
# 
# 

# ## Importing modules


# Basics
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
# sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
# Views 3
from viewser.operations import fetch
from viewser import Queryset, Column
import views_runs
from views_partitioning import data_partitioner, legacy
from stepshift import views
import views_dataviz

qs_baseline = (Queryset("fatalities002_baseline", "country_month")

    # target variable
    .with_column(Column("ln_ged_sb_dep", from_table = "ged2_cm", from_column = "ged_sb_best_sum_nokgi")
                 .transform.ops.ln()
                 .transform.missing.fill()
                )                   

    # timelag 0 of target variable
    .with_column(Column("ln_ged_sb", from_table = "ged2_cm", from_column = "ged_sb_best_sum_nokgi")
                 .transform.ops.ln()
                 .transform.missing.fill()
                )
    # Decay functions
    # sb
    .with_column(Column("decay_ged_sb_5", from_table = "ged2_cm", from_column = "ged_sb_best_sum_nokgi")
                 .transform.missing.replace_na()
                 .transform.bool.gte(5)
                 .transform.temporal.time_since()
                 .transform.temporal.decay(24)
                 .transform.missing.replace_na()
                )
     # os
    .with_column(Column("decay_ged_os_5", from_table = "ged2_cm", from_column = "ged_os_best_sum_nokgi")
                 .transform.missing.replace_na()
                 .transform.bool.gte(5)
                 .transform.temporal.time_since()
                 .transform.temporal.decay(24)
                 .transform.missing.replace_na()
                )
    # Spatial lag decay
    .with_column(Column("splag_1_decay_ged_sb_5", from_table = "ged2_cm", from_column = "ged_sb_best_sum_nokgi")
                 .transform.missing.replace_na()
                 .transform.bool.gte(5)
                 .transform.temporal.time_since()
                 .transform.temporal.decay(24)
                 .transform.spatial.countrylag(1,1,0,0)
                 .transform.missing.replace_na()
                )


     # From WDI
        .with_column(Column("wdi_sp_pop_totl", from_table = "wdi_cy", from_column = "wdi_sp_pop_totl")
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

print(f"fatalities002_baseline; "
      f"A dataset with {len(data.columns)} columns, with "
      f"data between t {min(data.index.get_level_values(0))} "
      f"and {max(data.index.get_level_values(0))}. "
      f"({len(np.unique(data.index.get_level_values(1)))} units)"
     )


#Mueller & Rauh topic model features
#tlag 1 variables

qs_topics_stub = (Queryset("fatalities002_topics_stub", "country_month")

         
    #Topic 0, religious tensions: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic0_religion_t1', from_table='topic_cm', from_column = 'topic_religion') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic0_religion_t13', from_table='topic_cm', from_column = 'topic_religion') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic0_religion_t1_stock', from_table='topic_cm', from_column = 'topic_religion') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    
    #Topic 1, politics, original: tlag1, 12 month moving average on tlag1
    .with_column(Column('topic1_politics_t1', from_table='topic_cm', from_column = 'topic_politics') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic1_politics_t13', from_table='topic_cm', from_column = 'topic_politics') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic1_politics_t1_stock', from_table='topic_cm', from_column = 'topic_politics') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    
    #Topic 2, diplomacy and sanctions: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic2_sanctions_t1', from_table='topic_cm', from_column = 'topic_sanctions') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic2_sanctions_t13', from_table='topic_cm', from_column = 'topic_sanctions') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic2_sanctions_t1_stock', from_table='topic_cm', from_column = 'topic_sanctions') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 3, civilian life: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic3_life_t1', from_table='topic_cm', from_column = 'topic_life') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic3_life_t13', from_table='topic_cm', from_column = 'topic_life') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic3_life_t1_stock', from_table='topic_cm', from_column = 'topic_life') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 4, energy and industry: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic4_energy_t1', from_table='topic_cm', from_column = 'topic_energy') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic4_energy_t13', from_table='topic_cm', from_column = 'topic_energy') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic4_energy_t1_stock', from_table='topic_cm', from_column = 'topic_energy') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 5, media and reporting: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic5_media_t1', from_table='topic_cm', from_column = 'topic_media') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic5_media_t13', from_table='topic_cm', from_column = 'topic_media') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic5_media_t1_stock', from_table='topic_cm', from_column = 'topic_media') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 6, economics: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic6_economics_t1', from_table='topic_cm', from_column = 'topic_economics') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic6_economics_t13', from_table='topic_cm', from_column = 'topic_economics') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic6_economics_t1_stock', from_table='topic_cm', from_column = 'topic_economics') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 7, health and emergencies: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic7_health_t1', from_table='topic_cm', from_column = 'topic_health') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic7_health_t13', from_table='topic_cm', from_column = 'topic_health') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic7_health_t1_stock', from_table='topic_cm', from_column = 'topic_health') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 8, chinese politics: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic8_china_t1', from_table='topic_cm', from_column = 'topic_china') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic8_china_t13', from_table='topic_cm', from_column = 'topic_china') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic8_china_t1_stock', from_table='topic_cm', from_column = 'topic_china') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 9, foreign policy: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic9_foreign_t1', from_table='topic_cm', from_column = 'topic_foreign') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic9_foreign_t13', from_table='topic_cm', from_column = 'topic_foreign') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic9_foreign_t1_stock', from_table='topic_cm', from_column = 'topic_foreign') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 10, armed conflict: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic10_conflict_t1', from_table='topic_cm', from_column = 'topic_conflict') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic10_conflict_t13', from_table='topic_cm', from_column = 'topic_conflict') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic10_conflict_t1_stock', from_table='topic_cm', from_column = 'topic_conflict') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 11, diplomacy: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic11_diplomacy_t1', from_table='topic_cm', from_column = 'topic_diplomacy') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic11_diplomacy_t13', from_table='topic_cm', from_column = 'topic_diplomacy') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic11_diplomacy_t1_stock', from_table='topic_cm', from_column = 'topic_diplomacy') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 12, power and negotiation: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic12_power_t1', from_table='topic_cm', from_column = 'topic_power') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic12_power_t13', from_table='topic_cm', from_column = 'topic_power') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic12_power_t1_stock', from_table='topic_cm', from_column = 'topic_power') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 13, sports: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic13_sports_t1', from_table='topic_cm', from_column = 'topic_sports') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic13_sports_t13', from_table='topic_cm', from_column = 'topic_sports') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic13_sports_t1_stock', from_table='topic_cm', from_column = 'topic_sports') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
    #Topic 14, judiciary and abuses: original, tlag1, 12 month moving average on tlag1
    .with_column(Column('topic14_judiciary_t1', from_table='topic_cm', from_column = 'topic_judiciary') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill())
    .with_column(Column('topic14_judiciary_t13', from_table='topic_cm', from_column = 'topic_judiciary') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(13)
                .transform.missing.fill())
    .with_column(Column('topic14_judiciary_t1_stock', from_table='topic_cm', from_column = 'topic_judiciary') 
                .transform.missing.fill()
                .transform.missing.replace_na()
                .transform.temporal.tlag(1)
                .transform.missing.fill()
                .transform.temporal.moving_average(12)
                .transform.missing.fill()
                )
        .with_theme("fatalities")
        .describe("""Predicting ln(fatalities), cm level

        Queryset with Mueller & Rauh topic model features

    """)
        )

data = qs_topics_stub.publish().fetch()

print(f"fatalities002_topics_stub; "
      f"A dataset with {len(data.columns)} columns, with "
      f"data between t {min(data.index.get_level_values(0))} "
      f"and {max(data.index.get_level_values(0))}. "
      f"({len(np.unique(data.index.get_level_values(1)))} units)"
     )

# Combined querysets
# Topics model and baseline

qs_topics = (Queryset("fatalities002_topics", "country_month")
        .with_theme("fatalities002")
        .describe("""Predicting ln(fatalities), cm level

        Queryset with baseline and Mueller & Rauh topic model features

        """)
        )
qs_topics.operations = qs_baseline.operations[0:] + qs_topics_stub.operations[0:]

#data = qs_topics.publish().fetch()

qslist = [qs_baseline,qs_topics]

