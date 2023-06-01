from main import *
from pathlib import Path

path = r'D:\Studium\GEO 411\Daten\geo411_gedi\Daten'
save_path = Path(r'{}'.format(path))

gedi_data = Path(r'GEDI_clipped.gpkg')
l2a_gpkg = Path(r'L2A.gpkg')
l2b_gpkg = Path(r'L2B.gpkg')

gedi_path = save_path / gedi_data
path_l2a = save_path / l2a_gpkg
path_l2b = save_path / l2b_gpkg

time_range = ['2019-04-28', '2022-04-29']

#load_gedi_gpkg(path_l2a, path_l2b, time_range, save_path)
#create_boxplots(gedi_path, save_path)
#plot_correlation_matrix(gedi_path, save_path)
#create_correlation_plots(gedi_path, save_path)
create_statistics(gedi_path, save_path)
