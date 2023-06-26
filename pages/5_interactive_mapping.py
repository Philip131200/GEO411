import streamlit as st
import plotly.graph_objects as go
import geopandas as gpd
from pathlib import Path

path = r'C:\Users\herzu\Documents\GEO411'
save_path = Path(r'{}'.format(path))

gedi_data_path = Path(r'GEDI_clipped.gpkg')
gedi_data = save_path / gedi_data_path
gedi_data = gpd.read_file(gedi_data)

# Streamlit app
st.title('Interactive 3D Plot of Vegetation Heights')

# Parameter selection
parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                   'Foliage Height Diversity Index']  # Add more parameter names if needed
selected_parameter = st.selectbox('Select a parameter:', parameter_names)

# Create 3D scatter plot
fig = go.Figure(data=[go.Scatter3d(
    x=gedi_data['geometry'].x,
    y=gedi_data['geometry'].y,
    z=gedi_data['Relative Height bin98 (cm)'],
    mode='markers',
    marker=dict(
        size=4,
        color=gedi_data[selected_parameter],
        colorscale='Viridis',
        opacity=0.8
    )
)])

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
