import folium
import random

def assign_colors(add_lst):
    """Color assignments for each library"""
    
    # the color list is limited in folium
    colors = ['red',
              'blue',
              'green',
              'purple',
              'orange',
              'darkred',
              'darkblue',
              'darkgreen',
              'cadetblue',
              'pink',
              'lightblue',
              'lightgreen',
              'gray',
              'black']
    
    new_dict = {}
    for address in add_lst:
        new_dict[address] = random.choice(colors)
    return new_dict



def adding_folium_layers(joined_df, boundaries, address, given_map):
    """Add the boundaries to the map using layers"""
    
    # filtering for a single library and pulling the assigned 
    # census tract geometries from boundaries GeoDataFrame
    cts = joined_df[joined_df.loc[:, 'address']==address]
    census_lst = cts.loc[:, 'namelsad10'].to_list()
    df = boundaries[boundaries.loc[:, 'namelsad10'].isin(census_lst)]

    # calling the color assigned for style function
    color = cts.loc[:, 'color_x'].iloc[0]
    
    def style_function(feature):
        return {
        'fillOpacity': 0,
        'color': color,
        'weight': 4}
    
    # creating layer for folium using style function
    l = folium.GeoJson(
        df[["geometry"]],
        name='Boundaries',
        style_function=style_function,
        control = False)
    
    # adding layer to map
    l.add_to(given_map)

    

def creating_foliumn_map(joined_df, boundaries):
    """Creating the Folium map to visualize 
       library and centract tract assignment"""
    
    # Initializing the folium map
    m = folium.Map(location=[joined_df.loc[:, 'lat'].mean(),
                             joined_df.loc[:, 'lon'].mean()],
                   zoom_start=10)
    
    # calling the color asssignment function and adding it to df
    color_assignments = assign_colors(joined_df.loc[:, 'address'].unique())
    joined_df.loc[:, 'color_x'] = joined_df.loc[:, 'address'].map(color_assignments)

    # unique address list to iterate through
    addresses = list(joined_df.loc[:, 'address'].unique())
    
    for address in addresses:
        # Add color assigned boundaries to the map using layers
        adding_folium_layers(joined_df, boundaries, address, m)


    # Add library locations and census centroids to the map
    for i, row in joined_df.iterrows():
        folium.Circle(location=[row['centroid'].y, row['centroid'].x],
                      radius=1, 
                      color=row['color_x'],
                      fill=True).add_to(m)
        try:
            folium.Marker(location=[row['lat'], row['lon']],
                          radius=1609,
                          color="blue",
                          fill=False,
                          tooltip=row['name']).add_to(m)
        except:
            continue


    # Add a layer control to the map to toggle the display of the boundaries
    folium.LayerControl().add_to(m)

    return m