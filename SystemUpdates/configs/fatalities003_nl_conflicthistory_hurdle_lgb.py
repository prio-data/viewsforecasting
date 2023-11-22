model = {
            'modelname': 'fatalities003_nl_conflicthistory_hurdle_lgb',
            'algorithm': HurdleRegression(clf_name='LGBMClassifier', reg_name='LGBMRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'conflict_ln',
            'queryset': "fatalities003_conflict_history",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }