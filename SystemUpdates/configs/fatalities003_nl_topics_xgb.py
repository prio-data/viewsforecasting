model = {
            'modelname':  'fatalities003_nl_topics_xgb',
            'algorithm': XGBRegressor(n_estimators=80, learning_rate=0.05, n_jobs=nj),
            'depvar': "ged_sb_dep",
            'data_train':    'topics_003',
            'queryset':   "fatalities003_topics",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }