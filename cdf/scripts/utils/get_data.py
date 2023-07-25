import pandas as pd
import geopandas as gpd

def get_lib_gdf(lib_file_path): 
    """
    This function cleans up library dataframe, and transfer it to geodataframe

    Input: 
        - lib_file_path: file path with library dataset

    Return: 
        - libs_gdf: cleaned library geodataframe
    """
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
    """
    This function transfer census tract boundary to geodataframe

    Input: 
        - ct_file_path: file path for census tract boundary

    Return: 
        - ct_gdf: census tract geodataframe
    """

    ct_gdf = gpd.read_file(ct_file_path)
    return ct_gdf