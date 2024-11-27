from Tools.visualization_assetts.config1 import*
from Tools.visualization_assetts.geo_coverage_determination import *

#general settings

#size of the map
width_global = 20
height_global = 20

#because of the specificities of how pgm maps work require to use plt.savefig rather than built in .save function within mapper
#choose the dpi size of the pgm maps

pgm_dpi_global = 600

#country map levels are the ones per earlier discussion that should have a background because of how they work and greater usefullness of actual map data
#below is the setting for both the background choice
#the transparency level
#the size of custom views experimental labels
#choice is also available for the background choice for pgm maps
#choices below are what I thought looked good for the two levels
country_background_global = 'OpenStreetMap'
country_mapping_transparency_global = 0.8
views_experimental_font_global = 18
pgm_background_country_level = 'StamenTerrainBackground'

#the following allows for changes to the textbox size
#change here to preferred textbox sizes if you do not like the appearance, especially if the width and height changes were made earlier
#note that ame and africa are close enough in size that their textbox size should be the same

def function_for_textbox(location):
    if str(location) in('globe'):
        textbox_font_size = 10
    elif str(location) in ('ame', 'africa'):
        textbox_font_size = 20
    else:textbox_font_size = 15
    return textbox_font_size

#note anything fatality related should have colormap rainbow, change here if you do not wish this option
#dictionary has been also chosen per previous discussions from standard dictionaries available
#change map color is also set at bwr
#however this is a step to change these defaults if you wish to
fatality_colormap = 'rainbow'
fatality_dictionary_cm =  dictionary_stand_2p_10k
fatality_dictionary_pgm = dictionary_stand_2p
change_colormap_global = 'bwr'


#dictionary for dichototomous prediciton outcome
#now with the new method
raw_dich_values=np.array([0.001,0.002,0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, .99])
dich_values = []
for i in raw_dich_values:
    temp1 = logit(i)
    dich_values.append(temp1)
dich_ticklabels=['<= 0.1%', '0.2%', '0.5%', '1%', '2%', '5%', '10%', '20%', '40%', '60%', '80%', '90%', '95%', '99%']
dichotomous_dictionary_cm = dict(zip(dich_ticklabels, dich_values))

dictionary_dichotomous_pgm = dichotomous_dictionary_cm

#for fetching predicitons, currently there is only one thing that is fetched, which is called step_combined
#this can potentially change in the future
#below choose what column name is given and what you want to call them, this should future proof this code as it will allow for renaming of variables
#please note that if you know that something is log transformed, make sure to change the name accordingly
#small note. dichotomous variable does not need to be double logged but continuous does. this allows the use of the default double log appearance which looks better in maps.

prediction_cont_name_default = {'step_combined':'ln1_step_combined_sb'}
prediction_dich_name_default = {'step_combined':'step_combined_sb'}

do_we_need_to_double_log_cont_variable = 'yes'


#below create double_logged names that you want to use, this feeds into a loop that checks for above 'yes' statement, transforms variable and then renames column
#the loop itself rests in the code portion of the code
#please include the single logged variable as the basis for the double logged one
prediction_cont_name_double_logged = []
variable1 = {'old_name': 'ln1_step_combined_sb', 'new_name':'ln2_step_combined_sb'}
#add additional variables as a continued list, eg. 
#variable2 = {'old_name': 'ln1_step_combined_ns', 'new_name':'ln2_step_combined_ns'}
prediction_cont_name_double_logged.append(variable1)
#here is an example of how to continue the list
#prediction_cont_name_double_logged.append(variable2)


#for predictions portion of the code 
#which variables do you want mapped for predictions
variables_wanted_predictions = {'ln2_step_combined_sb'}

variables_wanted_predictions_dich = {'step_combined_sb'}

#steps wanted for prediction (note that these are the steps to graph)
#additionally for the titles, this is the opportunity to give the output a human name
steps_wanted_prediction_fat = {3, 6, 12, 36}
prediction_title_name = 'Predicted fatalities'
prediction_dich_title_name = 'Predicted probability of conflict'

#choices for line, bar, pie charts
#note that dichotomous only has line choices, as that is the only additional graph type requested for this outcome

#choices for the line/bar/pie charts, including dpi and which variable is wanted
#please use a single ln1 variable version for here. explained in the bar and pie section.

line_bar_pie_charts_dpi = 600

#please use note that the below selection takes more than one variable if they exist, so ns and os, however, we can choose one dictionary at a time, as such please choose one type of transformed fatality variable, e.g., ln1 or actual and match the dictionaries and variable transformation accordingly
variables_wanted_predictions_line_bar_pie = {'ln1_step_combined_sb'}
#this is used inside the functions to create top X lists, note that you can use more than one variable
line_bar_pie_variable_transformation = 'ln1'
variables_wanted_predictions_dich_line = {'step_combined_sb'}

#choices for line for cont and dich choice
#assumption that they should be the same so most are the same for the two
#the first is how many top countries do you want, second line asks cumulative from 1 to what do you want to picture
#dictionary chooses what do you want to use for the y-scale as x-scale is time
#titles are self-explanatory 
#line x and y size is choice of font
#line x and y rotation is choice of labels rotation in case of collision in a graph
#line location is the location of the legend 
#line bbox to anchor is where do you want the legend to be anchored to
#i do not recommend changing the parameters below as they have been optimized for appearance, but if you wish to below provides all of the customization wanted
line_fig_size = (20, 15)
line_top = {5, 10}
cumulative_steps_line_charts = {12, 36}
line_dictionary_cm = dictionary_stand_1p_10k
line_dictionary_cm_dich = dichotomous_dictionary_cm
line_title_cm = "Predicted fatalities per month"
line_title_cm_dich = "Predicted probability of conflict per month"
line_x_size = 15
line_y_size = 15
line_x_rotation = 45
line_y_rotation = 0
line_location = 6
line_bbox_to_anchor = (1, 0.5)
line_title_fontsize = 20
line_x_y_labels_fontsize = 20
line_legend_fontsize = 15
#logo is set to be below the graph on right, textbox with description on the left
SAR_logo_x = 0.1
SAR_logo_y = -0.15
SAR_logo_h_w = 0.2
line_textbox_fontsize = 15
line_textbox_position_x = 0.6
line_textbox_position_y = 0
def region_human_name(region_name):
    if region_name == 'globe':
        output = "worldwide"
    elif region_name == "ame":
        output = "in Africa and Middle East"
    elif region_name == "africa":
        output = "in Africa"
    elif region_name == "me":
        output = "in Middle East"
    else: output = f"in countries {region_name}"
    return output


steps_for_dichotomous_line_graphs = {12, 36}

#bar charts
#first choice is which region do you want, i have coded it to allow choices 'globe', 'ame', 'africa', 'me', or a country list
bar_fig_size = (20, 15)
cumulative_steps_bar_charts = {3, 6, 12}
bar_chart_color = 'blue'
bar_chart_title = 'Cumulative predicted fatalities'
bar_chart_title_font = 20
bar_chart_xlabel_font = 20
bar_chart_xtick_font = 15
bar_chart_ylabel_font = 20
bar_chart_ytick_font = 10
bar_textbox_fontsize = 15
bar_textbox_position_x = 0.6
bar_textbox_position_y = 0

bar_SAR_logo_x = 0.1
bar_SAR_logo_y = -0.15
bar_SAR_logo_h_w = 0.2

#note that the bar charts and pie charts are the only ones that need to have graphing of cumulative fatalities. unfortunately, the procedure will vary on whether the variable we are using is not logged or logged. i attempted to make this future proof, but unfortunately, i could not think of a way to do so. so please use single log transformed variable only. dictionary will not be specified either, as the values are automatically transformed into actuals with assumption that the variable is ln1 transformed. 

#pie charts
#which fatality cutoff do you want to use
#which steps do you want to use
#region works same as above
pie_fig_size = (20, 15)
pie_greater_than = {300, 600}
cumulative_steps_pie_charts = {12, 36}
pie_chart_title = 'Cumulative predicted fatalities'
pie_chart_title_font = 25
pie_chart_start_angle = 90
pie_chart_fontsize = 15
pie_chart_labeldistance = 1.05
pie_chart_legend_title = 'Countries'
pie_chart_legend_loc = 6
pie_chart_bbox_to_anchor = (1,0.5)
pie_chart_legend_fontsize = 15
pie_textbox_fontsize = 15
pie_textbox_position_x = 0.6
pie_textbox_position_y = 0.10

pie_SAR_logo_x = 0.0
pie_SAR_logo_y = -0.05
pie_SAR_logo_h_w = 0.2


#change maps
#how many months back do you want to compare the predictions
months_back_comparison_predictions = {1, 3}
#what are the steps you want to map for change maps
steps_wanted_change_maps = {3, 12}



#change maps dictionary
#note that this is consistent with previous examples where the log transformed variable was used
#please therefore make the assignment below for choices for change variable be the ln1 transformed version of the variables
change_raw_values = np.array([-300,-30,-3,3,30,300])
change_values = np.sign(change_raw_values)*np.log(np.abs(change_raw_values)+1)
change_ticklabels = [str(tv) for tv in change_raw_values]
change_dictionary_cm = dict(zip(change_ticklabels, change_values))

change_dictionary_pgm = change_dictionary_cm


#change dictionary for dichotomous outcomes
dich_values_change=np.array([-1.0, -0.8, -0.6, -0.4, -0.2, 0,0.2,0.4,0.6,0.8,1.0])
dich_ticklabels_change=[str(tv) for tv in dich_values_change]
dichotomous_dictionary_change_cm = dict(zip(dich_ticklabels_change, dich_values_change))

dich_values_change2 = np.array([-0.01, 0, 0.01])
dich_ticklabels_change2 = [str(tv) for tv in dich_values_change2]
dichotomous_dictionary_change_pgm = dict(zip(dich_ticklabels_change2, dich_values_change2))


#some specific change map values for cm_change_maps
#note that first converts the original non specific name into a unique identifier
#second dictionary associated a specific variable with what to compare it with
cm_change_variable_cont_conversion = {'step_combined':'ln1_old_sb'}
cm_change_variable_comparison = {'ln1_step_combined_sb':'ln1_old_sb'}

#same for dichotomous
cm_change_variable_dich_conversion = {'step_combined':'old_sb'}
cm_change_variable_comparison_dich = {'step_combined_sb':'old_sb'}



#choice for the feature maps 
#which variables to do you want to be graphed for features 
#note for change variable, choose a ln1 version of the variables
variables_wanted_features_cm_ged = {'ged_sb_ln2', 'ged_ns_ln2', 'ged_os_ln2'}
variables_wanted_features_cm_other = {'vdem_v2x_libdem','gdp_pc_ln1', "wdi_sp_dyn_imrt_in"}
variables_wanted_features_pgm_ged = {'ged_sb_ln2', 'ged_ns_ln2', 'ged_os_ln2'}
variables_wanted_features_cm_change_ged = {'ged_sb_ln1', 'ged_ns_ln1', 'ged_os_ln1'}
variables_wanted_features_pgm_change_ged = {'ged_sb_ln1', 'ged_ns_ln1', 'ged_os_ln1'}

#which months do you want to have a graph of actual fatalities
months_wanted_features = {EndOfHistory, EndOfHistory -1}
#for the features maps, how many months back do you want a comparison
months_back_actual = {1, 3}
#which months do you want graphed
month_wanted_features_change_maps = {EndOfHistory}
#provide a human name for the features variable title
#provide a human name for the features change maps title
features_ged_title_name = 'Actual fatalities'
features_change_title_name = 'Change in actual fatalities'

#custom_dictionaries
#make sure to choose the correct style for the variables you want
#match the names with the names you wish to use below in the defining colormap and dictionary stage
libdem_values=np.array([0,0.2,0.4,0.6,0.8,1.0])
libdem_ticklabels=[str(tv) for tv in libdem_values]
libdem_dictionary = dict(zip(libdem_ticklabels, libdem_values))

gdp_raw_values = np.array([150,500,1500,5000,15000,50000])
gdp_values = np.array(np.log([150,500,1500,5000,15000,50000]))
gdp_ticklabels = [str(tv) for tv in gdp_raw_values]
gdp_dictionary = dict(zip(gdp_ticklabels, gdp_values))

imr_values = np.array([0,20,40,60,80,100])
imr_ticklabels = [str(tv) for tv in imr_values]
imr_dictionary = dict(zip(imr_ticklabels, imr_values))


#input your preferred variable here 
#note that for anything that is fatalities related, we will continue to use the rainbow
#define custom dictionary for the choice of 

#other choices to be defined below
def function_for_non_fatalities(variable_name):
    if variable_name == 'vdem_v2x_libdem': 
        dictionary_run = libdem_dictionary
        cmap_run = 'viridis_r'
        var_name_run = 'liberal democracy index'
    if variable_name == 'gdp_pc_ln1': 
        dictionary_run = gdp_dictionary
        cmap_run = 'viridis_r'
        var_name_run = 'GDP per capita, logged'
    if variable_name == 'wdi_sp_dyn_imrt_in': 
        dictionary_run = imr_dictionary
        cmap_run = 'viridis'
        var_name_run = 'infant mortality rate per 1,000 live births'
    return dictionary_run, cmap_run, var_name_run

def sanity_check2():
    print(f"{user}, for maps of predictions, you have chosen steps {steps_wanted_prediction_fat}. for line charts you have chosen steps {cumulative_steps_line_charts}, for dichotomous line graphs you have chosen steps {steps_for_dichotomous_line_graphs}, for bar charts you have chosen steps {cumulative_steps_bar_charts}, for pie charts you have chosen {cumulative_steps_pie_charts}, for change maps you have chosen to look back by {months_back_comparison_predictions} steps/months and you have chosen to map steps {steps_wanted_change_maps}. for features maps you have chosen to look back by {months_back_actual}")
