from main import *
from pathlib import Path

# Öffnen der NetCDF-Datei
dataset = xr.open_dataset(r'D:\Studium\GEO 411\Daten\geo411_gedi\Daten\dataset.nc')

path = r'D:\Studium\GEO 411\Daten\geo411_gedi\Daten'
save_path = Path(r'{}'.format(path))
gedi_data = save_path / Path(r'GEDI_clipped.gpkg')
gedi_gdf = gp.read_file(gedi_data)

parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                   'Foliage Height Diversity Index']

eo_gedi_data = add_gedi_to_xr(dataset, gedi_gdf, parameter_names, ('-20', '20'))

print(eo_gedi_data)
