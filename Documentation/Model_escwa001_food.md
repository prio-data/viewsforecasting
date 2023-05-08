| Model         | Included variable name    | Database variable name          | Transformations                                         |
|:--------------|:--------------------------|:--------------------------------|:--------------------------------------------------------|
| escwa001_food | 'ged_sb_dep'              | 'ged2_cm.ged_sb_best_sum_nokgi' | ["'missing.fill'", "'bool.gte'"]                        |
| escwa001_food | 'wfpmp_mp_price'          | 'wfpmp_cm.wfpmp_mp_price'       | ["'missing.replace_na'"]                                |
| escwa001_food | 'wfpmp_wheat_price'       | 'wfpmp_cm.wfpmp_wheat_price'    | ["'missing.replace_na'"]                                |
| escwa001_food | 'wfpmp_sugar_price'       | 'wfpmp_cm.wfpmp_sugar_price'    | ["'missing.replace_na'"]                                |
| escwa001_food | 'wfpmp_milk_price'        | 'wfpmp_cm.wfpmp_milk_price'     | ["'missing.replace_na'"]                                |
| escwa001_food | 'wfpmp_meat_price'        | 'wfpmp_cm.wfpmp_meat_price'     | ["'missing.replace_na'"]                                |
| escwa001_food | 'wfpmp_mp_price_t12'      | 'wfpmp_cm.wfpmp_mp_price'       | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'wfpmp_wheat_price_t12'   | 'wfpmp_cm.wfpmp_wheat_price'    | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'wfpmp_sugar_price_t12'   | 'wfpmp_cm.wfpmp_sugar_price'    | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'wfpmp_milk_price_t12'    | 'wfpmp_cm.wfpmp_milk_price'     | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'wfpmp_meat_price_t12'    | 'wfpmp_cm.wfpmp_meat_price'     | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'delta_wfpmp_mp_price'    | 'wfpmp_cm.wfpmp_mp_price'       | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'delta_wfpmp_wheat_price' | 'wfpmp_cm.wfpmp_wheat_price'    | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'delta_wfpmp_sugar_price' | 'wfpmp_cm.wfpmp_sugar_price'    | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'delta_wfpmp_milk_price'  | 'wfpmp_cm.wfpmp_milk_price'     | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'delta_wfpmp_meat_price'  | 'wfpmp_cm.wfpmp_meat_price'     | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'fao_mp_price'            | 'faostat_pp_cm.mp_price'        | ["'missing.replace_na'"]                                |
| escwa001_food | 'fao_wheat_price'         | 'faostat_pp_cm.wheat_price'     | ["'missing.replace_na'"]                                |
| escwa001_food | 'fao_sugar_price'         | 'faostat_pp_cm.sugar_price'     | ["'missing.replace_na'"]                                |
| escwa001_food | 'fao_milk_price'          | 'faostat_pp_cm.milk_price'      | ["'missing.replace_na'"]                                |
| escwa001_food | 'fao_meat_price'          | 'faostat_pp_cm.meat_price'      | ["'missing.replace_na'"]                                |
| escwa001_food | 'fao_mp_price_t12'        | 'faostat_pp_cm.mp_price'        | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'fao_wheat_price_t12'     | 'faostat_pp_cm.wheat_price'     | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'fao_sugar_price_t12'     | 'faostat_pp_cm.sugar_price'     | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'fao_milk_price_t12'      | 'faostat_pp_cm.milk_price'      | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'fao_meat_price_t12'      | 'faostat_pp_cm.meat_price'      | ["'missing.fill'", "'temporal.tlag'", "'missing.fill'"] |
| escwa001_food | 'delta_fao_mp_price'      | 'faostat_pp_cm.mp_price'        | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'delta_fao_wheat_price'   | 'faostat_pp_cm.wheat_price'     | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'delta_fao_sugar_price'   | 'faostat_pp_cm.sugar_price'     | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'delta_fao_milk_price'    | 'faostat_pp_cm.milk_price'      | ["'missing.replace_na'", "'temporal.delta'"]            |
| escwa001_food | 'delta_fao_meat_price'    | 'faostat_pp_cm.meat_price'      | ["'missing.replace_na'", "'temporal.delta'"]            |