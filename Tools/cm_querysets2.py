# # Specifying querysets for use in Predicting Fatalities project
# Fatalities002 version
# ## cm level
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


#######################################################################################################################

def get_cm_querysets():

    qs_baseline = (Queryset("fatalities002_baseline", "country_month")

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
                     )
         # os
        .with_column(Column("decay_ged_os_5", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        # Spatial lag decay
        .with_column(Column("splag_1_decay_ged_sb_5", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     .transform.missing.replace_na()
                     )

        # From WDI
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

    print(f"fatalities002_baseline; "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )

    #######################################################################################################################
    # Mueller & Rauh topic model features
    # tlag 1 variables

    qs_topics_stub = (Queryset("fatalities002_topics_stub", "country_month")

        # Topic 0, religious tensions: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic0_religion_t1', from_table='topic_cm', from_column='topic_religion')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     )

        .with_column(Column('topic0_religion_t13', from_table='topic_cm', from_column='topic_religion')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill()
                     )

        .with_column(Column('topic0_religion_t1_stock', from_table='topic_cm', from_column='topic_religion')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )

        # Topic 1, politics, original: tlag1, 12 month moving average on tlag1
        .with_column(Column('topic1_politics_t1', from_table='topic_cm', from_column='topic_politics')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic1_politics_t13', from_table='topic_cm', from_column='topic_politics')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic1_politics_t1_stock', from_table='topic_cm', from_column='topic_politics')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )

        # Topic 2, diplomacy and sanctions: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic2_sanctions_t1', from_table='topic_cm', from_column='topic_sanctions')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic2_sanctions_t13', from_table='topic_cm', from_column='topic_sanctions')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic2_sanctions_t1_stock', from_table='topic_cm', from_column='topic_sanctions')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 3, civilian life: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic3_life_t1', from_table='topic_cm', from_column='topic_life')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic3_life_t13', from_table='topic_cm', from_column='topic_life')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic3_life_t1_stock', from_table='topic_cm', from_column='topic_life')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 4, energy and industry: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic4_energy_t1', from_table='topic_cm', from_column='topic_energy')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic4_energy_t13', from_table='topic_cm', from_column='topic_energy')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic4_energy_t1_stock', from_table='topic_cm', from_column='topic_energy')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 5, media and reporting: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic5_media_t1', from_table='topic_cm', from_column='topic_media')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic5_media_t13', from_table='topic_cm', from_column='topic_media')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic5_media_t1_stock', from_table='topic_cm', from_column='topic_media')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 6, economics: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic6_economics_t1', from_table='topic_cm', from_column='topic_economics')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic6_economics_t13', from_table='topic_cm', from_column='topic_economics')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic6_economics_t1_stock', from_table='topic_cm', from_column='topic_economics')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 7, health and emergencies: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic7_health_t1', from_table='topic_cm', from_column='topic_health')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic7_health_t13', from_table='topic_cm', from_column='topic_health')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic7_health_t1_stock', from_table='topic_cm', from_column='topic_health')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 8, chinese politics: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic8_china_t1', from_table='topic_cm', from_column='topic_china')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic8_china_t13', from_table='topic_cm', from_column='topic_china')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic8_china_t1_stock', from_table='topic_cm', from_column='topic_china')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 9, foreign policy: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic9_foreign_t1', from_table='topic_cm', from_column='topic_foreign')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic9_foreign_t13', from_table='topic_cm', from_column='topic_foreign')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic9_foreign_t1_stock', from_table='topic_cm', from_column='topic_foreign')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 10, armed conflict: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic10_conflict_t1', from_table='topic_cm', from_column='topic_conflict')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic10_conflict_t13', from_table='topic_cm', from_column='topic_conflict')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic10_conflict_t1_stock', from_table='topic_cm', from_column='topic_conflict')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 11, diplomacy: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic11_diplomacy_t1', from_table='topic_cm', from_column='topic_diplomacy')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic11_diplomacy_t13', from_table='topic_cm', from_column='topic_diplomacy')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic11_diplomacy_t1_stock', from_table='topic_cm', from_column='topic_diplomacy')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 12, power and negotiation: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic12_power_t1', from_table='topic_cm', from_column='topic_power')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic12_power_t13', from_table='topic_cm', from_column='topic_power')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic12_power_t1_stock', from_table='topic_cm', from_column='topic_power')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 13, sports: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic13_sports_t1', from_table='topic_cm', from_column='topic_sports')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic13_sports_t13', from_table='topic_cm', from_column='topic_sports')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic13_sports_t1_stock', from_table='topic_cm', from_column='topic_sports')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        # Topic 14, judiciary and abuses: original, tlag1, 12 month moving average on tlag1
        .with_column(Column('topic14_judiciary_t1', from_table='topic_cm', from_column='topic_judiciary')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill())
        .with_column(Column('topic14_judiciary_t13', from_table='topic_cm', from_column='topic_judiciary')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(13)
                     .transform.missing.fill())
        .with_column(Column('topic14_judiciary_t1_stock', from_table='topic_cm', from_column='topic_judiciary')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     .transform.temporal.moving_average(12)
                     .transform.missing.fill()
                     )
        .with_theme("fatalities")
        .describe("""Predicting ln(fatalities), cm level
    
            Stub queryset with Mueller & Rauh topic model features
    
        """)
            )

    data = qs_topics_stub.publish().fetch()

    print(f"fatalities002_topics_stub; "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
         )

    #######################################################################################################################
    qs_aquastat_stub = (Queryset("fatalities002_aquastat_stub", "country_month")

        # Agricultural water withdrawal as % of total renewable water resources [%]
        .with_column(Column('agr_withdrawal_pct_t48', from_table='fao_aqua_cy', from_column='agr_withdrawal_pct')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # Dam capacity per capita [m3/inhab]
        .with_column(Column('dam_cap_pcap_t48', from_table='fao_aqua_cy', from_column='dam_cap_pcap')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # Groundwater: leaving the country to other countries (total) [10^9 m3/year]
        .with_column(Column('groundwater_export_t48', from_table='fao_aqua_cy', from_column='groundwater_export')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # MDG 7.5. Freshwater withdrawal as % of total renewable water resources [%]
        .with_column(Column('fresh_withdrawal_pct_t48', from_table='fao_aqua_cy', from_column='fresh_withdrawal_pct')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # SDG 6.4.1. Industrial Water Use Efficiency [US$/m3]
        .with_column(Column('ind_efficiency_t48', from_table='fao_aqua_cy', from_column='ind_efficiency')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # SDG 6.4.1. Irrigated Agriculture Water Use Efficiency [US$/m3]
        .with_column(Column('irr_agr_efficiency_t48', from_table='fao_aqua_cy', from_column='irr_agr_efficiency')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # SDG 6.4.1. Services Water Use Efficiency [US$/m3]
        .with_column(Column('services_efficiency_t48', from_table='fao_aqua_cy', from_column='services_efficiency')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # SDG 6.4.1. Water Use Efficiency [US$/m3]
        .with_column(Column('general_efficiency_t48', from_table='fao_aqua_cy', from_column='general_efficiency')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # SDG 6.4.2. Water Stress [%]
        .with_column(Column('water_stress_t48', from_table='fao_aqua_cy', from_column='water_stress')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # Total internal renewable water resources per capita [m3/inhab/yr]
        .with_column(Column('renewable_internal_pcap_t48', from_table='fao_aqua_cy', from_column='renewable_internal_pcap')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        # Total annual renewable water resources per capita [m3/inhab/year]
        .with_column(Column('renewable_pcap_t48', from_table='fao_aqua_cy', from_column='renewable_pcap')
                     .transform.missing.fill()
                     .transform.missing.replace_na()
                     .transform.temporal.tlag(48)
                     .transform.missing.fill())

        .with_theme("fatalities")
        .describe("""Predicting ln(fatalities), cm level
    
            Queryset based on the FAO AQUASTAT data
    
        """)
            )

    data = qs_aquastat_stub.publish().fetch()

    print(f"fatalities002_aquastat_stub; "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
         )

    #######################################################################################################################

    # ## Shorter conflict history model stub

    # log variables

    qs_conflict_stub = (Queryset("fatalities002_cm_conflict_history_stub", "country_month")

        # Lags
        .with_column(Column("ln_ged_sb_tlag_1", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_ged_sb_tlag_2", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(2)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_ged_sb_tlag_3", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(3)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_ged_sb_tlag_4", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(4)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_ged_sb_tlag_5", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(5)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_ged_sb_tlag_6", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(6)
                     .transform.missing.fill()
                     )
        # Moving sums
        .with_column(Column("ln_ged_sb_tsum_24", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.temporal.moving_sum(24)
                     .transform.ops.ln()
                     .transform.missing.replace_na()
                     )

        # Decay functions
        # sb

        .with_column(Column("decay_ged_sb_100", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(100)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )
        .with_column(Column("decay_ged_sb_500", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(500)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )
        # os

        .with_column(Column("decay_ged_os_100", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(100)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )
        # ns
        .with_column(Column("decay_ged_ns_5", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("decay_ged_ns_100", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(100)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        # Other independent variables
        .with_column(Column("ln_ged_ns", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )
        .with_column(Column("ln_ged_os", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )
        .with_column(Column("ln_acled_sb", from_table="acled2_cm", from_column="acled_sb_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )
        .with_column(Column("ln_acled_sb_count", from_table="acled2_cm", from_column="acled_sb_count")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )
        .with_column(Column("ln_acled_os", from_table="acled2_cm", from_column="acled_os_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )

        # time-lagged by 0-2 independent variables
        .with_column(Column("ln_ged_os_tlag_1", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     )

        # 12-month decay dummy of independent variables
        .with_column(Column("decay_acled_sb_5", from_table="acled2_cm", from_column="acled_sb_fat")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )
        .with_column(Column("decay_acled_os_5", from_table="acled2_cm", from_column="acled_os_fat")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )
        .with_column(Column("decay_acled_ns_5", from_table="acled2_cm", from_column="acled_ns_fat")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        # Spatial lags of decay functions
        .with_column(Column("splag_1_decay_ged_os_5", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("splag_1_decay_ged_ns_5", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     .transform.missing.replace_na()
                     )

        # gwnos
        .with_column(Column("gleditsch_ward", from_table="country", from_column="gwcode")
                     )

        .with_theme("fatalities")
        .describe("""Fatalities conflict history, cm level
    
                Predicting ln(fatalities) using conflict predictors
    
            """)
        )
    data = qs_conflict_stub.publish().fetch()

    print(f"fatalities002_cm_conflict_history_stub; "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
         )

    ########################################################################################################################

    # ## Long conflict history model
    # log variables
    qs_conflict_ext = (Queryset("fatalities002_cm_conflict_history_ext", "country_month")

        # Moving sums
        .with_column(Column("ln_ged_sb_tsum_12", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.temporal.moving_sum(12)
                     .transform.ops.ln()
                     .transform.missing.replace_na()
                     )

        .with_column(Column("ln_ged_sb_tsum_48", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.temporal.moving_sum(48)
                     .transform.ops.ln()
                     .transform.missing.replace_na()
                     )

        # Spatial lags
        .with_column(Column("splag_1_ged_sb", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     )

        .with_column(Column("splag_2_ged_sb", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.spatial.countrylag(1, 2, 0, 0)
                     )

        .with_column(Column("splag_1_ged_os", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     )

        .with_column(Column("splag_1_ged_ns", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     )
        # Decay functions
        # sb
        .with_column(Column("decay_ged_sb_1", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(1)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("decay_ged_sb_25", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(25)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )
        # os
        .with_column(Column("decay_ged_os_1", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(1)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("decay_ged_os_5", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(5)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("decay_ged_os_25", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(25)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("decay_ged_os_500", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(500)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )
        # ns
        .with_column(Column("decay_ged_ns_1", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(1)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("decay_ged_ns_25", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(25)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("decay_ged_ns_500", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(500)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.missing.replace_na()
                     )
        # Spatial lags of decays
        .with_column(Column("splag_1_decay_ged_sb_100", from_table="ged2_cm", from_column="ged_sb_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(100)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("splag_1_decay_ged_os_100", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(100)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     .transform.missing.replace_na()
                     )

        .with_column(Column("splag_1_decay_ged_ns_100", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.missing.replace_na()
                     .transform.bool.gte(100)
                     .transform.temporal.time_since()
                     .transform.temporal.decay(24)
                     .transform.spatial.countrylag(1, 1, 0, 0)
                     .transform.missing.replace_na()
                     )

        # Other independent variables
        .with_column(Column("ln_acled_prx_count", from_table="acled2_cm", from_column="acled_prx_count")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_pr_count", from_table="acled2_cm", from_column="acled_pr_count")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_prx_fat", from_table="acled2_cm", from_column="acled_prx_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_sb_gov", from_table="acled2_cm", from_column="acled_bat_gov_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_sb_reb", from_table="acled2_cm", from_column="acled_bat_reb_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_ns", from_table="acled2_cm", from_column="acled_ns_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     )

        # time-lagged by 0-2 independent variables
        .with_column(Column("ln_ged_ns_tlag_1", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_ged_ns_tlag_2", from_table="ged2_cm", from_column="ged_ns_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(2)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_ged_os_tlag_2", from_table="ged2_cm", from_column="ged_os_best_sum_nokgi")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(2)
                     .transform.missing.fill()
                     )
        .with_column(Column("ln_acled_sb_tlag_1", from_table="acled2_cm", from_column="acled_sb_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_sb_tlag_2", from_table="acled2_cm", from_column="acled_sb_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(2)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_os_tlag_1", from_table="acled2_cm", from_column="acled_os_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_os_tlag_2", from_table="acled2_cm", from_column="acled_os_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(2)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_ns_tlag_1", from_table="acled2_cm", from_column="acled_ns_fat")
                     .transform.ops.ln()
                     .transform.missing.fill()
                     .transform.temporal.tlag(1)
                     .transform.missing.fill()
                     )

        .with_column(Column("ln_acled_ns_tlag_2", from_table="acled2_cm", from_column="acled_os_fat")
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
    data = qs_conflict_ext.publish().fetch()

    print(f"fatalities002_cm_conflict_history_ext; "
          f"A dataset with {len(data.columns)} columns, with "
          f"data between t = {min(data.index.get_level_values(0))} "
          f"and {max(data.index.get_level_values(0))}. "
          f"({len(np.unique(data.index.get_level_values(1)))} units)"
          )


    #######################################################################################################################
    # Combined querysets
    # Topics model and baseline

    qs_topics = (Queryset("fatalities002_topics", "country_month")
                 .with_theme("fatalities002")
                 .describe("""Predicting ln(fatalities), cm level
    
            Queryset with baseline and Mueller & Rauh topic model features
    
            """)
                 )
    qs_topics.operations = qs_baseline.operations[0:] + qs_topics_stub.operations[0:]

    data = qs_topics.publish().fetch()

    #######################################################################################################################
    # Aquastat model and baseline

    qs_aquastat = (Queryset("fatalities002_aquastat", "country_month")
                   .with_theme("fatalities002")
                   .describe("""Predicting ln(fatalities), cm level
    
            Queryset with baseline and aquastat features
    
            """)
                   )
    qs_aquastat.operations = qs_baseline.operations[0:] + qs_aquastat_stub.operations[0:]

    data = qs_aquastat.publish().fetch()

    #######################################################################################################################
    # Conflict history model and baseline

    qs_conflict = (Queryset("fatalities002_conflict_history", "country_month")
                   .with_theme("fatalities002")
                   .describe("""Predicting ln(fatalities), cm level
    
            Queryset with baseline and first set of conflict history features
    
            """)
                   )
    qs_conflict.operations = qs_baseline.operations[0:] + qs_conflict_stub.operations[0:]

    data = qs_conflict.publish().fetch()


    #######################################################################################################################
    # Conflict history model, extension, and baseline

    qs_conflict_long = (Queryset("fatalities002_conflict_history_long", "country_month")
                        .with_theme("fatalities002")
                        .describe("""Predicting ln(fatalities), cm level
    
            Queryset with baseline, first set and extended set of conflict history features
    
            """)
                        )
    qs_conflict_long.operations = qs_conflict.operations[0:] + qs_conflict_ext.operations[0:]

    data = qs_conflict_long.publish().fetch()

    #######################################################################################################################
    # Collecting combined queryset objects in a list


    qslist = [qs_baseline, qs_topics, qs_aquastat, qs_conflict, qs_conflict_long]

    return

