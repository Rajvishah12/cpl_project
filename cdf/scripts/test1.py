import geopandas as gpd

import os

current_directory = os.getcwd()
print(current_directory)

# from ..utils.utils import get_lib_gdf, get_ct_gdf
from ..utils.plotting import creating_foliumn_map
# from acs_agg import acs_cleaning, acs_join


# class assignment_centroid_euclideandists:
#     """
#     Extracts data from the US Census Data for a specified geographic location and state.
#     The default is at the census tract level and for the state of Illinois.
#     """

#     def __init__(self, lib_file_path, ct_file_path):
#         """
#         Initializes a new instance of the assignment class.

#         Inputs:
#             - boundary_df: An integer with the year the data want to be
#               consulted
#         """

#         self.libs = get_lib_gdf(lib_file_path)
#         self.cts = get_ct_gdf(ct_file_path)

#     def assignment_dataframes(self, meters):
#         """
#         This function assigns census tracts to each library based on shortest euclidean distance

#         Inputs: 
#             - boundry_df: geodataframe of census tract boundary
#             - library_df: geodataframe of library location
#             - meters: meters for the library buffer zone 

#         Return: 
#             - intersect_area_dist: joined dataframe of each census tract with assigned home library
#         """

#         # create buffer geometry around library and convert mile into meters (~1609 meters)
#         library_df = self.libs
#         boundary_df = self.cts
        
#         library_df.loc[:, 'bufferzone'] = library_df['geometry'].buffer(meters)
#         library_df.set_geometry('bufferzone', inplace=True)
        
#         # census tract boundaries calculating centroids
#         boundary_df.loc[:, 'centroid'] = boundary_df.geometry.centroid
        
#         # create intersection dataframe of census tracts within x mile radius
#         interesect_df = gpd.overlay(boundary_df, library_df, how='intersection', keep_geom_type=False)
        
#         # calculate distance
#         interesect_df.loc[:, 'lib_geometry'] = gpd.points_from_xy(interesect_df.loc[:, 'lon'],\
#                                                                 interesect_df.loc[:, 'lat'], crs="EPSG:4326")
            
#         interesect_df.loc[:, 'distance'] = interesect_df.loc[:, 'lib_geometry'].distance(interesect_df.loc[:, 'centroid'])
        
#         interesect_df = interesect_df.to_crs("EPSG:3857")
        
#         # assign the lib with min distance for each unique census tract
#         intersect_area_dist = interesect_df.groupby('namelsad10', as_index=False).agg({'distance':'min'})
#         intersect_area_dist = intersect_area_dist.merge(interesect_df, how = 'left', on=['namelsad10','distance'])

#         return intersect_area_dist

#     def assignment_plot(self): 
#         """
#         This function returns output according 
#         """

#         # Create library and census tract geodataframe


#         # Assign census tracts overlapping with lib 1 mile bufferzone
#         joined_df = self.assignment_dataframes(1609)

#         # Creating map ploting assigned census tracts and library
#         m = creating_foliumn_map(joined_df, self.cts)

#         return m
        
#     def assignment_agg(self, acs_filepath): 

#         # Aggregate census data based on the assignment
#         acs_data = acs_cleaning(acs_filepath)
#         joined_df = self.assignment_dataframes(1609)

#         agg_df = acs_join(acs_data, joined_df)

#         return agg_df
    


# # Define the parameter to call on the API

# # lib_file_path = "../data/library_locations.csv"
# lib_file_path = "/Users/qingyi/Documents/uchicago/job/community_data_fellow/cpl/cpl_project/cdf/data/library_locations.csv"

# # ct_file_path = "../data/census_tract_boundaries.geojson"
# ct_file_path = "/Users/qingyi/Documents/uchicago/job/community_data_fellow/cpl/cpl_project/cdf/data/census_tract_boundaries.geojson"

# acs_filepath = 'https://raw.githubusercontent.com/ssegovba/cpl_project/main/data_bases/census_cook_county_dta.csv'

# assignment = assignment_centroid_euclideandists(lib_file_path, ct_file_path)

# m = assignment.assignment_plot()
# # m.save("../output/test1.html")

# agg_df = assignment.assignment_agg(acs_filepath)
# # agg_df.to_csv('../output/test1.csv',index=False)
# agg_df.to_csv('/Users/qingyi/Documents/uchicago/job/community_data_fellow/cpl/cpl_project/cdf/output/test.csv',index=False)
