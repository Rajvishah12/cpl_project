import requests
import numpy as np
import pandas as pd
import geopandas as gpd
from .get_data import get_lib_gdf, get_ct_gdf
from .plotting import creating_foliumn_map
from .acs_agg import acs_cleaning, acs_join

class assignment_area_drivingdists:
    """
    Assign home library to each census tract based on shortest driving distance
    """

    def __init__(self, lib_file_path, ct_file_path, MAPBOX_TOKEN):
        """
        Initializes a new instance of the assignment class.

        Inputs:
            - lib_file_path: file path for library location dataset
            - ct_file_path: file path for census tract boundary
            - MAPBOX_TOKEN: your mapbox token for calculating driving distance
        """

        calc_CRS = "EPSG:3857"
        self.libs = get_lib_gdf(lib_file_path).to_crs(calc_CRS)
        self.cts = get_ct_gdf(ct_file_path).to_crs(calc_CRS)
        self.api = MAPBOX_TOKEN

    def driving_dist(self, tract, library):
        """
        This function calculates driving distance from a library to a census block centroid

        Inputs:
            - tract: census tract centroid geometry
            - library: library geometry

        Return: 
            - dist: distance between the two input
        """
        try:
            slat = str(tract.y)
            slng = str(tract.x)
            elat = str(library.y)
            elng = str(library.x)

            # add driving distances
            ENDPOINT = "https://api.mapbox.com/directions/v5/mapbox/driving/"
            url = ENDPOINT + slng + "," + slat + ";" + elng + "," + elat + "?" + "access_token=" + self.api
            response = requests.get(url)
            results = response.json()
            dist = results['routes'][0]['distance']/1609.34
        except:
            dist = np.nan
        return dist

    def assignment(self, boundary_df, library_df, meters):
        """
        This function assign census tract based on major overlapping area with meters lib bufferzone

        Inputs:
            - boundary_df: census tract geodataframe
            - library_df: library geodataframe 
            - meters: chosen meters for library buffer zone

        Return: 
            - intersect_area_dist: joined dataframe for overlapping census tract and library
        """

        CRS = "EPSG:4326"
        calc_CRS = "EPSG:3857"

        # create buffer geometry around library and convert mile into meters
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
        
        interesect_df.loc[:, 'distance'] = interesect_df.apply(lambda row: self.driving_dist(row['lib_geometry'],\
                                                                                        row['centroid']), axis=1)
        interesect_df = interesect_df.to_crs(calc_CRS)
        # assign the lib with max overlapping area for each unique census tract
        intersect_area = interesect_df.groupby('namelsad10', as_index=False).agg({'area':'max'})
        intersect_area = intersect_area.merge(interesect_df, how = 'left', on=['namelsad10', 'area'])
        
        # assign the lib with min distance for each unique census tract
        intersect_area_dist = intersect_area.groupby('namelsad10', as_index=False).agg({'distance':'min'})
        intersect_area_dist = intersect_area_dist.merge(intersect_area, how = 'left', on=['namelsad10','distance'])

        return intersect_area_dist
    
    def assignment_dataframes(self): 
        """
        This function assign all census tract to each library

        Return: 
            - joined_df: joined dataframe for each census tract and library
        """
                
        libs = self.libs
        cts = self.cts

        mile1 = self.assignment(cts, libs, meters=1609)

        remaining = pd.merge(cts, mile1.loc[:, ['namelsad10', 'name']], on='namelsad10', how='left')
        remaining = remaining[remaining.isnull().any(axis=1)].reset_index()
        remaining = remaining[~remaining.loc[:, 'namelsad10'].isin(['Census Tract 9800','Census Tract 7706.02'])]
        remaining = remaining.drop(columns=['index', 'name', 'centroid'])

        mile5 = self.assignment(remaining, libs, meters=9654)

        joined_df = mile1.append(mile5, ignore_index=True)

        return joined_df


    def assignment_plot(self): 
        """
        This function returns plotting for the assignment 
        """
        
        # Assign census tracts overlapping with lib 1 mile bufferzone
        joined_df = self.assignment_dataframes()

        # Creating map ploting assigned census tracts and library
        m = creating_foliumn_map(joined_df, self.cts)

        return m

    def assignment_agg(self, acs_filepath): 
        """
        This function aggregates census information for each library based on the assignment
        """

        # Aggregate census data based on the assignment
        acs_data = acs_cleaning(acs_filepath)
        joined_df = self.assignment_dataframes()

        agg_df = acs_join(acs_data, joined_df)

        return agg_df

