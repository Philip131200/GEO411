from main import *
from pathlib import Path
import streamlit as st

# Öffnen der NetCDF-Datei
dataset = xr.open_dataset(r'D:\Studium\GEO 411\Daten\geo411_gedi\Daten\dataset.nc')

path = r'D:\Studium\GEO 411\Daten\geo411_gedi\Daten'
save_path = Path(r'{}'.format(path))
gedi_data = save_path / Path(r'GEDI_clipped.gpkg')
gedi_gdf = gp.read_file(gedi_data)

parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                   'Foliage Height Diversity Index']

eo_gedi_data = add_gedi_to_xr(dataset, gedi_gdf, parameter_names, ('-20', '20'))

# Extrahieren der Variablen vv, vh, ndvi und GEDI-Parameter
vv = eo_gedi_data['vv']
vh = eo_gedi_data['vh']
ndvi = eo_gedi_data['ndvi']
total_canopy_cover = eo_gedi_data['Total Canopy Cover']
relative_height = eo_gedi_data['Relative Height bin98 (cm)']
total_plant_area_index = eo_gedi_data['Total Plant Area Index']
foliage_height_diversity_index = eo_gedi_data['Foliage Height Diversity Index']

# Parameter selection box
parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                   'Foliage Height Diversity Index']
selected_parameter = st.selectbox('Parameter', parameter_names)
selected_eo_gedi_data = eo_gedi_data['{}'.format(selected_parameter)]


st.write('streamlit: ', selected_eo_gedi_data)
print('prnt: ', selected_eo_gedi_data)
