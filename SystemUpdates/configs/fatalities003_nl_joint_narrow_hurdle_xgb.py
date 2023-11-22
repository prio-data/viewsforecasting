model = {
            'modelname': 'fatalities003_nl_joint_narrow_hurdle_xgb',
            'algorithm': HurdleRegression(clf_name='XGBClassifier', reg_name='XGBRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'joint_narrow',
            'queryset': 'fatalities003_joint_narrow',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }