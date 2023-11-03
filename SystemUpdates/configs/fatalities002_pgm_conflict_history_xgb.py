model = {
            'modelname': 'fatalities002_pgm_conflict_history_xgb',
            'algorithm': xgb_regressor,
            'depvar': "ln_ged_sb_dep",
            'queryset': 'fatalities002_pgm_conflict_history',
            'data_train': 'conflicthist',
            'level':            'pgm',
            'preprocessing': 'float_it',
            'description':      '',
            'long_description':      ''

        }