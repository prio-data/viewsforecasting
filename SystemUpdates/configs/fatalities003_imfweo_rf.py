model = {
            'modelname':        'fatalities003_imfweo_rf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           "ln_ged_sb_dep",
            'data_train':       'imfweo',
            'queryset':         'fatalities003_imfweo',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      '',
            'long_description': ''
        }