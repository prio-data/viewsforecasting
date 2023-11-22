model = {
            'modelname':        'fatalities003_faoprices_rf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           'ln_ged_sb_dep',
            'data_train':       'faoprices',
            'queryset':         'fatalities003_faoprices',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      '',
            'long_description': ''
        }