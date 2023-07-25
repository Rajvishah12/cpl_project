## Chicago Public Library (CPL)

This directory contains code that maps every census tract in the city of Chicago to each of the CPL's 81 branches. This helps to establish a definition of a "home" library to identify the expected user demographic based on proximity and community characteristics (such as population size and demographics) that each branch should serve.

The definition of a home library allows CPL to identify users who utilize their home branch and those who do not, in order to refine resources and programs offered at each branch based on user preferences and usage patterns.

### Installation

Software Setup

1. Install Docker. The project is designed to run in a Docker container. Therefore, the only prerequisite is Docker: [Get Docker](https://docs.docker.com/get-docker/)

2. Clone the repo
   ```sh
   git clone https://github.com/uchicago-dsi/cpl_project.git
   ```
3. Change to the root project directory:
   ```sh
   cd cdf
   ```
4. Build the Docker image from the root project directory:
    ```sh
   docker build -t cpl_image .
   ```
5. Run the Docker image:
   ```sh
   docker run --platform=linux/amd64 -e "REPOPATH=`readlink -f $1`" -e "LINT=$2" -v $REPOPATH:/container-repo-mount cpl_image
   ```

### Directory Structure

```sh
├── README.md
├── .gitignore
├── Dockerfile
├── requirements.txt
├── data/
│   ├── README.md
│   ├── census_cook_county_dta.csv
│   ├── census_tract_boundaries.geojson
│   ├── library_locations.csv
│   └── census_tract_data.csv
├── notebooks/
│   ├── README.md
│   ├── assignments_area_drivingdists.ipynb
│   ├── assignments_centroids_euclideandists.ipynb
│   └── acs_pull.py
├── output/
│   ├── README.md
│   ├── cpl_assignments.html
│   ├── cpl_agg_data.csv
│   ├── lib_tract.csv
│   ├── library_locations.csv
│   └── vars_dict_operations.xlsx
├── utils/
│   ├── README.md
│   ├── acs_agg.py
│   ├── plotting.py
│   └── utils.py
```