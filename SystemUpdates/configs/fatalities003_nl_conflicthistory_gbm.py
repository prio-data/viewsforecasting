model = {
            'modelname':        'fatalities003_nl_conflicthistory_gbm',
            'algorithm':        GradientBoostingRegressor(n_estimators=200),
            'depvar':           'ged_sb_dep',
            'data_train':       'conflict_ln',
            'queryset':         "fatalities003_conflict_history",
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'A collection of variables that together map the conflict history of a country, scikit gradient boosting regression model.',
            'long_description': ''
        }