| Model             | Included variable name        | Database variable name                | Transformations                                         |
|:------------------|:------------------------------|:--------------------------------------|:--------------------------------------------------------|
| escwa001_aquastat | 'ged_sb_dep'                  | 'ged2_cm.ged_sb_best_sum_nokgi'       | ["'missing.fill'", "'bool.gte'"]                        |
| escwa001_aquastat | 'agr_withdrawal_pct_t48'      | 'fao_aqua_cy.agr_withdrawal_pct'      | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'dam_cap_pcap_t48'            | 'fao_aqua_cy.dam_cap_pcap'            | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'groundwater_export_t48'      | 'fao_aqua_cy.groundwater_export'      | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'fresh_withdrawal_pct_t48'    | 'fao_aqua_cy.fresh_withdrawal_pct'    | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'ind_efficiency_48'           | 'fao_aqua_cy.ind_efficiency'          | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'irr_agr_efficiency_48'       | 'fao_aqua_cy.irr_agr_efficiency'      | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'services_efficiency_48'      | 'fao_aqua_cy.services_efficiency'     | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'general_efficiency_t48'      | 'fao_aqua_cy.general_efficiency'      | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'water_stress_t48'            | 'fao_aqua_cy.water_stress'            | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'renewable_internal_pcap_t48' | 'fao_aqua_cy.renewable_internal_pcap' | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_aquastat | 'renewable_pcap_t48'          | 'fao_aqua_cy.renewable_pcap'          | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |