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
data.drop(columns='geometry', inplace=True)  # delete geometry column for streamlit
data_pandas = pd.DataFrame(data.drop(columns='geometry'))

)
