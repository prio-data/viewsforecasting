model = {
            'modelname':     'fatalities003_nl_faostat_rf',
            'algorithm':     XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':        "ged_sb_dep",
            'data_train':    'faostat',
            'queryset':      'fatalities003_faostat',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }