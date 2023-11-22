model = {
            'modelname': 'fatalities003_nl_joint_narrow_hurdle_lgb',
            'algorithm': HurdleRegression(clf_name='LGBMClassifier', reg_name='LGBMRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'joint_narrow',
            'queryset': 'fatalities003_joint_narrow',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }