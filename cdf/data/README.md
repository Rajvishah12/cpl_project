# Data Sources
We used three main data sources for this project:

    1. Libraries location: csv file that has the geolocation of each of the 81 branches of Chicago Public Library (CPL) across the city. Provided by CPL.

    2. Census tract boundaries: geojson file that has the corresponding boundaries for each one of the 866 census tracts in the city of Chicago.

    3. American Community Survey (ACS): json file obtained from an API call (See **notebooks/acs_pull.py** ) to the Census Bureau with several demographic variables to define each census tract characteristics. Variables selected by CPL.


Files:

**census_cook_county_dta.csv** - census api call output from notebooks/acs_pull.py. Need API key to run

**census_tract_boundaries.geojson** - census tract boundaries retrieved from github

**library_locations** - csv provided to us from CPL partner with all the information for each library branch

**census_tract_data.csv** - output from notebooks/acs_pull.py and used for aggregations based on assignments




