model = {
            'modelname':        'fatalities003_nl_conflicthistory_rf',
            'algorithm':        XGBRFRegressor(n_estimators=250, n_jobs=nj),
            'depvar':           "ged_sb_dep",
            'data_train':       'conflict_ln',
            'queryset':         "fatalities003_conflict_history",
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'A collection of variables that together map the conflict history of a country, random forests regression model.' ,
            'long_description': 'A collection of variables that together map the conflict history of a country. The features include lagged dependent variables for each conflict type as coded by the UCDP (state-based, one-sided, or non-state) for up to each of the preceding six months, decay functions of time since conflict caused 5, 100, and 500 deaths in a month, for each type of violence, whether ACLED (https://doi.org/10.1177/0022343310378914 recorded similar violence, and whether there was recent violence in any neighboring countries.'
        }