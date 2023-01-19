from Tools.visualization_assetts.config2 import *
from Tools.visualization_assetts.folder_creation import *

#fetch the data from queryset

features_qs = (Queryset("Monthly_update_features_cm", "country_month"))
features_cm=features_qs.fetch()

#create new variables, note this part to be moved into queryset when new querysetting is ready
features_cm['gdp_pc']=features_cm['wdi_ny_gdp_mktp_kd']/features_cm['wdi_sp_pop_totl']
features_cm['gdp_pc_ln1']=np.log(features_cm['gdp_pc'])

print(f'{user} cm_current_data fetched successfully')

#obtaining cm level geometries
engine = sa.create_engine(source_db_path)
gdf_ci_master = gpd.GeoDataFrame.from_postgis(
    "SELECT id as country_id, name, in_africa, in_me, geom FROM prod.country",
    engine,
    geom_col='geom'
)
gdf_ci_master = gdf_ci_master.to_crs(4326)
print(f'{user} gdf_ci_master fetched successfully')


def features_cm_level_mapping_ged():
    #cm level features mapping, ged

    #prep data
    data= features_cm.copy()
    gdf = gdf_ci_master.copy()

    data = data.join(gdf.set_index("country_id"))
    gdf = gpd.GeoDataFrame(data, geometry="geom")

    #savefolder
    features_cm_folder = master_folder+'/Features/Maps/cm/'

    #looping informationa
    variable_loop = variables_wanted_features_cm_ged
    dictionary_run = fatality_dictionary_cm
    cmap_run = fatality_colormap
    steps_loop = months_wanted_features

    for step in steps_loop:
        for variable in variable_loop:
            for region_name in geo_coverage_loop:
                data_run = gdf.loc[step]
                var_run = variable
                var_name_run = find_the_violence_type(variable)
                var_run_savefile = give_me_violence_string_label_only(variable)
                bbox_run = bbox_from_cid_region(region_name)                       

                #making the choice of textbox size
                textbox_font_size = function_for_textbox(region_name)

                title_run = f'{features_ged_title_name} in {str(vid2date(step))}, {var_name_run}'
                textbox = f'Name: features,\n{var_run}_at_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                savefile = f'{features_cm_folder}GED_cm{var_run_savefile}_{region_name}_{cmap_run}_month{step}.png'

                if region_name in ('globe', 'ame', 'africa'):
                    map_run=Mapper2(
                        width=width_global,
                        height=height_global,
                        frame_on=True,
                        title=title_run,
                        bbox=bbox_run
                    ).add_layer(
                        gdf=data_run,
                        map_dictionary=dictionary_run,
                        cmap='binary',
                        edgecolor="black",
                        linewidth=0.5,
                        transparency = 1.0,
                        column=var_run
                    ).add_mask(
                        gdf = data_run,
                        map_dictionary = dictionary_run,
                        cmap = cmap_run,
                        transparency = 1,
                        masking_location = region_name,
                        column=var_run,
                        edgecolor="black",
                        linewidth=1
                    ).add_views_textbox(
                        text=textbox,
                        textsize=textbox_font_size)

                    map_run.save(savefile)
                else:
                    map_run=Mapper2(
                        width=width_global,
                        height=height_global,
                        frame_on=True,
                        title=title_run,
                        bbox=bbox_run
                    ).add_mask(
                        gdf = data_run,
                        map_dictionary = dictionary_run,
                        cmap = cmap_run,
                        transparency = country_mapping_transparency_global,
                        background = country_background_global,
                        masking_location = str(cid2name(region_name)),
                        column=var_run,
                        edgecolor="black",
                        linewidth=1, 
                        views_experimental_labels = views_experimental_font_global
                    ).add_views_textbox(
                        text=textbox,
                        textsize=textbox_font_size)

                    map_run.save(savefile)
    print(f'{user}, cm maps for ged completed')




def features_cm_maps_all_others():
    #cm features map, all others
    #prep data
    data= features_cm.copy()
    gdf = gdf_ci_master.copy()

    data = data.join(gdf.set_index("country_id"))
    gdf = gpd.GeoDataFrame(data, geometry="geom")

    #savefolder
    features_cm_folder = master_folder+'/Features/Maps/cm/'

    #looping information
    variable_loop = variables_wanted_features_cm_other
    steps_loop = months_wanted_features

    for step in steps_loop:
        for variable in variable_loop:
            for region_name in geo_coverage_loop:
                data_run = gdf.loc[step]
                var_run = variable
                var_name_run = function_for_non_fatalities(variable)[2]
                cmap_run = function_for_non_fatalities(variable)[1]
                dictionary_run = function_for_non_fatalities(variable)[0]

                textbox_font_size = function_for_textbox(region_name)

                var_run_savefile = variable
                bbox_run = bbox_from_cid(region_name)                       

                title_run = f'{var_name_run} in {str(vid2date(step))}'
                textbox = f'Name: features,\n{var_run}_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                savefile = f'{features_cm_folder}{var_run_savefile}_cm_{region_name}_{cmap_run}_month{step}.png'

                if region_name in ('globe', 'ame', 'africa'):
                    map_run=Mapper2(
                        width=width_global,
                        height= height_global,
                        frame_on=True,
                        title=title_run,
                        bbox=bbox_run
                    ).add_layer(
                        gdf=data_run,
                        map_dictionary=dictionary_run,
                        cmap='binary',
                        edgecolor="black",
                        linewidth=0.5,
                        transparency = 1.0,
                        column=var_run
                    ).add_mask(
                        gdf = data_run,
                        map_dictionary = dictionary_run,
                        cmap = cmap_run,
                        transparency = 1,
                        masking_location = region_name,
                        column=var_run,
                        edgecolor="black",
                        linewidth=1
                    ).add_views_textbox(
                        text=textbox,
                        textsize=textbox_font_size)

                    map_run.save(savefile)
                else:
                    map_run=Mapper2(
                        width=width_global,
                        height=height_global,
                        frame_on=True,
                        title=title_run,
                        bbox=bbox_run
                    ).add_mask(
                        gdf = data_run,
                        map_dictionary = dictionary_run,
                        cmap = cmap_run,
                        transparency = country_mapping_transparency_global,
                        background = country_background_global,
                        masking_location = str(cid2name(region_name)),
                        column=var_run,
                        edgecolor="black",
                        linewidth=1, 
                        views_experimental_labels = views_experimental_font_global
                    ).add_views_textbox(
                        text=textbox,
                        textsize=textbox_font_size)

                    map_run.save(savefile)
    print(f'{user}, cm maps for all other variables completed')
    
    
    
    
    
def features_cm_change_maps():
    #note change maps will denote the following, increase from the past is red (things got worse, more fatalities)
    #decrease is blue (things got better, less fatalities)
    #no change is white

    for delta in months_back_actual:
        for variable in variables_wanted_features_cm_change_ged:
            column = variable
            actual = np.exp(features_cm[column]) - 1
            shifted = np.exp(features_cm[column].groupby(level = 1).shift(periods = delta)) - 1
            change_run_column = f'ln1_delta_{delta}_{column}'
            features_cm[change_run_column] = np.sign(actual-shifted)*np.log(np.abs(actual-shifted)+1)

            data= features_cm.copy()
            gdf = gdf_ci_master.copy()

            data = data.join(gdf.set_index("country_id"))
            gdf = gpd.GeoDataFrame(data, geometry="geom")

            #savefolder
            features_change_cm_folder = master_folder+'/Features/ChangeMaps/cm/'

            #looping information

            variable_loop = {change_run_column}
            steps_loop = month_wanted_features_change_maps

            #custom dictionary for this run
            dictionary_run = change_dictionary_cm
            cmap_run = change_colormap_global


            for step in steps_loop:
                for variable in variable_loop:
                    for region_name in geo_coverage_loop:
                        data_run = gdf.loc[step]
                        var_run = variable
                        var_name_run = find_the_violence_type(variable)
                        var_run_savefile = variable
                        bbox_run = bbox_from_cid(region_name)

                        textbox_font_size = function_for_textbox(region_name)

                        title_run = f'{features_change_title_name} from {delta} month ago on {str(vid2date(step))}, {var_name_run}'
                        textbox = f'Name: features,\n{var_run}_at_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                        savefile = f'{features_change_cm_folder}ChangeMaps_GED_cm_{variable}_{region_name}_{change_colormap_global}_month{step}.png'

                        if region_name in ('globe', 'ame', 'africa'):
                            map_run=Mapper2(
                                width=width_global,
                                height=height_global,
                                frame_on=True,
                                title=title_run,
                                bbox=bbox_run
                            ).add_layer(
                                gdf=data_run,
                            map_dictionary=dictionary_run,
                                cmap='binary',
                                edgecolor="black",
                                linewidth=0.5,
                                transparency = 1.0,
                                column=var_run
                            ).add_mask(
                                gdf = data_run,
                                map_dictionary = dictionary_run,
                                cmap = cmap_run,
                                transparency = 1,
                                masking_location = region_name,
                                column=var_run,
                                edgecolor="black",
                                linewidth=1
                            ).add_views_textbox(
                                text=textbox,
                                textsize=textbox_font_size)

                            map_run.save(savefile)
                        else:
                            map_run=Mapper2(
                                width=width_global,
                                height=height_global,
                                frame_on=True,
                                title=title_run,
                                bbox=bbox_run
                            ).add_mask(
                                gdf = data_run,
                                map_dictionary = dictionary_run,
                                cmap = cmap_run,
                                transparency = country_mapping_transparency_global,
                                background = country_background_global,
                                masking_location = str(cid2name(region_name)),
                                column=var_run,
                                edgecolor="black",
                                linewidth=1, 
                                views_experimental_labels = views_experimental_font_global
                            ).add_views_textbox(
                                text=textbox,
                                textsize=textbox_font_size)

                            map_run.save(savefile)
    print(f'{user}, cm change maps for ged completed')
    