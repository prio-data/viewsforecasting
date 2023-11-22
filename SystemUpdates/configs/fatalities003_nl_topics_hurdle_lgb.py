model = {
            'modelname':  'fatalities003_nl_topics_hurdle_lgb',
            'algorithm': HurdleRegression(clf_name='LGBMClassifier', reg_name='LGBMRegressor'),
            'depvar': "ged_sb_dep",
            'data_train':    'topics_003',
            'queryset':   "fatalities003_topics",
            'preprocessing': 'float_it',
            'level':            'cm',
            'description':      '',
            'long_description':      ''
        }
