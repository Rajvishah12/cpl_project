
from utils.assignment_centroid_euclideandists import assignment_centroid_euclideandists

lib_file_path = "../data/library_locations.csv"
ct_file_path = "../data/census_tract_boundaries.geojson"
acs_filepath = '../data/census_cook_county_dta.csv'

def assignment_output(lib_file_path, ct_file_path, acs_filepath): 
    assignment = assignment_centroid_euclideandists(lib_file_path, ct_file_path)

    m = assignment.assignment_plot()
    m.save("../output/cpl_assignment_euclideandists.html")

    agg_df = assignment.assignment_agg(acs_filepath)
    agg_df.to_csv('../output/cpl_agg_data_euclideandists.csv',index=False)

assignment_output(lib_file_path, ct_file_path, acs_filepath)