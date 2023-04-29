from Tools.visualization_assetts_fat002_add.config2 import *
from Tools.visualization_assetts_fat002_add.folder_creation import *
from Tools.visualization_assetts_fat002_add.features_cm import *

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

#adding the top10
gdf_ci_master = gdf_ci_master.reset_index()
gdf_ci_master['top10_sb'] = np.where(gdf_ci_master['country_id'].isin(top10_sb), 1,0)
gdf_ci_master['top10_ns'] = np.where(gdf_ci_master['country_id'].isin(top10_ns), 1,0)
gdf_ci_master['top10_os'] = np.where(gdf_ci_master['country_id'].isin(top10_os), 1,0)

print(f'{user}, pgm geometries fetching completed')

def features_pgm_maps():
    #data preparation
    data = features_pgm.copy()
    gdf = gdf_pid_master.copy()
    data_pid = pd.merge(left = data, right = gdf, left_index = True, right_index = True, how = 'left')
    gdf = gpd.GeoDataFrame(data_pid, geometry="geom")
    gdf_c = gdf_ci_master.copy()

    #savefolder
    features_pgm_folder = f"{master_folder}/"

    #looping informationa
    variable_loop = variables_wanted_features_pgm_ged
    dictionary_run = fatality_dictionary_pgm
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
                textbox = f'Name: features,\n{var_run}_at_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                savefile = f'{features_pgm_folder}GED_pgm_{var_run_savefile}_{region_name}_{cmap_run}_month{step}.png'

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
                plt.close()
    print(f'{user}, pgm maps for ged completed')
    
def features_pgm_maps_with_top10():
    #data preparation
    data = features_pgm.copy()
    gdf = gdf_pid_master.copy()
    data_pid = pd.merge(left = data, right = gdf, left_index = True, right_index = True, how = 'left')
    gdf = gpd.GeoDataFrame(data_pid, geometry="geom")
    gdf_c = gdf_ci_master.copy()

    #savefolder
    features_pgm_folder = f"{master_folder}/"

    #looping informationa
    variable_loop = variables_wanted_features_pgm_ged
    dictionary_run = fatality_dictionary_pgm
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
                textbox = f'Name: features,\n{var_run}_at_{str(step)},\nlast input: {str(vid2date(EndOfHistory))}'
                savefile = f'{features_pgm_folder}GED_pgm_{var_run_savefile}_{region_name}_{cmap_run}_month{step}_with_top10.png'

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
                
                gdf_part = gdf_c.loc[gdf_c[f"top10{var_run_savefile}"] > 0]
                masked_with_borders = gdf_c.plot(ax=ax,edgecolor='black',linewidth=2.0,facecolor='None')
                masked_with_top10 = gdf_part.plot(ax=ax,edgecolor='magenta',linewidth=3.0,facecolor='None')
                
                plt.savefig(savefile, dpi = pgm_dpi_global)
                plt.close()
    print(f'{user}, pgm maps for ged with top 10 completed')
    
    
    
