# model1_config.py

modelname = 'fatalities003_nl_baseline_rf'
n_estimators = 100
n_jobs = 12
depvar = 'ged_sb_dep'
data_train = 'baseline003'
queryset = 'fatalities003_baseline'
preprocessing = 'float_it'
level = 'cm'
description = 'Baseline model with a few conflict history features as well as log population, random forests regression model.'
long_description = 'A very simple model with only five data columns (each column representing one feature): The number of fatalities in the same country at $t-1$, three decay functions of time since there was at least five fatalities in a single month, for each of the UCDP conflict types -- state-based, one-sided, or non-state conflict -- and log population size (Hegre2020RP, Pettersson2021JPR).'
