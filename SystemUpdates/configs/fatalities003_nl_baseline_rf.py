model = {
            'modelname':        'fatalities003_nl_baseline_rf',
            'algorithm':        XGBRFRegressor(n_estimators=300, n_jobs=nj),
            'depvar':           'ged_sb_dep',
            'data_train':       'baseline003',
            'queryset':         'fatalities003_baseline',
            'preprocessing':    'float_it',
            'level':            'cm',
            'description':      'Baseline model with a few conflict history features as well as log population, random forests regression model.',
            'long_description':  'A very simple model with only five data columns (each column representing one feature): The number of fatalities in the same country at $t-1$, three decay functions of time since there was at least five fatalities in a single month, for each of the UCDP conflict types -- state-based, one-sided, or non-state conflict -- and log population size (Hegre2020RP,Pettersson2021JPR).The features in the baseline are included in all the models described below. This ensures that all models in the ensemble provides at least moderately good predictions, while guaranteeing diversity in feature sets and modelling approaches.'
        }