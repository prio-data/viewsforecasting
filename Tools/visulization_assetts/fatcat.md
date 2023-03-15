# Introduction

This document outlines two tools VIEWS-users can engage with to employ and visualize the data: FatCat and FatCat Lists. FatCat is a VIEWS tool which categorized VIEWS data into fatalities categories. FatCat Lists, is a visualization tool which allows users to quickly generate lists of countries that are predicted to transition between states of violence. 

This document begins by introducing FatCat, explaining its purpose, defining the operationalization of its variables, and outlines its functions. Following the overview of FatCat, the document introduces FatCat Lists, and explains its functionality for users.  

<br />

# FatCat
## <u>Purpose</u>

FatCat is a tool that categorizes country-month (cm) violence into classes and presents these data in a comparison list. The function creates a pandas DataFrame that fetches conflict actuals for the 40 months prior to EndOfHistory (as report by the UCDP GED and UCDP candidate datasets) and VIEWS predictions from EndOfHistory+1 to EndOfHistory+36. 

This combined DataFrame indexes these data by country_id-step. Country_id refers to the country's assigned Gledtisch-Ward country code, whereas steps refer to the number of months away the observation is from the EndOfHistory. EndOfHistory is defined as the last month of available UCDP candidate data (*actuals*). 

Here, Step0 refers to the user defined EndOfHistory. The negative steps represent months since EndOfHistory (*actuals*) and positive steps correspond to steps forward since EndOfHistory (*predictions*). 

<br/>

##### Fatalities Categories

These data are then categorized by the number of fatalities at each country-step as follows:<br/>
**<u>Non-violent</u>**: The country-step has zero estimated conflict-related fatalities. 
**<u>Low Violence</u>**: The country-step has 1-9 estimated conflict-related fatalities. 
**<u>Violent</u>**: The country-step has 10-99 estimated conflict-related fatalities.
**<u>High Violence</u>**: The country-step has 100-999 estimated conflict-related fatalities.
**<u>Extreme Violence</u>**: The country-step has 1000+ estimated conflict-related fatalities.

<br/>

##### Monthly Changes

Next, the 'monthly_change' variable calculates the change between levels of violence from one month to the next. For example, whether a country escalates or de-escalates from step(x) to step(y). These changes are categorized as: 

**<u>Extreme De-scalation</u>**: When a country changes  from extreme violence to non-violent in one month
**<u>Rapid De-escalation</u>**: When a country moves from high violence to non-violent in one month
**<u>De-Escalation</u>**: When a country moves from high violent to non-violent in one month
**<u>Low De-esclation</u>**: When a country moves from low violence to non-violent in one month
**<u>Staus Quo</u>**: When a country does not observe a change in violence level form month to month
**<u>Low Escalation</u>**: When a country moves from non-violent low violence to in one month. 
**<u>Escalation</u>**: When a country moves from non-violent to violent in one month
**<u>Rapid Escalation</u>**: When a country moves from non-violent to high violent in one month
**<u>Extreme Escalation</u>**: When a country moves from non-violent to high violence in one month

<br/>

##### Rolling Violence and Intensity Levels

After the creation of 'monthly change', the variables 'rolling_mean_violence' and 'intensity_lvl' are created. The variable 'rolling_mean_violence' takes the mean number of fatalities over the user defined months prior (currently set to three months prior). This variable provides context on the baseline level of recent violence. The 'intensity_lvl' variable is created by categorizing the 'rolling_mean_violence' into three categories: 
<br/>
**<u>0</u>**: The mean fatalities in the 3-months prior is 0 
**<u>1</u>**: The mean fatalities in the 3-months prior is less than 100
**<u>2</u>**: The mean fatalities in the 3-months prior is greater than 100

<br/>
<br/>

##### Uncertainty of Predictions

All positive steps (*predictions*) have four additional variables. These variables capture the probability that a given country-step prediction will fall into the corresponding categories:

<br/>
<u>multi_0_logit</u>: The probability that fatalities in the step have 0 fatalitites  <br />
<u>multi_1_logit</u>:  The probability that fatalities in the step have 1-9 fatalitites  <br />
<u>multi_2_logit</u>: The probability that fatalities in the step have 9-99 fatalitites  <br />
<u>multi_3_logit</u>: The probability that fatalities in the step have 100-999 fatalitites  <br />
<u>multi_4_logit</u>: The probability that fatalities in the step have 1000+ fatalitites  <br />



<br/>
<br/>
<br/>
<br/>


## FatCat Lists

Whereas FatCat provides a Pandas DataFrame with relevant information on changes in violence levels for given countries, FatCat Lists provides a list of countries predicted to change from one fatcat status to another over a user-specified period. 
<br/>
For example, the photo below presents the list of countries that are expected to de-escalate in violence from EndOfHistory to EndOfHistory+12 months. This table presents the status of the country at present (EndOfHistory) and the predicted level of violence in the future (here one-year later). FatCat Lists also provides the number of fatalities at each point and the mean level of violence in the 3-months preceding the given month. 

![[Screen Shot 2023-02-09 at 16.31.39.png]]

FatCat Lists allows for users to produce lists of countries that move between any of the possible FatCats over any specified time period. 

<br/>
<br/>

## What FatCat Lists does not do

1. FatCat provides the ability to compare change across two steps. (e.g., Step0 vs Step12). FatCat does not allow for the comparison of multiple steps, yet. <br/>

2. This version of FatCat allows for the comparison of a future step against Step0; it does not allow for the comparison of future steps against another. For example, Step0 vs Step12 works. Step6 vs Step12 does not work, yet. <br/>
4. 

<br/>
<br/>


## Future Ambitions

A future version of FatCat uses these data to create variables which capture the probability that a given country will shift between any of the FatCats. To conduct this, these data will be modeled in a multinomial logit. This equation will produce the likelihood that a given step will shift between states of conflict, only taking into account its past conflicts. 
<br/>
With these results, FatCat can assign risk categories to country-steps based on the probability that the country will escalate in violence. These data can be used as future input data for models that seek to study how specific interventions alter the probability of violence de-/escalation. 

<br/>
<br/>


## FatCat Variable Descriptions

This section provides information on the variables defined in FatCat. 

<u>fatalities_step_0</u>: The number of fatalities at step 0 (integer) <br />
<u>fatcat_step_0</u>: The fatalities category at step0 (categorical) <br />
<u>fatcat_change_step_0</u>: The change in category from step -1 to step0 (integer) <br />
<u>rolling_mean_violence_step_0</u>: Mean number of fatalities in the 3-months prior to step 0.  (integer) <br />
<u>intensity_lvl_step_0</u>: Categorical variable defining the level of intensity in the three months prior to step0. (0 = no fatalities, 1 = 1-99 fatalities, 2 = more than 100 fatalities ) <br />

<u>fatalities_step_12</u>: The number of fatalities at step 12 (integer) <br />
<u>fatcat_step_12</u>: The fatalities category at step 12 (categorical) <br />
<u>fatcat_change_step_12</u>: The change in category from step 11 to step 12 (integer) <br />
<u>intensity_lvl_step_12</u>: Categorical variable defining the level of intensity in the three months prior to step 12. (0 = no fatalities, 1 = 1-99 fatalities, 2 = more than 100 fatalities ) <br />

<u>multi_0_logit</u>: The probability that fatalities from step 12 have 0 fatalitites  <br />
<u>multi_1_logit</u>: The probability that fatalities from step 12 have 1-9 fatalitites  <br />
<u>multi_2_logit</u>: The probability that fatalities from step 12 have 9-99 fatalitites  <br />
<u>multi_3_logit</u>: The probability that fatalities from step 12 have 100-999 fatalitites  <br />
<u>multi_4_logit</u>: The probability that fatalities from step 12 have 1000+ fatalitites  <br />

<u>rolling_mean_violence_step_12</u>:  Mean number of fatalities in the 3-months prior to step 12.  (integer) <br />
<u>fatcat_change</u>: The change in fatcat when moving from step 0 to step 12. (integer ranging from -4 to 4) <br />
<u>facat_change_nominal</u>: The nominal category for fatcat_change. (-4: extreme de-esclation; -3: high de-esclation; -2 de-esclation; -1: low de-escalation;  0: status quo; 1: low escalation; 2: esclation; 3: high escalation; 4: extreme escalation) <br />

<u>country</u>: Country name <br />
<u>fatcat_0_nominal</u>: Category of violence at step 0 ('Non-violent', 'Low Violence', 'Violent', 'High-violence', 'Extreme Violence') <br />
<u>fatcat_12_nominal</u>  (Category of violence at step 0 ('Non-violent', 'Low Violence', 'Violent', 'High-violence', 'Extreme Violence') <br />