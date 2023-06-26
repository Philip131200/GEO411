import streamlit as st
import plotly.graph_objects as go
import geopandas as gpd
from pathlib import Path

path = r'C:\Users\herzu\Documents\GEO411'
save_path = Path(r'{}'.format(path))

gedi_data_path = Path(r'GEDI_clipped.gpkg')
gedi_data = save_path / gedi_data_path
gedi_data = gpd.read_file(gedi_data)

# Define height ranges and titles for the violinplots
height_ranges = [
    ('All Classes', [0, 2100]),
    ('Shrub (< 250 cm)', [0, 250]),
    ('Brush (250 - 550 cm)', [250, 550]),
    ('Tree (> 550 cm)', [550, 2100])
]

# Get all classes
all_classes = [height_range[0] for height_range in height_ranges]

# Streamlit app
st.title('Interactive 3D Plot of Vegetation Heights')

# Parameter selection
parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                   'Foliage Height Diversity Index']  # Add more parameter names if needed
selected_parameter = st.selectbox('Select a parameter:', parameter_names)

# Height range selection
selected_height_range = st.selectbox('Select a height range:', all_classes)

# Get selected height range values
height_range_values = [height_range[1] for height_range in height_ranges if height_range[0] == selected_height_range][0]

# Filter data based on selected height range
if selected_height_range == 'All Classes':
    filtered_data = gedi_data
else:
    filtered_data = gedi_data[
        (gedi_data['Relative Height bin98 (cm)'] >= height_range_values[0]) &
        (gedi_data['Relative Height bin98 (cm)'] <= height_range_values[1])
    ]

# Create 3D scatter plot with class colors
fig = go.Figure()

# Add scatter trace for selected class
fig.add_trace(
    go.Scatter3d(
        x=filtered_data['geometry'].x,
        y=filtered_data['geometry'].y,
        z=filtered_data['Relative Height bin98 (cm)'],
        mode='markers',
        marker=dict(
            size=4,
            color=filtered_data[selected_parameter],
            colorscale='Viridis',
            opacity=0.8
        ),
        name=selected_height_range
    )
)

# Set plot layout
fig.update_layout(
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Relative Height (cm)'
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

# Show the plot using Streamlit
st.plotly_chart(fig, use_container_width=True)
