model = {
            'modelname':  'fatalities003_joint_narrow_xgb',
            'algorithm':  XGBRFRegressor(n_estimators=250, n_jobs=nj),
            'depvar':     "ged_sb_dep",
            'data_train':    'joint_narrow',
            'queryset':   'fatalities003_joint_narrow',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }