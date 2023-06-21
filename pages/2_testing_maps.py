import altair as alt
import pandas as pd
import geopandas as gp
import streamlit as st
import numpy as np
from pathlib import Path
import pydeck as pdk
import sys

st.set_page_config(layout="wide")

path = r'D:\Studium\GEO 411\Daten\geo411_gedi\Daten'
save_path = Path(r'{}'.format(path))

gedi_data = save_path / Path(r'GEDI_clipped.gpkg')
# read file as geopandas dataframe and delete geometry column
data = gp.read_file(gedi_data)
data['lon'] = data['geometry'].x
data['lat'] = data['geometry'].y
#data.drop(columns='geometry', inplace=True)  # delete geometry column for streamlit

data_pandas = pd.DataFrame(data.drop(columns='geometry'))

st.pydeck_chart(pdk.Deck(
    map_provider='google_maps',
    map_style='satellite',
    initial_view_state=pdk.ViewState(
        latitude=-25.193,
        longitude=31.526,
        zoom=11,
        pitch=35,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=data_pandas,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=2,
           elevation_range=[0, 2000],
           pickable=True,
           extruded=True,
        ),
    ],
))

parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                   'Foliage Height Diversity Index']
vegatation_class_names = ['Shrub', 'Brush', 'Trees']

parameter = st.selectbox('select Parameter', parameter_names)
vegetation_class = st.selectbox('select Vegetation class', vegatation_class_names)
