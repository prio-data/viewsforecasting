model = {
            'modelname': 'fatalities003_nl_conflicthistory_long_xgb',
            'algorithm': XGBRegressor(n_estimators=100, learning_rate=0.05, n_jobs=nj),
            'depvar': "ged_sb_dep",
            'data_train':    'conflictlong_ln',
            'queryset': "fatalities003_conflict_history_long",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }