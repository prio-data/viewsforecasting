from Tools.visualization_assetts.config2 import *
from Tools.visualization_assetts.folder_creation import *


#fetching geometries
engine = sa.create_engine(source_db_path)
gdf_pid = gpd.GeoDataFrame.from_postgis(
    "SELECT id as priogrid_gid, in_africa, in_me, geom FROM prod.priogrid", 
    engine, 
    geom_col='geom'
)
gdf_pid = gdf_pid.to_crs(4326)

#now grab the country names
pg_country_queryset = (Queryset("m_associate_country_2_priogrid", "priogrid_month"))

pg_country = pg_country_queryset.fetch().reset_index()
#pg_country_cleaned = pg_country.reset_index().drop(['month_id'], axis = 1).drop_duplicates(subset=['priogrid_gid'])

gdf_pid_master = pd.merge(left = gdf_pid, right = pg_country, left_on = 'priogrid_gid', 
                          right_on = 'priogrid_gid', how = 'right').set_index(['month_id', 'priogrid_gid'])


#grab country geometries for borders creation
gdf_ci_master = gpd.GeoDataFrame.from_postgis(
    "SELECT id as country_id, name, in_africa, in_me, geom FROM prod.country",
    engine,
    geom_col='geom'
)
gdf_ci_master = gdf_ci_master.to_crs(4326)

print(f'{user}, pgm geometries fetching completed')


#read in future predictions at pgm level from internal storage

predstore_future = 'pgm_' + model_wanted_pgm + '_f' + str(EndOfHistory)
predstore_future_dich = 'pgm_' +  model_wanted_pgm + '_dich_f' + str(EndOfHistory)

predictions_df = pd.DataFrame.forecasts.read_store(predstore_future, run=dev_id)
predictions_df = predictions_df.reset_index()
predictions_df['step'] = predictions_df['month_id'] - EndOfHistory
predictions_df = predictions_df.set_index(['step', 'priogrid_id'], drop = True)
predictions_df.rename(columns = prediction_cont_name_default, inplace = True)
if do_we_need_to_double_log_cont_variable == 'yes':
    for i in prediction_cont_name_double_logged: predictions_df[i['new_name']]=np.log1p(predictions_df[i['old_name']])

predictions_dich_df = pd.DataFrame.forecasts.read_store(predstore_future_dich, run=dev_id)
predictions_dich_df = predictions_dich_df.reset_index()
predictions_dich_df['step'] = predictions_dich_df['month_id'] - EndOfHistory
predictions_dich_df = predictions_dich_df.set_index(['step', 'priogrid_id'], drop = True)
predictions_dich_df.rename(columns = prediction_dich_name_default, inplace = True)

print(f'{user}, prediction data at pgm level successfully fetched')

def predictions_pgm_maps_cont():
    #for predictions, we have chosen steps we wanted earlier

    #prep data
    #this process took a while and we technically just need the end of history month
    data= predictions_df.copy().reset_index().set_index(['priogrid_id'])
    gdf = gdf_pid_master.copy().query(f"month_id == {EndOfHistory}").reset_index().drop('month_id', axis = 1).rename(columns = {'priogrid_gid':'priogrid_id'}).set_index(['priogrid_id'])

    data_pid = pd.merge(left = data, right = gdf, left_index = True, right_index = True, how= 'left').reset_index().set_index(['step', 'priogrid_id'])

    gdf = gpd.GeoDataFrame(data_pid, geometry="geom")
    gdf_c = gdf_ci_master.copy()

    #savefolder
    predictions_pgm_folder = master_folder+'/Continuous/Ensemble/ForecastMaps/pgm/'

    #looping informationa
    variable_loop = variables_wanted_predictions
    dictionary_run = fatality_dictionary_pgm
    cmap_run = fatality_colormap
    steps_loop = steps_wanted_prediction_fat

    for step in steps_loop:
        for variable in variable_loop:
            for region_name in geo_coverage_loop:
                data_run = gdf.loc[step]
                var_run = variable
                var_name_run = find_the_violence_type(variable)
                var_run_savefile = give_me_violence_string_label_only(variable)
                bbox_run = bbox_from_cid_region(region_name)
                month_id = step+EndOfHistory

                #making the choice of textbox size
                textbox_font_size = function_for_textbox(region_name)

                 #masking_choices
                if str(region_name) in('globe'):
                    masking_run = 'globe'
                    background2 = None
                elif str(region_name) in ('ame'):
                    masking_run = 'ame'
                    background2 = None
                elif str(region_name) in ('africa'):
                    masking_run = 'africa'
                    background2 = None
                else:
                    masking_run = cid2name(region_name)
                    background2 = pgm_background_country_level

                title_run = f'{prediction_title_name} in {str(vid2date(month_id))}, {var_name_run}'
                textbox = f'Name: {dev_id}_{model_wanted}_{model_attempt},\n{var_run}_at_step{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                savefile = f'{predictions_pgm_folder}{dev_id}_cm_{var_run_savefile}_{region_name}_{cmap_run}_step{step}.png'
                
                try:
                    masked=Mapper2(
                        width=width_global,
                        height=height_global,
                        frame_on=True,
                        title=title_run,
                        bbox=bbox_run
                    ).add_mask(
                        gdf = data_run,
                        map_dictionary = dictionary_run,
                        cmap = cmap_run,
                        transparency = 1,
                        masking_location = masking_run,
                        column=var_run,
                        background = background2,
                        edgecolor="black",
                        linewidth=0.5
                    ).add_views_textbox(
                        text=textbox,
                        textsize=textbox_font_size)

                    ax = masked.ax

                    masked_with_borders = gdf_c.plot(ax=ax, edgecolor = 'black', linewidth = 2.0, facecolor = 'None')
                    plt.savefig(savefile, dpi = pgm_dpi_global)

                    plt.close()
                
                except:
                    print(f"{user}, sorry {region_name} not available in pgm yet")
                    plt.close()
    print(f'{user}, pgm prediction cont maps completed')
    
    
    
    
    
def predictions_pgm_maps_dich():
    #for predictions, we have chosen steps we wanted earlier

    #prep data
    #this process took a while and we technically just need the end of history month
    data= predictions_dich_df.copy().reset_index().set_index(['priogrid_id'])
    for variable in variables_wanted_predictions_dich:
        data[variable] = np.where(data[variable] == 0, 0.000001, data[variable])
        data[variable] = np.where(data[variable] == 1, 0.999999, data[variable])
        data[variable] = logit(data[variable])
    
    gdf = gdf_pid_master.copy().query(f"month_id == {EndOfHistory}").reset_index().drop('month_id', axis = 1).rename(columns = {'priogrid_gid':'priogrid_id'}).set_index(['priogrid_id'])

    data_pid = pd.merge(left = data, right = gdf, left_index = True, right_index = True, how= 'left').reset_index().set_index(['step', 'priogrid_id'])

    gdf = gpd.GeoDataFrame(data_pid, geometry="geom")
    gdf_c = gdf_ci_master.copy()

    #savefolder
    predictions_pgm_folder = master_folder+'/Dichotomous/Ensemble/ForecastMaps/pgm/'

    #looping informationa
    variable_loop = variables_wanted_predictions_dich
    dictionary_run = dictionary_dichotomous_pgm
    cmap_run = fatality_colormap
    steps_loop = steps_wanted_prediction_fat

    for step in steps_loop:
        for variable in variable_loop:
            for region_name in geo_coverage_loop:
                data_run = gdf.loc[step]
                var_run = variable
                var_name_run = find_the_violence_type(variable)
                var_run_savefile = give_me_violence_string_label_only(variable)
                bbox_run = bbox_from_cid_region(region_name)
                month_id = step+EndOfHistory

                #making the choice of textbox size
                textbox_font_size = function_for_textbox(region_name)

                 #masking_choices
                if str(region_name) in('globe'):
                    masking_run = 'globe'
                    background2 = None
                elif str(region_name) in ('ame'):
                    masking_run = 'ame'
                    background2 = None
                elif str(region_name) in ('africa'):
                    masking_run = 'africa'
                    background2 = None
                else:
                    masking_run = cid2name(region_name)
                    background2 = pgm_background_country_level

                title_run = f'{prediction_title_name} in {str(vid2date(month_id))}, {var_name_run}'
                textbox = f'Name: {dev_id}_{model_wanted}_{model_attempt},\n{var_run}_at_step{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                savefile = f'{predictions_pgm_folder}{dev_id}_cm_{var_run_savefile}_{region_name}_{cmap_run}_step{step}.png'
                
                try:
                    masked=Mapper2(
                        width=width_global,
                        height=height_global,
                        frame_on=True,
                        title=title_run,
                        bbox=bbox_run
                    ).add_mask(
                        gdf = data_run,
                        map_dictionary = dictionary_run,
                        cmap = cmap_run,
                        transparency = 1,
                        masking_location = masking_run,
                        column=var_run,
                        background = background2,
                        edgecolor="black",
                        linewidth=0.5
                    ).add_views_textbox(
                        text=textbox,
                        textsize=textbox_font_size)

                    ax = masked.ax

                    masked_with_borders = gdf_c.plot(ax=ax, edgecolor = 'black', linewidth = 2.0, facecolor = 'None')
                    plt.savefig(savefile, dpi = pgm_dpi_global)

                    plt.close()
                
                except:
                    print(f"{user}, sorry {region_name} not available in pgm yet")
                    plt.close()
                    
    print(f'{user}, pgm prediction dich maps completed')
    
    
    
    
def predictions_pgm_maps_cont_change1():
    #continuous_changes_vs_actuals_or_running_average
    data = predictions_df.copy()
    historic = Queryset("Monthly_update_features_pgm", "priogrid_month").fetch()[['ged_sb_ln1', 'ged_ns_ln1', 'ged_os_ln1']]
    end_of_history = historic.query(f'month_id == {EndOfHistory}')
    data2 = pd.merge(data.reset_index(), end_of_history, left_on = 'priogrid_id', right_on = 'priogrid_gid', how = 'left').set_index(['step', 'priogrid_id'])
    rolling_average = Queryset("Monthly_update_running_average_pgm", "country_month").fetch()
    rolling_average_end_of_history = rolling_average.query(f'month_id == {EndOfHistory}')
    data3 = pd.merge(data2.reset_index(), rolling_average_end_of_history, left_on = 'priogrid_id', right_on = 'priogrid_gid', how = 'left').set_index(['step', 'priogrid_id'])

    for variable, variable_old in cm_change_variable_comparison.items():
        conf = give_me_violence_string_label_only(variable)
        if conf == '_sb': variables_to_compare = {'ged_sb_ln1', 'ged_sb_run_average_6_ln1'}
        elif conf == '_ns': variables_to_compare = {'ged_ns_ln1', 'ged_ns_run_average_6_ln1'}
        elif conf == '_os': variables_compare = {'ged_os_ln1', 'ged_os_run_average_6_ln1'}
        else: print('variable name does not specify violence type, make sure it does')
        column_prediction = variable
        variable_loop = []
        for column_comparison in variables_to_compare:
            actual_prediction = np.exp(data3[column_prediction])-1
            actual_comparison = np.exp(data3[column_comparison])-1
            temp_change_name = f'change_from_{column_comparison}'
            data3[temp_change_name] = np.sign(actual_prediction - actual_comparison)*np.log(np.abs(actual_prediction - actual_comparison)+1)
            variable_loop.append(temp_change_name)


    #geometries
    gdf = gdf_pid_master.copy().query(f"month_id == {EndOfHistory}").reset_index().drop('month_id', axis = 1).rename(columns = {'priogrid_gid':'priogrid_id'}).set_index(['priogrid_id'])
    data4 = pd.merge(data3.reset_index().set_index(['priogrid_id']), gdf.reset_index().set_index(['priogrid_id']), left_index = True, right_index = True, how = 'left').reset_index().set_index(['step', 'priogrid_id'])
    gdf = gpd.GeoDataFrame(data4, geometry = "geom")
    gdf_c = gdf_ci_master.copy()

    cm_predictions_change_maps_folder = master_folder + '/Continuous/Ensemble/ChangeMaps/pgm/'

    steps_loop = steps_wanted_change_maps
    dictionary_run = change_dictionary_pgm
    cmap_run = change_colormap_global

    for step in steps_loop:
        for variable in variable_loop:
            for region_name in geo_coverage_loop:
                data_run = gdf.loc[step]
                var_run = variable
                var_name_run = find_the_violence_type(variable)
                var_run_savefile = variable
                bbox_run = bbox_from_cid(region_name)
                month_id_temp = step+EndOfHistory

                textbox_font_size = function_for_textbox(region_name)

                 #masking_choices
                if str(region_name) in('globe'):
                    masking_run = 'globe'
                    background2 = None
                elif str(region_name) in ('ame'):
                    masking_run = 'ame'
                    background2 = None
                elif str(region_name) in ('africa'):
                    masking_run = 'africa'
                    background2 = None
                else:
                    masking_run = cid2name(region_name)
                    background2 = pgm_background_country_level

                if 'ged_sb_ln1' or 'ged_ns_ln1' or 'ged_os_ln1' in variable: human_name = 'actual at last month available'
                if 'ged_sb_run_average_6_ln1' or 'ged_ns_run_average_6_ln1' or 'ged_os_run_average_6_ln1' in variable: human_name = 'running average at last month available'
                title_run = f'Change of prediction from {human_name}, date {str(vid2date(month_id_temp))}, {var_name_run}'
                textbox = f'Name: {dev_id}_{model_wanted}_{model_attempt},\n{var_run}_at_step{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                savefile = f'{cm_predictions_change_maps_folder}ChangeMaps_{dev_id}_cm_{var_run_savefile}_{region_name}_{cmap_run}_step{step}.png'
                
                try:
                    masked=Mapper2(
                        width=width_global,
                        height=height_global,
                        frame_on=True,
                        title=title_run,
                        bbox=bbox_run
                    ).add_mask(
                        gdf = data_run,
                        map_dictionary = dictionary_run,
                        cmap = cmap_run,
                        transparency = 1,
                        masking_location = masking_run,
                        column=var_run,
                        background = background2,
                        edgecolor="black",
                        linewidth=0.5
                    ).add_views_textbox(
                        text=textbox,
                        textsize=textbox_font_size)

                    ax = masked.ax

                    masked_with_borders = gdf_c.plot(ax=ax, edgecolor = 'black', linewidth = 2.0, facecolor = 'None')
                    plt.savefig(savefile, dpi = pgm_dpi_global)

                    plt.close()
                
                except:
                    print(f"{user}, sorry {region_name} not available in pgm yet")
                    plt.close()

    print(f'{user}, pgm prediction change maps from actuals completed')
    
    
    
    
def predictions_pgm_maps_cont_change2():
    data = predictions_df.copy()

    for variable_pred, variable_old in cm_change_variable_comparison.items():
        for months_back in months_back_comparison_predictions:
            column_prediction = variable_pred
            pred_old = 'pgm_' + model_wanted_pgm + '_f' + str(EndOfHistory-months_back)
            temp_old = pd.DataFrame.forecasts.read_store(pred_old, run = dev_id_comparison)
            temp_old2 = temp_old.reset_index()
            temp_old2['step'] = temp_old2['month_id'] - (EndOfHistory-months_back)
            temp_old2.rename(columns =cm_change_variable_cont_conversion , inplace = True)

            temp_old_name = f'{variable_old}_mb_{months_back}'
            temp_old2[temp_old_name] = temp_old2[variable_old]
            column_comparison = temp_old_name

            for method_merge in {'step', 'month_id'}:
                data_merged = pd.merge(data.reset_index(), temp_old2.reset_index(), left_on = (method_merge, 'priogrid_id'), right_on = (method_merge, 'priogrid_id'), how = 'left', suffixes = ('','_y')).set_index(['step', 'priogrid_id'])

                actual_prediction = np.exp(data_merged[column_prediction])-1
                actual_comparison = np.exp(data_merged[column_comparison])-1
                temp_change_name = f'change_from_{column_comparison}'
                data_merged[temp_change_name] = np.sign(actual_prediction - actual_comparison)*np.log(np.abs(actual_prediction - actual_comparison)+1)
                variable = temp_change_name

                gdf = gdf_pid_master.copy().query(f"month_id == {EndOfHistory}").reset_index().drop('month_id', axis = 1).rename(columns = {'priogrid_gid':'priogrid_id'}).set_index(['priogrid_id'])
                data_merged2 = pd.merge(data_merged.reset_index().set_index(['priogrid_id']), gdf.reset_index().set_index(['priogrid_id']), left_index = True, right_index = True, how = 'left').reset_index().set_index(['step', 'priogrid_id'])
                gdf = gpd.GeoDataFrame(data_merged2, geometry = "geom")
                gdf_c = gdf_ci_master.copy()

                cm_predictions_change_maps_folder = master_folder + '/Continuous/Ensemble/ChangeMaps/pgm/'

                steps_loop = steps_wanted_change_maps
                dictionary_run = change_dictionary_pgm
                cmap_run = change_colormap_global


                for step in steps_loop:
                    for region_name in geo_coverage_loop:
                        data_run = gdf.loc[step]
                        var_run = variable
                        var_name_run = find_the_violence_type(variable)
                        var_run_savefile = variable
                        bbox_run = bbox_from_cid(region_name)
                        month_id_temp = step+EndOfHistory

                        textbox_font_size = function_for_textbox(region_name)

                        #masking_choices
                        if str(region_name) in('globe'):
                            masking_run = 'globe'
                            background2 = None
                        elif str(region_name) in ('ame'):
                            masking_run = 'ame'
                            background2 = None
                        elif str(region_name) in ('africa'):
                            masking_run = 'africa'
                            background2 = None
                        else:
                            masking_run = cid2name(region_name)
                            background2 = pgm_background_country_level

                        title_run = f'Change of prediction from {pred_old} model {months_back} months back at same {method_merge} on {str(vid2date(month_id_temp))}, {var_name_run}'
                        textbox = f'Name: {dev_id}_{model_wanted}_{model_attempt},\n{var_run}_matched_by_{method_merge}_at_step{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                        savefile = f'{cm_predictions_change_maps_folder}ChangeMaps_{dev_id}_cm_vs_{pred_old}_variable_{var_run_savefile}_matched_by_{method_merge}_{region_name}_{cmap_run}_step{step}.png'
                        
                        try:
                            masked=Mapper2(
                                width=width_global,
                                height=height_global,
                                frame_on=True,
                                title=title_run,
                                bbox=bbox_run
                            ).add_mask(
                                gdf = data_run,
                                map_dictionary = dictionary_run,
                                cmap = cmap_run,
                                transparency = 1,
                                masking_location = masking_run,
                                column=var_run,
                                background = background2,
                                edgecolor="black",
                                linewidth=0.5
                            ).add_views_textbox(
                                text=textbox,
                                textsize=textbox_font_size)

                            ax = masked.ax

                            masked_with_borders = gdf_c.plot(ax=ax, edgecolor = 'black', linewidth = 2.0, facecolor = 'None')
                            plt.savefig(savefile, dpi = pgm_dpi_global)

                            plt.close()
                        
                        except:
                            print(f"{user}, sorry {region_name} not available in pgm yet")
                            plt.close()


    print(f'{user}, pgm prediction maps from previous prediction completed')
    
    
    
    
def predictions_pgm_maps_dich_change():
    data = predictions_dich_df.copy()

    for variable_pred, variable_old in cm_change_variable_comparison_dich.items():
        for months_back in months_back_comparison_predictions:
            column_prediction = variable_pred
            pred_old = 'pgm_' + model_wanted_pgm + '_dich_f' + str(EndOfHistory-months_back)
            temp_old = pd.DataFrame.forecasts.read_store(pred_old, run = dev_id_comparison)
            temp_old2 = temp_old.reset_index()
            temp_old2['step'] = temp_old2['month_id'] - (EndOfHistory-months_back)
            temp_old2.rename(columns =cm_change_variable_dich_conversion , inplace = True)

            temp_old_name = f'{variable_old}_mb_{months_back}'
            temp_old2[temp_old_name] = temp_old2[variable_old]
            column_comparison = temp_old_name

            for method_merge in {'step', 'month_id'}:
                data_merged = pd.merge(data.reset_index(), temp_old2.reset_index(), left_on = (method_merge, 'priogrid_id'), right_on = (method_merge, 'priogrid_id'), how = 'left', suffixes = ('','_y')).set_index(['step', 'priogrid_id'])

                actual_prediction = data_merged[column_prediction]
                actual_comparison = data_merged[column_comparison]
                temp_change_name = f'change_from_{column_comparison}'
                data_merged[temp_change_name] = np.sign(actual_prediction - actual_comparison)*(np.abs(actual_prediction - actual_comparison))
                variable = temp_change_name

                gdf = gdf_pid_master.copy().query(f"month_id == {EndOfHistory}").reset_index().drop('month_id', axis = 1).rename(columns = {'priogrid_gid':'priogrid_id'}).set_index(['priogrid_id'])
                data_merged2 = pd.merge(data_merged.reset_index().set_index(['priogrid_id']), gdf.reset_index().set_index(['priogrid_id']), left_index = True, right_index = True, how = 'left').reset_index().set_index(['step', 'priogrid_id'])
                gdf = gpd.GeoDataFrame(data_merged2, geometry = "geom")
                gdf_c = gdf_ci_master.copy()

                cm_predictions_change_maps_folder = master_folder + '/Dichotomous/Ensemble/ChangeMaps/pgm/'

                steps_loop = steps_wanted_change_maps
                dictionary_run = dichotomous_dictionary_change_pgm
                cmap_run = change_colormap_global


                for step in steps_loop:
                    for region_name in geo_coverage_loop:
                        data_run = gdf.loc[step]
                        var_run = variable
                        var_name_run = find_the_violence_type(variable)
                        var_run_savefile = variable
                        bbox_run = bbox_from_cid(region_name)
                        month_id_temp = step+EndOfHistory

                        textbox_font_size = function_for_textbox(region_name)

                        #masking_choices
                        if str(region_name) in('globe'):
                            masking_run = 'globe'
                            background2 = None
                        elif str(region_name) in ('ame'):
                            masking_run = 'ame'
                            background2 = None
                        elif str(region_name) in ('africa'):
                            masking_run = 'africa'
                            background2 = None
                        else:
                            masking_run = cid2name(region_name)
                            background2 = pgm_background_country_level

                        title_run = f'Change of prediction from {pred_old} model {months_back} months back at same {method_merge} on {str(vid2date(month_id_temp))}, {var_name_run}'
                        textbox = f'Name: {dev_id}_{model_wanted}_{model_attempt},\n{var_run}_matched_by_{method_merge}_at_step{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                        savefile = f'{cm_predictions_change_maps_folder}ChangeMaps_{dev_id}_cm_vs_{pred_old}_variable_{var_run_savefile}_matched_by_{method_merge}_{region_name}_{cmap_run}_step{step}.png'
                        
                        try:
                            masked=Mapper2(
                                width=width_global,
                                height=height_global,
                                frame_on=True,
                                title=title_run,
                                bbox=bbox_run
                            ).add_mask(
                                gdf = data_run,
                                map_dictionary = dictionary_run,
                                cmap = cmap_run,
                                transparency = 1,
                                masking_location = masking_run,
                                column=var_run,
                                background = background2,
                                edgecolor="black",
                                linewidth=0.5
                            ).add_views_textbox(
                                text=textbox,
                                textsize=textbox_font_size)

                            ax = masked.ax

                            masked_with_borders = gdf_c.plot(ax=ax, edgecolor = 'black', linewidth = 2.0, facecolor = 'None')
                            plt.savefig(savefile, dpi = pgm_dpi_global)

                            plt.close()
                        
                        
                        
                        except:
                            print(f"{user}, sorry {region_name} not available in pgm yet")
                            plt.close()


    print(f'{user}, pgm prediction dichotomous maps from previous prediction completed')
