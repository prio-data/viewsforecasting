from Tools.visualization_assetts_fat002_add.config1 import*
from Tools.visualization_assetts_fat002_add.geo_coverage_determination import *

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

#choice for the feature maps 
#which variables to do you want to be graphed for features 
#note for change variable, choose a ln1 version of the variables
variables_wanted_features_cm_ged = {'ged_sb_ln2', 'ged_ns_ln2', 'ged_os_ln2'}
variables_wanted_features_pgm_ged = {'ged_sb_ln2', 'ged_ns_ln2', 'ged_os_ln2'}

#which months do you want to have a graph of actual fatalities
months_wanted_features = months_wanted
#provide a human name for the features variable title
#provide a human name for the features change maps title
features_ged_title_name = 'Actual fatalities'



