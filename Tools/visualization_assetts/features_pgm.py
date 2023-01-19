from Tools.visualization_assetts.config2 import *
from Tools.visualization_assetts.folder_creation import *

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

def features_pgm_maps():
    