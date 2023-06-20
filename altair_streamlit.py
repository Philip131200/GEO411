import altair as alt
import pandas as pd
import geopandas as gp
import streamlit as st
import numpy as np
from pathlib import Path
import sys

st.set_page_config(layout="wide")

path = r'D:\Studium\GEO 411\Daten\geo411_gedi\Daten'
save_path = Path(r'{}'.format(path))

gedi_data = save_path / Path(r'GEDI_clipped.gpkg')

data = gp.read_file(gedi_data)
data_pandas = pd.DataFrame(data.drop(columns='geometry'))

brush = alt.selection_interval()

scatterplot = alt.Chart(data_pandas).mark_circle(size=60).encode(
    x=alt.X('time:T', timeUnit='yearmonthdate'),
    y='Relative Height bin98 (cm)',
    #color='Origin',
    tooltip=['Relative Height bin98 (cm)'],
    opacity=alt.condition(brush, alt.value(0.6), alt.value(0.1))
).add_params(
    brush
).properties(
    title='GEDI Data',
    width=800,
    height=500
)

line250 = alt.Chart(pd.DataFrame({'y': [250]})).mark_rule(color='red').encode(
    y='y',
    tooltip='y'
)

line550 = alt.Chart(pd.DataFrame({'y': [550]})).mark_rule(color='orange').encode(
    y='y',
    tooltip='y'
)

hist = alt.Chart(data_pandas).mark_bar().encode(
    y='count(Relative Height bin98 (cm)):Q',
    x=alt.X('Relative Height bin98 (cm):Q').bin(),
).transform_filter(
    brush
).properties(
    title='Histogram',
    width=350,
    height=500
)

st.write(scatterplot + line250 + line550 | hist)
#st.write(scatterplot | hist)
