#!/usr/bin/env python
# coding: utf-8

# The following notebooks is currently storage for all the standard querysets needed for the monthly runs.
# This has been added so they may be stored with all the other standard querysets and adjusted/changed en-masse later without having to touch the visualization code. 
# 
# To be added when updates to queryset come up: combined variable gdp that requires the use of two variables to create a third one. 
# Currently has to be done in notebook and outside querysetting. 

# In[1]:


from viewser.operations import fetch
from viewser import Queryset, Column


# In[2]:

def publish_querysets():
    #features mapping required queryset at cm level
    features_qs = (Queryset("Monthly_update_features_cm", "country_month")
        .with_column(Column("ged_sb_ln1", from_loa = "country_month", from_column = "ged_sb_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            )
          .with_column(Column("ged_ns_ln1", from_loa = "country_month", from_column = "ged_ns_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            )
          .with_column(Column("ged_os_ln1", from_loa = "country_month", from_column = "ged_os_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            )
        .with_column(Column("ged_sb_ln2", from_loa = "country_month", from_column = "ged_sb_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            .transform.ops.ln()
            )
        .with_column(Column("ged_ns_ln2", from_loa = "country_month", from_column = "ged_ns_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            .transform.ops.ln()
            )
        .with_column(Column("ged_os_ln2", from_loa = "country_month", from_column = "ged_os_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            .transform.ops.ln()
            )

        .with_column(Column("vdem_v2x_libdem", from_loa = "country_year", from_column = "vdem_v12_v2x_libdem")
            .transform.missing.replace_na()
            .transform.temporal.tlag(12)
            .transform.missing.fill()
            )
        .with_column(Column("wdi_sp_dyn_imrt_in", from_loa = "country_year", from_column = "wdi_sp_dyn_imrt_in")
                             .transform.missing.fill()
                             .transform.temporal.tlag(12)
                             .transform.missing.fill()
            )
        .with_column(Column("wdi_ny_gdp_mktp_kd", from_loa = "country_year", from_column = "wdi_ny_gdp_mktp_kd")
                     .transform.missing.fill()
                     .transform.temporal.tlag(12)
                     .transform.missing.fill()
                    )
        .with_column(Column("wdi_sp_pop_totl", from_loa = "country_year", from_column = "wdi_sp_pop_totl")
                     .transform.missing.fill()
                     .transform.temporal.tlag(12)
                     .transform.missing.fill()
                    )
        .with_theme("monthly_update")

                .describe("""Features for the monthly report""")
                  )

    features_qs.publish().fetch()
    print('published Monthly_update_features_cm queryset')




    #features mapping queryset at pgm level
    features_pgm_qs = (Queryset("Monthly_update_features_pgm", "priogrid_month")
        .with_column(Column("ged_sb_ln1", from_loa = "priogrid_month", from_column = "ged_sb_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            )
          .with_column(Column("ged_ns_ln1", from_loa = "priogrid_month", from_column = "ged_ns_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            )
          .with_column(Column("ged_os_ln1", from_loa = "priogrid_month", from_column = "ged_os_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            )
        .with_column(Column("ged_sb_ln2", from_loa = "priogrid_month", from_column = "ged_sb_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            .transform.ops.ln()
            )
          .with_column(Column("ged_ns_ln2", from_loa = "priogrid_month", from_column = "ged_ns_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            .transform.ops.ln()
            )
          .with_column(Column("ged_os_ln2", from_loa = "priogrid_month", from_column = "ged_os_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.ops.ln()
            .transform.ops.ln()
            )

        .with_theme("monthly_update")

                .describe("""Features for the monthly report""")
                  )

    features_pgm_qs.publish().fetch()
    print('published Monthly_update_features_pgm queryset')


   
    #required queryset for association priogrid and countries
    pg_country_queryset = (Queryset("m_associate_country_2_priogrid", "priogrid_month")
                #CONFLICT TYPES NOT LOGGED and NOT time lagged 
                #.with_column(Column("month_id", from_table = "priogrid_month", from_column = "month_id"))
                .with_column(Column('name', from_loa = 'country', from_column = 'name'))

                .with_theme("Mapping")

                .describe("""Mapping, allows for association of priogrid with country 

                """)

               )
    pg_country_queryset.publish().fetch()
    print('published m_associate_country_2_priogrid queryset')


    

    #now getting the monthly running average for mapping at cm level
    running_average_qs = (Queryset("Monthly_update_running_average_cm", "country_month")
        .with_column(Column("ged_sb_run_average_6_ln1", from_loa = "country_month", from_column = "ged_sb_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.temporal.moving_average(6)
            .transform.ops.ln()
            )
          .with_column(Column("ged_ns_run_average_6_ln1", from_loa = "country_month", from_column = "ged_ns_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.temporal.moving_average(6)
            .transform.ops.ln()
            )
          .with_column(Column("ged_os_run_average_6_ln1", from_loa = "country_month", from_column = "ged_os_best_sum_nokgi")
            .transform.missing.replace_na()
            .transform.temporal.moving_average(6)
            .transform.ops.ln()
            )

        .with_theme("monthly_update")

                .describe("""Features for the monthly report""")
        )


    running_average_qs.publish().fetch()
    print('published Monthly_update_running_average_cm queryset')
    
    #now getting the montly running average for mapping at pgm level

    running_average_qs_pgm = (Queryset("Monthly_update_running_average_pgm", "priogrid_month")


    # target variable
    .with_column(Column("ged_sb_run_average_6_ln1", from_loa = "priogrid_month", from_column = "ged_sb_best_sum_nokgi")
        .transform.missing.replace_na()
        .transform.temporal.moving_average(6)
        .transform.ops.ln()
        )
      .with_column(Column("ged_ns_run_average_6_ln1", from_loa = "priogrid_month", from_column = "ged_ns_best_sum_nokgi")
        .transform.missing.replace_na()
        .transform.temporal.moving_average(6)
        .transform.ops.ln()
        )
      .with_column(Column("ged_os_run_average_6_ln1", from_loa = "priogrid_month", from_column = "ged_os_best_sum_nokgi")
        .transform.missing.replace_na()
        .transform.temporal.moving_average(6)
        .transform.ops.ln()
        )
                
    .with_theme("monthly_update")
                         
            .describe("""Features for the monthly report""")
    )
              

    running_average_pgm_master=running_average_qs_pgm.publish().fetch()
    print('published Monthly_update_running_average_pgm queryset')
    
    #country name and region association queryset
    country_names_and_regions_qs = (Queryset('Monthly_update_country_names_and_regions', 'country_month')
            .with_column(Column('name', from_loa = 'country', from_column = 'name'))
            .with_column(Column('in_africa', from_loa = 'country', from_column = 'in_africa'))
            .with_column(Column('in_me', from_loa = 'country', from_column = 'in_me'))
            .with_theme("monthly_update")

                .describe("""Features for the monthly report""")
        )
    country_names_and_regions_qs.publish().fetch()
    print('published Monthly_update_country_names_and_regions queryset')






