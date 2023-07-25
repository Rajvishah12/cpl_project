
from utils.assignment_centroid_euclideandists import assignment_centroid_euclideandists

lib_file_path = "cdf/data/library_locations.csv"
ct_file_path = "cdf/data/census_tract_boundaries.geojson"
acs_filepath = 'cdf/data/census_cook_county_dta.csv'

def assignment_output(lib_file_path, ct_file_path, acs_filepath): 
    """
    Assign census tracts to each library based on shortest euclidean distance. 
    
    Outputs: 
        - m: plotting for assignment saved to output folder
        - agg_df: aggregated dataframe based on assignment saved to output folder
    """
    assignment = assignment_centroid_euclideandists(lib_file_path, ct_file_path)

    m = assignment.assignment_plot()
    m.save("cdf/output/cpl_assignment_euclideandists.html")

    agg_df = assignment.assignment_agg(acs_filepath)
    agg_df.to_csv('cdf/output/cpl_agg_data_euclideandists.csv',index=False)

assignment_output(lib_file_path, ct_file_path, acs_filepath)