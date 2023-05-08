| Model            | Included variable name            | Database variable name                           | Transformations                                         |
|:-----------------|:----------------------------------|:-------------------------------------------------|:--------------------------------------------------------|
| escwa001_faostat | 'ged_sb_dep'                      | 'ged2_cm.ged_sb_best_sum_nokgi'                  | ["'missing.fill'", "'bool.gte'"]                        |
| escwa001_faostat | 'consumer_prices_food_indices'    | 'faostat_cpi_cm.consumer_prices_food_indices'    | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'consumer_prices_general_indices' | 'faostat_cpi_cm.consumer_prices_general_indices' | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'food_price_inflation'            | 'faostat_cpi_cm.food_price_inflation'            | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'avg_adequate_diet'               | 'faostat_fsec_cy.avg_adequate_diet'              | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'avg_animalprotein_pcap_day'      | 'faostat_fsec_cy.avg_animalprotein_pcap_day'     | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'avg_fprod_value'                 | 'faostat_fsec_cy.avg_fprod_value'                | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'avg_protein_pcap_day'            | 'faostat_fsec_cy.avg_protein_pcap_day'           | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'gdp_pc_ppp'                      | 'faostat_fsec_cy.gdp_pc_ppp'                     | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'kcal_pcap_day'                   | 'faostat_fsec_cy.kcal_pcap_day'                  | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'kcal_pcap_day_cerotu'            | 'faostat_fsec_cy.kcal_pcap_day_cerotu'           | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pcap_fprod_var'                  | 'faostat_fsec_cy.pcap_fprod_var'                 | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pcap_fsupply_var'                | 'faostat_fsec_cy.pcap_fsupply_var'               | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_arable_land'                 | 'faostat_fsec_cy.pct_arable_land'                | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_cereal_import'               | 'faostat_fsec_cy.pct_cereal_import'              | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_fimport_merch'               | 'faostat_fsec_cy.pct_fimport_merch'              | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_modsevere_finsecurity'       | 'faostat_fsec_cy.pct_modsevere_finsecurity'      | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_pop_basicdrink'              | 'faostat_fsec_cy.pct_pop_basicdrink'             | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_pop_basicsani'               | 'faostat_fsec_cy.pct_pop_basicsani'              | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_pop_safedrink'               | 'faostat_fsec_cy.pct_pop_safedrink'              | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_pop_safesani'                | 'faostat_fsec_cy.pct_pop_safesani'               | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_severe_finsecurity'          | 'faostat_fsec_cy.pct_severe_finsecurity'         | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_und5_overweight'             | 'faostat_fsec_cy.pct_und5_overweight'            | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_und5_stunted'                | 'faostat_fsec_cy.pct_und5_stunted'               | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_und5_wasting'                | 'faostat_fsec_cy.pct_und5_wasting'               | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pct_undernourished'              | 'faostat_fsec_cy.pct_undernourished'             | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pol_stability'                   | 'faostat_fsec_cy.pol_stability'                  | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pop_modsevere_finsecurity'       | 'faostat_fsec_cy.pop_modsevere_finsecurity'      | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pop_severe_finsecurity'          | 'faostat_fsec_cy.pop_severe_finsecurity'         | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'pop_undernourished'              | 'faostat_fsec_cy.pop_undernourished'             | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'prev_adult_obesity'              | 'faostat_fsec_cy.prev_adult_obesity'             | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'prev_infant_bfeed'               | 'faostat_fsec_cy.prev_infant_bfeed'              | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'prev_lowbweight'                 | 'faostat_fsec_cy.prev_lowbweight'                | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'prev_repr_anemia'                | 'faostat_fsec_cy.prev_repr_anemia'               | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_faostat | 'rail_density'                    | 'faostat_fsec_cy.rail_density'                   | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |