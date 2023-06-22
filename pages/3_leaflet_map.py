import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from pathlib import Path
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt

path = r'C:\Users\herzu\Documents\GEO411'
save_path = Path(r'{}'.format(path))

gedi_data = save_path / Path(r'GEDI_clipped.gpkg')
data = gpd.read_file(gedi_data)

# Create a dictionary of parameter color maps
parameter_color_maps = {
    'Total Canopy Cover': cm.get_cmap('Spectral'),
    'Relative Height bin98 (cm)': cm.get_cmap('Spectral'),
    'Total Plant Area Index': cm.get_cmap('Spectral'),
    'Foliage Height Diversity Index': cm.get_cmap('Spectral')
}

# Create a Folium map centered around the data points
map = folium.Map(location=[data['geometry'].centroid.y.mean(), data['geometry'].centroid.x.mean()], zoom_start=10)

# Add the Google satellite imagery tile layer
googleSat = folium.TileLayer(
    tiles='http://{s}.google.com/vt?lyrs=s&x={x}&y={y}&z={z}',
    attr='Google Satellite',
    name='Satellite Image',
    max_zoom=20,
    subdomains=['mt0', 'mt1', 'mt2', 'mt3']
).add_to(map)

# Streamlit App
st.title('Map Visualization')
st.subheader('Select Parameter to Display')

# Parameter selection box
parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                   'Foliage Height Diversity Index']
selected_parameter = st.selectbox('Parameter', parameter_names)

# Year selection box
years = ['All Years', 2019, 2020, 2021]
selected_year = st.selectbox('Select Year', years)

# Filter data by year
if selected_year == 'All Years':
    filtered_data = data
else:
    filtered_data = data[data['time'].dt.year == selected_year]

# Display selected parameter
if selected_parameter:
    st.subheader('Selected Parameter:')
    st.write(selected_parameter)
    parameter_data = filtered_data[selected_parameter].values

    # Normalize the data values for color mapping
    min_value = parameter_data.min()
    max_value = parameter_data.max()
    normalize = colors.Normalize(vmin=min_value, vmax=max_value)

    # Get the color map for the selected parameter
    parameter_color_map = parameter_color_maps[selected_parameter]

    # Iterate over the data points and add them to the map with respective colors and tooltip
    for index, row in filtered_data.iterrows():
        value = row[selected_parameter]
        color = colors.rgb2hex(parameter_color_map(normalize(value)))
        tooltip = f"{selected_parameter}: {value}, Time: {row['time'].strftime('%Y-%m-%d')}"
        folium.CircleMarker(
            location=(row['geometry'].y, row['geometry'].x),
            radius=5,
            fill=True,
            color=color,
            fill_color=color,
            tooltip=tooltip
        ).add_to(map)

    # Plot histogram
    st.subheader('Histogram')
    plt.hist(parameter_data, bins=10)  # Adjust the number of bins as needed
    plt.xlabel(selected_parameter)
    plt.ylabel('Frequency')
    st.pyplot(plt)

# Display the Folium map
st.subheader('Map')
folium_static(map)
