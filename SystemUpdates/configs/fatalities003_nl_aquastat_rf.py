model = {
            'modelname':     'fatalities003_nl_aquastat_rf',
            'algorithm':     XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':        "ged_sb_dep",
            'data_train':    'aquastat',
            'queryset':      'fatalities003_aquastat',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }