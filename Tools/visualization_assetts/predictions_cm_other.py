from Tools.visualization_assetts.config2 import *
from Tools.visualization_assetts.folder_creation import *
from Tools.visualization_assetts.SAR_logo_import import *
SAR_logo = import_SAR_logo()

#obtaining cm level geometries
engine = sa.create_engine(source_db_path)
gdf_ci_master = gpd.GeoDataFrame.from_postgis(
    "SELECT id as country_id, name, in_africa, in_me, geom FROM prod.country",
    engine,
    geom_col='geom'
)
gdf_ci_master = gdf_ci_master.to_crs(4326)
print(f'{user} gdf_ci_master fetched successfully')

#Read in future predictions at cm level as given by the parameters above
#note that the output step combined is already log transformed

predstore_future =  'cm_' + model_wanted + '_f' + str(EndOfHistory)
predstore_future_dich = 'cm_' + model_wanted + '_dich_f' + str(EndOfHistory)

predictions_df = pd.DataFrame.forecasts.read_store(predstore_future, run=dev_id)
predictions_df = predictions_df.reset_index()
predictions_df['step'] = predictions_df['month_id'] - EndOfHistory
predictions_df = predictions_df.set_index(['step', 'country_id'], drop = True)
predictions_df.rename(columns = prediction_cont_name_default, inplace = True)
if do_we_need_to_double_log_cont_variable == 'yes':
    for i in prediction_cont_name_double_logged: predictions_df[i['new_name']]=np.log1p(predictions_df[i['old_name']])


predictions_dich_df = pd.DataFrame.forecasts.read_store(predstore_future_dich, run=dev_id)
predictions_dich_df = predictions_dich_df.reset_index()
predictions_dich_df['step'] = predictions_dich_df['month_id'] - EndOfHistory
predictions_dich_df = predictions_dich_df.set_index(['step', 'country_id'], drop = True)
predictions_dich_df.rename(columns = prediction_dich_name_default, inplace = True)

print(f'{user}, prediction data at cm level successfully fetched')

def predictions_cm_cont_line():
    #continuous, linear, cm
    ContinuousLineGraph = master_folder + '/Continuous/Ensemble/LineGraphs/'

    data = predictions_df.copy()
    steps_end_loop = cumulative_steps_line_charts
    how_many_countries = line_top
    variable_loop = variables_wanted_predictions_line_bar_pie
    regions_loop = line_chart_region

    for region in regions_loop:
        for top_country in how_many_countries:
            for end_step in steps_end_loop:
                for variable in variable_loop:
                    country_name_and_regions_master = Queryset('Monthly_update_country_names_and_regions', 'country_month').fetch().reset_index().drop(columns = ['month_id']).drop_duplicates()

                    country_data = country_name_and_regions_master.copy()
                    line_charts_data = pd.merge(left = data.reset_index(), right = country_data, left_on = ('country_id'), right_on = ('country_id'), how = 'left').reset_index().set_index(['step', 'country_id'])

                    if region == 'globe':
                        temp = line_charts_data
                    elif region == 'ame':
                        temp = line_charts_data.query('in_africa == 1 or in_me == 1')
                    elif region == 'africa':
                        temp = line_charts_data.query('in_africa == 1')
                    elif region == 'me':
                        temp = line_charts_data.query('in_me == 1')
                    else: temp = line_charts_data.query(f'country_id in {region}')

                    country_list_run = give_me_topX_country_id_cumulative(df=temp, time_index = 'step', number_wanted = top_country, variable = variable, start = 1, end = end_step, variable_transformation = line_bar_pie_variable_transformation)

                    #subset the data
                    temporary_df = temp.iloc[temp.index.get_level_values('step') <= end_step]
                    data_run = temporary_df[temporary_df.index.get_level_values('country_id').isin(country_list_run)].reset_index().set_index('step')
                    #define the tags
                    var_name_run = find_the_violence_type(variable)
                    var_run_savefile = give_me_violence_string_label_only(variable)

                    #define the scale
                    dict_run = line_dictionary_cm
                    y_label = list(dict_run.keys())
                    y_value = list(dict_run.values())

                    #define the scale for x acis, and before and after the range of interest

                    time_line_values = np.array(range(1, end_step+1, 1))
                    time_line_names = [vid2date(i+EndOfHistory) for i in time_line_values]

                    savefile = f'{ContinuousLineGraph}LineGraph_continuous_cm{var_run_savefile}_{dev_id}_r{EndOfHistory}_region_{region}_top{top_country}_step1to{end_step}_{variable}.png'

                    fig, ax = plt.subplots(figsize = line_fig_size)
                    for i in list(data_run.groupby('country_id').groups.keys()):
                        cdata= data_run.groupby('country_id').get_group(i)
                        main = cdata[variable].plot(label=Country(i).name)

                    plt.xticks(time_line_values, time_line_names, size = line_x_size, rotation = line_x_rotation)  
                    plt.yticks(y_value, y_label, size = line_y_size, rotation = line_y_rotation)
                    plt.legend(title='Country', loc=line_location, bbox_to_anchor=line_bbox_to_anchor, fontsize = line_legend_fontsize)

                    plt.title(f'{line_title_cm} of top {top_country} countries {region_human_name(region)} for steps 1 through {end_step}, {var_name_run}', fontsize = line_title_fontsize, pad = 20)
                    plt.xlabel("Month", fontsize = line_x_y_labels_fontsize)
                    plt.ylabel(f"{line_title_cm}, {var_name_run}", fontsize = line_x_y_labels_fontsize)

                    logo = fig.add_axes([SAR_logo_x, SAR_logo_y,SAR_logo_h_w, SAR_logo_h_w], anchor='NE', zorder=-1)
                    logo.imshow(SAR_logo)
                    logo.axis('off')

                    props = dict(boxstyle = 'round', facecolor  = 'white', alpha = 0.5)
                    textbox = f"https://viewsforecasting.org,\nmodel: {dev_id}_{model_wanted}_{model_attempt},region {region},\n{variable},last input: {str(vid2date(EndOfHistory))}"

                    plt.text(x = line_textbox_position_x, y = line_textbox_position_y, s = textbox, bbox = props, fontsize = line_textbox_fontsize, transform=plt.gcf().transFigure)

                    plt.savefig(savefile, dpi = line_bar_pie_charts_dpi, bbox_inches= 'tight')
                    plt.close()



    print(f'{user}, line for continuous predictions, cm level completed')
        
    
def predictions_cm_dich_line():
    #dichotomous linear graph 

    DichotomousLineGraph = master_folder + '/Dichotomous/Ensemble/LineGraphs/'

    data = predictions_dich_df.copy()
    steps_end_loop = cumulative_steps_line_charts
    how_many_countries = line_top
    variable_loop = variables_wanted_predictions_dich_line
    regions_loop = line_chart_region

    for region in regions_loop:
        for top_country in how_many_countries:
            for end_step in steps_end_loop:
                for variable in variable_loop:
                    country_name_and_regions_master = Queryset('Monthly_update_country_names_and_regions', 'country_month').fetch().reset_index().drop(columns = ['month_id']).drop_duplicates()

                    country_data = country_name_and_regions_master.copy()
                    line_charts_data = pd.merge(left = data.reset_index(), right = country_data, left_on = ('country_id'), right_on = ('country_id'), how = 'left').reset_index().set_index(['step', 'country_id'])

                    if region == 'globe':
                        temp = line_charts_data
                    elif region == 'ame':
                        temp = line_charts_data.query('in_africa == 1 or in_me == 1')
                    elif region == 'africa':
                        temp = line_charts_data.query('in_africa == 1')
                    elif region == 'me':
                        temp = line_charts_data.query('in_me == 1')
                    else: temp = line_charts_data.query(f'country_id in {region}')

                    country_list_run = give_me_topX_country_id_cumulative(df=temp, time_index = 'step', number_wanted = top_country, variable = variable, start = 1, end = end_step, variable_transformation = line_bar_pie_variable_transformation)

                    #subset the data
                    temporary_df = temp.iloc[temp.index.get_level_values('step') <= end_step]
                    data_run = temporary_df[temporary_df.index.get_level_values('country_id').isin(country_list_run)].reset_index().set_index('step')
                    #define the tags
                    var_name_run = find_the_violence_type(variable)
                    var_run_savefile = give_me_violence_string_label_only(variable)

                    #define the scale
                    dict_run = line_dictionary_cm_dich
                    y_label = list(dict_run.keys())
                    y_value = list(dict_run.values())

                    #define the scale for x acis, and before and after the range of interest

                    time_line_values = np.array(range(1, end_step+1, 1))
                    time_line_names = [vid2date(i+EndOfHistory) for i in time_line_values]

                    savefile = f'{DichotomousLineGraph}LineGraph_dichotomous_cm{var_run_savefile}_{dev_id}_r{EndOfHistory}_region_{region}_top{top_country}_step1to{end_step}_{variable}.png'

                    fig, ax = plt.subplots(figsize = line_fig_size)
                    for i in list(data_run.groupby('country_id').groups.keys()):
                        cdata= data_run.groupby('country_id').get_group(i)
                        cdata[variable].plot(label=Country(i).name)

                plt.xticks(time_line_values, time_line_names, size = line_x_size, rotation = line_x_rotation)  
                plt.yticks(y_value, y_label, size = line_y_size, rotation = line_y_rotation)
                plt.legend(title='Country', loc=line_location, bbox_to_anchor=line_bbox_to_anchor, fontsize = line_legend_fontsize)

                plt.title(f'{line_title_cm} of top {top_country} countries {region_human_name(region)} for steps 1 through {end_step}, {var_name_run}', fontsize = line_title_fontsize, pad = 20)
                plt.xlabel("Month", fontsize = line_x_y_labels_fontsize)
                plt.ylabel(f"{line_title_cm}, {var_name_run}", fontsize = line_x_y_labels_fontsize)

                logo = fig.add_axes([SAR_logo_x, SAR_logo_y,SAR_logo_h_w, SAR_logo_h_w], anchor='NE', zorder=-1)
                logo.imshow(SAR_logo)
                logo.axis('off')

                props = dict(boxstyle = 'round', facecolor  = 'white', alpha = 0.5)
                textbox = f"https://viewsforecasting.org,\nmodel: {dev_id}_{model_wanted}_{model_attempt},region {region},\n{variable},last input: {str(vid2date(EndOfHistory))}"

                plt.text(x = line_textbox_position_x, y = line_textbox_position_y, s = textbox, bbox = props, fontsize = line_textbox_fontsize, transform=plt.gcf().transFigure)

                plt.savefig(savefile, dpi = line_bar_pie_charts_dpi, bbox_inches= 'tight')

                plt.close()


    print(f'{user}, line for dichotomous predictions, cm level completed')
        
    
def predictions_cm_bar():
    #continuous, bar graph, cm
    ContinuousBarCharts = master_folder + '/Continuous/Ensemble/BarCharts/'

    data = predictions_df.copy()
    steps_end_loop = cumulative_steps_bar_charts
    variable_loop = variables_wanted_predictions_line_bar_pie
    regions_loop = bar_chart_region

    country_name_and_regions_master = Queryset('Monthly_update_country_names_and_regions', 'country_month').fetch().reset_index().drop(columns = ['month_id']).drop_duplicates()

    country_data = country_name_and_regions_master.copy()
    bar_charts_data = pd.merge(left = data.reset_index(), right = country_data, left_on = ('country_id'), right_on = ('country_id'), how = 'left').reset_index().set_index(['step', 'country_id'])

    for region in regions_loop:
        for end_step in steps_end_loop:
            for variable in variable_loop:
                #choosing a subset of data

                if region == 'globe':
                    temp = bar_charts_data
                elif region == 'ame':
                    temp = bar_charts_data.query('in_africa == 1 or in_me == 1')
                elif region == 'africa':
                    temp = bar_charts_data.query('in_africa == 1')
                elif region == 'me':
                    temp = bar_charts_data.query('in_me == 1')
                else: temp = bar_charts_data.query(f'country_id in {region}')

                temp2 = temp.iloc[temp.index.get_level_values('step')<=end_step]
                temp2['actual'] = np.exp(temp2[variable])-1
                temp3 = pd.DataFrame(temp2.groupby('country_id', dropna = False).agg({str('actual'):'sum'})).reset_index()
                data_run = pd.merge(left = temp3, right = country_data, left_on = 'country_id', right_on = 'country_id', how = 'left')

                var_name_run = find_the_violence_type(variable)
                var_run_savefile = give_me_violence_string_label_only(variable)

                savefile = f'{ContinuousBarCharts}BarCharts_continuous_cm{var_run_savefile}_{dev_id}_r{EndOfHistory}_region_{region}_step1to{end_step}_{variable}.png' 

                name = data_run['name']
                value = data_run['actual']

                fig, ax = plt.subplots(figsize = bar_fig_size)
                plt.barh(name, value, color = bar_chart_color)
                plt.title(f'{bar_chart_title} {region_human_name(region)} from step 1 to {end_step}, {var_name_run}', fontsize = bar_chart_title_font, pad = 20)
                plt.xlabel(f'{bar_chart_title}, {var_name_run}', fontsize = bar_chart_xlabel_font)
                plt.xticks(fontsize = bar_chart_xtick_font)
                plt.ylabel('Country', fontsize = bar_chart_ylabel_font)
                plt.yticks(fontsize = bar_chart_ytick_font)

                logo = fig.add_axes([bar_SAR_logo_x, bar_SAR_logo_y, bar_SAR_logo_h_w, bar_SAR_logo_h_w], anchor='NE', zorder=-1)
                logo.imshow(SAR_logo)
                logo.axis('off')

                props = dict(boxstyle = 'round', facecolor  = 'white', alpha = 0.5)
                textbox = f"https://viewsforecasting.org,\nmodel: {dev_id}_{model_wanted}_{model_attempt},region {region},\n{variable},last input: {str(vid2date(EndOfHistory))}"

                plt.text(x = bar_textbox_position_x, y = bar_textbox_position_y, s = textbox, bbox = props, fontsize = bar_textbox_fontsize, transform=plt.gcf().transFigure)

                plt.savefig(savefile, dpi = line_bar_pie_charts_dpi, bbox_inches= 'tight')
                plt.close()

    print(f'{user}, bar charts completed')

            
    
def predictions_cm_pie():
    #pie chart for the continous prediction
    ContinuousPieCharts = master_folder + '/Continuous/Ensemble/PieCharts/'

    data = predictions_df.copy()
    steps_end_loop = cumulative_steps_pie_charts
    variable_loop = variables_wanted_predictions_line_bar_pie
    regions_loop = pie_chart_region
    pie_greater_than_loop = pie_greater_than

    country_name_and_regions_master = Queryset('Monthly_update_country_names_and_regions', 'country_month').fetch().reset_index().drop(columns = ['month_id']).drop_duplicates()

    country_data = country_name_and_regions_master.copy()
    pie_charts_data = pd.merge(left = data.reset_index(), right = country_data, left_on = ('country_id'), right_on = ('country_id'), how = 'left').reset_index().set_index(['step', 'country_id'])

    for region in regions_loop:
        for end_step in steps_end_loop:
            for variable in variable_loop:
                for pie_cutoff in pie_greater_than_loop:
                #choosing a subset of data

                    if region == 'globe':
                        temp = pie_charts_data
                    elif region == 'ame':
                        temp = pie_charts_data.query('in_africa == 1 or in_me == 1')
                    elif region == 'africa':
                        temp = pie_charts_data.query('in_africa == 1')
                    elif region == 'me':
                        temp = pie_charts_data.query('in_me == 1')
                    else: temp = pie_charts_data.query(f'country_id in {region}')

                    temp2 = temp.iloc[temp.index.get_level_values('step')<=end_step]
                    temp2['actual'] = np.exp(temp2[variable])-1
                    temp3 = pd.DataFrame(temp2.groupby('country_id', dropna = False).agg({str('actual'):'sum'})).reset_index()
                    temp4 = pd.merge(left = temp3, right = country_data, left_on = 'country_id', right_on = 'country_id', how = 'left')
                    data_run = temp4.query(f'actual >= {pie_cutoff}')

                    var_name_run = find_the_violence_type(variable)
                    var_run_savefile = give_me_violence_string_label_only(variable)

                    savefile = f'{ContinuousPieCharts}PieCharts_continuous_cm{var_run_savefile}_{dev_id}_r{EndOfHistory}_region_{region}_step1to{end_step}_{variable}_cutoff{pie_cutoff}.png' 

                    data_run['legend'] = data_run['country_id'].astype(str)+'='+data_run['name']

                    pie_label = data_run['country_id']
                    pie_legend_label = data_run['legend']
                    value = data_run['actual']

                    fig,ax = plt.subplots(figsize = pie_fig_size)
                    pie = plt.pie(value, labels =pie_label, startangle = pie_chart_start_angle, textprops = {'fontsize':pie_chart_fontsize}, labeldistance = pie_chart_labeldistance)
                    plt.legend(pie[0], labels = pie_legend_label, title = pie_chart_legend_title, loc = pie_chart_legend_loc, bbox_to_anchor = pie_chart_bbox_to_anchor, fontsize = pie_chart_legend_fontsize)
                    plt.title(f'{pie_chart_title} from step 1 to {end_step}, {var_name_run}, cutoff {pie_cutoff} {region_human_name(region)}', fontsize = pie_chart_title_font)

                    logo = fig.add_axes([pie_SAR_logo_x, pie_SAR_logo_y, pie_SAR_logo_h_w, pie_SAR_logo_h_w], anchor='NE', zorder=-1)
                    logo.imshow(SAR_logo)
                    logo.axis('off')

                    props = dict(boxstyle = 'round', facecolor  = 'white', alpha = 0.5)
                    textbox = f"https://viewsforecasting.org,\nmodel: {dev_id}_{model_wanted}_{model_attempt},region {region},\ncutoff{pie_cutoff}, {variable},last input: {str(vid2date(EndOfHistory))}"

                    plt.text(x = pie_textbox_position_x, y = pie_textbox_position_y, s = textbox, bbox = props, fontsize = pie_textbox_fontsize, transform=plt.gcf().transFigure)

                    plt.savefig(savefile, dpi = line_bar_pie_charts_dpi, bbox_inches= 'tight')
                    plt.close()

    print(f'{user}, pie charts completed')