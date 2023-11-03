model = {
            'modelname':  'fatalities003_nl_vdem_hurdle_xgb',
            'algorithm': HurdleRegression(clf_name='XGBClassifier', reg_name='XGBRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'vdem_short',
            'queryset':  "fatalities003_vdem_short",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }