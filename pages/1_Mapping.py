import altair as alt
import pandas as pd
import geopandas as gp
import streamlit as st
import numpy as np
from pathlib import Path
import sys

st.set_page_config(layout="wide")

path = r'C:\Users\herzu\Documents\GEO411'
save_path = Path(r'{}'.format(path))

gedi_data = save_path / Path(r'GEDI_clipped.gpkg')
# read file as geopandas dataframe and delete geometry column
data = gp.read_file(gedi_data)
data['lon'] = data['geometry'].x
data['lat'] = data['geometry'].y
data.drop(columns='geometry', inplace=True)  # delete geometry column for streamlit

Karte = alt.Chart(data).mark_circle().encode(
    longitude='lon:Q',
    latitude='lat:Q',
    size=alt.value(10),
    tooltip=['Relative Height bin98 (cm)', 'time:T'],
).project(
    "mercator"
).properties(
    width=500,
    height=400
)

st.map(data)
st.write(Karte)
# st.write(data)
