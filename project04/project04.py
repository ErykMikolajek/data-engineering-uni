# %%
import json

with open('proj4_params.json', 'r') as f:
    params = json.load(f)

params

# %%
import geopandas as gpd
df = gpd.read_file('proj4_points.geojson')
df.to_crs('epsg:4326', inplace=True)
df.head()

# %%
lamps_counted = {}
gdf_meters = df.to_crs('epsg:2180')
for _, row in gdf_meters.iterrows():
    buffer = row['geometry'].buffer(100)
    lamps_counted[row['lamp_id']] = gdf_meters['geometry'].within(buffer).sum()


# %%
import pandas as pd
lamps_counted_df = pd.DataFrame.from_dict(lamps_counted, orient='index', columns=['count'])
lamps_counted_df.to_csv('proj4_ex01_counts.csv', index_label=params['id_column'])

# %%
lamps_coords = {}
for i, row in df.iterrows():
    lamps_coords[row['lamp_id']] = (row['geometry'].y, row['geometry'].x)
lamps_coords_df = pd.DataFrame.from_dict(lamps_coords, orient='index', columns=['lat', 'lon'])
lamps_coords_df.to_csv('proj4_ex01_coords.csv', index_label=params['id_column'])

# %%
import pyrosm
fp = pyrosm.get_data(params['city'])
osm = pyrosm.OSM(fp)
gdf_driving = osm.get_network(network_type="driving")
gdf_driving.to_crs('epsg:3857', inplace=True)

# %%
gdf_driving = gdf_driving[gdf_driving['highway'] == 'primary']
gdf_driving = gdf_driving[['id', 'name', 'geometry']]
gdf_driving.rename(columns={'id': 'osm_id'}, inplace=True)
gdf_driving

# %%
gdf_driving.to_file('proj4_ex02_primary_roads.geojson', driver='GeoJSON')

# %%
gdf_driving.to_crs('epsg:2178', inplace=True)
gdf_driving['buffer'] = gdf_driving['geometry'].buffer(50)
gdf_driving.dropna(inplace=True)
gdf_driving.head()

# %%
roads_lamps = {}

for _, row in gdf_driving.iterrows():
    if row['name'] in roads_lamps:
        roads_lamps[row['name']] += gdf_meters['geometry'].within(row['buffer']).sum()
    else:
        roads_lamps[row['name']] = gdf_meters['geometry'].within(row['buffer']).sum()


# %%
roads_lamps_df = pd.DataFrame.from_dict(roads_lamps, orient='index', columns=['point_count'])
roads_lamps_df.to_csv('proj4_ex03_streets_points.csv', index_label='name')

# %%
countries_gdf = gpd.read_file('proj4_countries.geojson')
countries_gdf.to_crs('epsg:3857', inplace=True)
countries_gdf.head()

# %%
import matplotlib.pyplot as plt

for _, row in countries_gdf.iterrows():
    fig1, ax1 = plt.subplots()
    if row['geometry'].geom_type == 'Polygon':
        x,y = row['geometry'].exterior.xy
        ax1.plot(x, y, color='blue')
    else:
        for polygon in row['geometry'].geoms:
            ax1.plot(*polygon.exterior.xy, color='blue')

# %%
import contextily as cx

for _, row in countries_gdf.iterrows():
    fig1, ax1 = plt.subplots()
    if row['geometry'].geom_type == 'Polygon':
        x,y = row['geometry'].exterior.xy
        ax1.plot(x, y)
        cx.add_basemap(ax1)
    else:
        for polygon in row['geometry'].geoms:
            ax1.plot(*polygon.exterior.xy)
        cx.add_basemap(ax1)
    plt.savefig(f'proj4_ex04_{row["name"].lower()}.png', bbox_inches='tight')

# %%
countries_gdf_copy = countries_gdf.copy()
countries_gdf_copy['geometry'] = countries_gdf['geometry'].boundary
countries_gdf_copy.head()

# %%
import pickle
with open('proj4_ex04_gdf.pkl', 'wb') as f:
    pickle.dump(countries_gdf_copy, f)


