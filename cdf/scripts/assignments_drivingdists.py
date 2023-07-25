from utils.assignment_area_drivingdists import assignment_area_drivingdists

lib_file_path = "cdf/data/library_locations.csv"
ct_file_path = "cdf/data/census_tract_boundaries.geojson"
acs_filepath = 'cdf/data/census_cook_county_dta.csv'
api = "your_mapbox_token"

def assignment_output(lib_file_path, ct_file_path, acs_filepath, api): 
    """
    Assign census tracts to each library based on shortest driving distance. 
    
    Outputs: 
        - m: plotting for assignment saved to output folder
        - agg_df: aggregated dataframe based on assignment saved to output folder
    """

    assignment = assignment_area_drivingdists(lib_file_path, ct_file_path, api)

    m = assignment.assignment_plot()
    m.save("cdf/output/cpl_assignment_drivingdists.html")

    agg_df = assignment.assignment_agg(acs_filepath)
    agg_df.to_csv('cdf/output/cpl_agg_data_drivingdists.csv',index=False)

assignment_output(lib_file_path, ct_file_path, acs_filepath, api)