# CHANGELOG

This file documents changes to the ViEWS models over time.

The title of each entry specifies the model and model version that the changes relate to, as well as the production run and try sequence for which the changes were first implemented. The general format is as follows:

`[model][version]_[production run]_[try sequence]`, where

- **Model** is a a short label for the prediction model at hand, e.g. the `fatalities` model that is currently in production. To learn more about current and deprecated ViEWS models, please visit https://viewsforecasting.org/methodology.

- **Model version** is a numeric identifier that specifies the concerned version of the aforementioned model, e.g. `001`. Changes to the model(s) in production (such as new ensembling techniques or updates to model compositions) are implemented in batches and documented in this changelog. Each batch of changes prompts a new model version, upon which the corresponding numeric identifier is incremented by 1.

- **Production run** specifies the first production run that made use of the new model version. From 2022 onwards, all production runs in ViEWS are named by means of the year (YYYY) and month (MM) of the last data that informs a given run, e.g. `2022_06`, rather than by the time of the data release itself. To learn more about the naming convention for our public production runs, please see the API documentation at https://github.com/prio-data/viewsforecasting/tree/main/Documentation/API.

- **Try sequence** indicates whether the aforementioned production run required any bug fixes prior to successful completion. If the production run was completed on the first attempt, the try counter is given the default value of `t01`. For each additional attempt, the counter is incremented by 1. Errors and resolutions are documented in this changelog.


## Unreleased

This section lists unreleased model updates that we are currently working on. Pending completion, only the concerned models and model versions are listed.

### fatalities002

#### Added

Features from the ViEWS-ESCWA model, which was developed under the ViEWS2 data infrastructure (TBC).

This model version is specified in the `viewsforecasting` GitHub repository at https://github.com/prio-data/viewsforecasting.

#### Changed

#### Deprecated

#### Removed

#### Fixed


## Released

### fatalities001_2022_01_t01

#### Added

Launch of the new `fatalities` model, which generates predictions for the number of fatalities in impending conflict per country-month and PRIO-GRID-month, as well as dichotomous forecasts for the probability of at least 25 battle-related deaths (BRDs) per country-month and at least 1 BRD per PRIO-GRID-month.

This model and version is specified in the `FCDO_predicting_fatalities` GitHub repository at https://github.com/prio-data/FCDO_predicting_fatalities.

To learn more, please see:

> Hegre et al (2022). "Forecasting fatalities". Technical report, Uppsala University. Available at: http://urn.kb.se/resolve?urn=urn:nbn:se:uu:diva-476476.
