model = {
            'modelname': 'fatalities003_nl_joint_broad_hurdle_rf',
            'algorithm': HurdleRegression(clf_name='RFClassifier', reg_name='RFRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'joint_broad',
            'queryset': 'fatalities003_joint_broad',
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }