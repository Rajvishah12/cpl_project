import os
import pandas as pd
import geopandas as gpd
import requests
import numpy as np

def get_lib_gdf(lib_file_path): 
    libs = pd.read_csv(lib_file_path)
    libs.columns = map(str.lower, libs.columns)
    libs.columns = libs.columns.str.strip()
    libs.loc[:, 'location'] = libs.loc[:, 'location'].apply(lambda x: eval(x))
    libs.loc[:, 'lat'] = libs.loc[:, 'location'].apply(lambda x: x[0])
    libs.loc[:, 'lon'] = libs.loc[:, 'location'].apply(lambda x: x[1])
    lib_geometry = gpd.points_from_xy(libs['lon'], libs['lat'])
    libs_gdf = gpd.GeoDataFrame(libs, geometry=lib_geometry, crs="EPSG:4326")
    return libs_gdf

def get_ct_gdf(ct_file_path): 
    ct_gdf = gpd.read_file(ct_file_path)
    return ct_gdf

def assignment_dataframes1(boundary_df, library_df, meters):

    # create buffer geometry around library and convert mile into meters (~1609 meters)
    library_df.loc[:, 'bufferzone'] = library_df['geometry'].buffer(meters)
    library_df.set_geometry('bufferzone', inplace=True)
    
    # census tract boundaries calculating centroids
    boundary_df.loc[:, 'centroid'] = boundary_df.geometry.centroid
    
    # create intersection dataframe of census tracts within x mile radius
    interesect_df = gpd.overlay(boundary_df, library_df, how='intersection', keep_geom_type=False)
    
    # calculate distance
    interesect_df.loc[:, 'lib_geometry'] = gpd.points_from_xy(interesect_df.loc[:, 'lon'],\
                                                              interesect_df.loc[:, 'lat'], crs="EPSG:4326")
        
    interesect_df.loc[:, 'distance'] = interesect_df.loc[:, 'lib_geometry'].distance(interesect_df.loc[:, 'centroid'])
    
    interesect_df = interesect_df.to_crs("EPSG:3857")
    
    # assign the lib with min distance for each unique census tract
    intersect_area_dist = interesect_df.groupby('namelsad10', as_index=False).agg({'distance':'min'})
    intersect_area_dist = intersect_area_dist.merge(interesect_df, how = 'left', on=['namelsad10','distance'])

    return intersect_area_dist


def driving_dist(tract, library):
    try:
        slat = str(tract.y)
        slng = str(tract.x)
        elat = str(library.y)
        elng = str(library.x)

        # add driving distances
        ENDPOINT = "https://api.mapbox.com/directions/v5/mapbox/driving/"
        url = ENDPOINT + slng + "," + slat + ";" + elng + "," + elat + "?" + "access_token=" + MAPBOX_TOKEN
        response = requests.get(url)
        results = response.json()
        dist = results['routes'][0]['distance']/1609.34
    except:
        dist = np.nan
    return dist


def assignment_dataframes2(boundary_df, library_df, meters):

    # create buffer geometry around library and convert mile into meters (~1609 meters)
    
    library_df.loc[:, 'bufferzone'] = library_df['geometry'].buffer(meters)
    library_df.set_geometry('bufferzone', inplace=True)
    
    # census tract boundaries calculating centroids
    boundary_df.loc[:, 'centroid'] = boundary_df.geometry.centroid
    
    # create intersection dataframe of census tracts within x mile radius
    interesect_df = gpd.overlay(boundary_df, library_df, how='intersection', keep_geom_type=False)
        
    # calculate overlapping area
    interesect_df.loc[:, 'area'] = interesect_df['geometry'].area

    # calculate distance
    interesect_df.loc[:, 'lib_geometry'] = gpd.points_from_xy(interesect_df.loc[:, 'lon'],\
                                                              interesect_df.loc[:, 'lat'], crs=CRS) #.to_crs(calc_CRS)
    
    interesect_df.loc[:, 'centroid'] = interesect_df.loc[:, 'centroid'].to_crs(CRS)
    
#     interesect_df.loc[:, 'distance'] = interesect_df.loc[:, 'lib_geometry'].distance(interesect_df.loc[:, 'centroid'])
    interesect_df.loc[:, 'distance'] = interesect_df.apply(lambda row: driving_dist(row['lib_geometry'],\
                                                                                    row['centroid']), axis=1)
    interesect_df = interesect_df.to_crs(calc_CRS)
    # assign the lib with max overlapping area for each unique census tract
    intersect_area = interesect_df.groupby('namelsad10', as_index=False).agg({'area':'max'})
    intersect_area = intersect_area.merge(interesect_df, how = 'left', on=['namelsad10', 'area'])
    
    # assign the lib with min distance for each unique census tract
    intersect_area_dist = intersect_area.groupby('namelsad10', as_index=False).agg({'distance':'min'})
    intersect_area_dist = intersect_area_dist.merge(intersect_area, how = 'left', on=['namelsad10','distance'])

    return intersect_area_dist


def acs_cleaning(acs_filepath): 
    acs_data = pd.read_csv(acs_filepath)
    acs_data = acs_data.loc[acs_data.loc[:,'county'] == 31,] 
    acs_data.loc[:,'geoid10'] = acs_data.loc[:,'geo_id'].str.split('1400000US',expand=True).loc[:,1]
    acs_data.loc[:,'geoid10'] = acs_data.loc[:,'geoid10'].astype('int')
    invalid_values = [-666666666, -999999999]
    non_changeable_cols = ["tract", "county", "geo_id", "census_name", "state", "geoid10"]
    cols_mod = [ col for col in acs_data.columns if col not in non_changeable_cols]
    acs_data.loc[:, cols_mod] = acs_data.loc[:, cols_mod].replace(invalid_values, np.nan)

    joined_df.loc[:,'geoid10'] = joined_df.loc[:,'geoid10'].astype('int')
