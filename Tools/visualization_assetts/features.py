def cm_feature_maps():
    features_qs = (Queryset("Monthly_update_features_cm", "country_month"))
    features_cm=features_qs.fetch()

    #create new variables, note this part to be moved into queryset when new querysetting is ready
    features_cm['gdp_pc']=features_cm['wdi_ny_gdp_mktp_kd']/features_cm['wdi_sp_pop_totl']
    features_cm['gdp_pc_ln1']=np.log(features_cm['gdp_pc'])

    print(f'{user} cm_current_data fetched successfully, note to malika, gdp is currently coded to be derived, recode within queryset at queryset revision')
    
    #obtaining cm level geometries
    engine = sa.create_engine(source_db_path)
    gdf_ci_master = gpd.GeoDataFrame.from_postgis("SELECT id as country_id, name, in_africa, in_me, geom FROM prod.country", engine, geom_col='geom')
    gdf_ci_master = gdf_ci_master.to_crs(4326)
    print(f'{user} gdf_ci_master fetched successfully')
    
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
                textbox = f'Name: features,\n{var_run}_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
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

def cm_change_maps():
    features_qs = (Queryset("Monthly_update_features_cm", "country_month"))
    features_cm=features_qs.fetch()

    #create new variables, note this part to be moved into queryset when new querysetting is ready
    features_cm['gdp_pc']=features_cm['wdi_ny_gdp_mktp_kd']/features_cm['wdi_sp_pop_totl']
    features_cm['gdp_pc_ln1']=np.log(features_cm['gdp_pc'])

    print(f'{user} cm_current_data fetched successfully, note to malika, gdp is currently coded to be derived, recode within queryset at queryset revision')
    
    #obtaining cm level geometries
    engine = sa.create_engine(source_db_path)
    gdf_ci_master = gpd.GeoDataFrame.from_postgis("SELECT id as country_id, name, in_africa, in_me, geom FROM prod.country", engine, geom_col='geom')
    gdf_ci_master = gdf_ci_master.to_crs(4326)
    print(f'{user} gdf_ci_master fetched successfully')
    
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
                        textbox = f'Name: features,\n{var_run}_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
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

def pgm_feature_maps():
    #obtain data
    features_pgm_qs = (Queryset("Monthly_update_features_pgm", "priogrid_month")
    )

    features_pgm=features_pgm_qs.fetch()


    print(f'{user} pgm_current_data fetched successfully')
    
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
    
    #data preparation
    data = features_pgm.copy()
    gdf = gdf_pid_master.copy()
    data_pid = pd.merge(left = data, right = gdf, left_index = True, right_index = True, how = 'left')
    gdf = gpd.GeoDataFrame(data_pid, geometry="geom")
    gdf_c = gdf_ci_master.copy()

    #savefolder
    features_pgm_folder = master_folder+'/Features/Maps/pgm/'

    #looping informationa
    variable_loop = variables_wanted_features_pgm_ged
    dictionary_run = fatality_dictionary_pgm
    cmap_run = fatality_colormap
    steps_loop = months_wanted_features

    for step in steps_loop:
        for variable in variable_loop:
            for region_name in geo_coverage_loop_pgm:
                data_run = gdf.loc[step]
                var_run = variable
                var_name_run = find_the_violence_type(variable)
                var_run_savefile = give_me_violence_string_label_only(variable)
                bbox_run = bbox_from_cid_region(region_name)                       

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

                title_run = f'{features_ged_title_name} in {str(vid2date(step))}, {var_name_run}'
                textbox = f'Name: features,\n{var_run}_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                savefile = f'{features_pgm_folder}GED_pgm{var_run_savefile}_{region_name}_{cmap_run}_month{step}.png'

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
                masked_with_borders=gdf_c.plot(ax=ax,edgecolor='black',linewidth=2.0,facecolor='None')

                plt.savefig(savefile, dpi = pgm_dpi_global)
    print(f'{user}, pgm maps for ged completed')


def pgm_feature_change_maps():
    #obtain data
    features_pgm_qs = (Queryset("Monthly_update_features_pgm", "priogrid_month")
    )

    features_pgm=features_pgm_qs.fetch()


    print(f'{user} pgm_current_data fetched successfully')
    
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
    
    for delta in months_back_actual:
    for variable in variables_wanted_features_pgm_change_ged:
        column = variable
        actual = np.exp(features_pgm[column]) - 1
        shifted = np.exp(features_pgm[column].groupby(level = 1).shift(periods = delta)) - 1
        change_run_column = f'ln1_delta_{delta}_{column}'
        features_pgm[change_run_column] = np.sign(actual-shifted)*np.log(np.abs(actual-shifted)+1)
        
        data = features_pgm.copy()
        gdf = gdf_pid_master.copy()
        data_pid = pd.merge(left = data, right = gdf, left_index = True, right_index = True, how = 'left')
        gdf = gpd.GeoDataFrame(data_pid, geometry="geom")
        gdf_c = gdf_ci_master.copy()

        #savefolder
        features_change_pgm_folder = master_folder+'/Features/ChangeMaps/pgm/'
        
        #looping information
        variable_loop = {change_run_column}
        steps_loop = month_wanted_features_change_maps

        #custom dictionary for this run
        dictionary_run = change_dictionary_pgm
        cmap_run = change_colormap_global     

        for step in steps_loop:
            for variable in variable_loop:
                for region_name in geo_coverage_loop_pgm:
                    data_run = gdf.loc[step]
                    var_run = variable
                    var_name_run = find_the_violence_type(variable)
                    var_run_savefile = give_me_violence_string_label_only(variable)
                    bbox_run = bbox_from_cid_region(region_name)
                    
                    #making the choice of textbox size
                    textbox_font_size = function_for_textbox(region_name)

                    #making the choice of textbox size
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

                    title_run = f'{features_change_title_name} in {str(vid2date(step))}, {var_name_run}'
                    textbox = f'Name: features,\n{var_run}_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                    savefile = f'{features_change_pgm_folder}ChangeMaps_GED_pgm{var_run_savefile}_{region_name}_{cmap_run}_month{step}.png'

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
                    masked_with_borders=gdf_c.plot(ax=ax,edgecolor='black',linewidth=2.0,facecolor='None')

                    plt.savefig(savefile, dpi = pgm_dpi_global)
print(f'{user}, pgm  change maps for ged completed')
    