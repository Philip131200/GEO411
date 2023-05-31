from main import *
from pathlib import Path

path = r'D:\Studium\GEO 411\Daten\geo411_gedi\Daten'
gedi_data = Path(r'GEDI_clipped.gpkg')

save_path = Path(r'{}'.format(path))
#gedi_path = Path(r'{}\{}'.format(path, gedi_data))
gedi_path = save_path / gedi_data
l2a_gpkg = 'C:/Users/herzu/Downloads/L2A.gpkg'
l2b_gpkg = 'C:/Users/herzu/Downloads/L2B.gpkg'
time_range = ['2019-04-28', '2022-04-29']

save_path = Path(r'{}'.format(save_path))
gedi_path = Path(r'{}'.format(gedi_path))
path_l2a = Path(r'{}'.format(l2a_gpkg))
path_l2b = Path(r'{}'.format(l2b_gpkg))

#load_gedi_gpkg(path_l2a, path_l2b, time_range, save_path)
#create_boxplots(gedi_path, save_path)
#plot_correlation_matrix(gedi_path, save_path)
#create_correlation_plots(gedi_path, save_path)



""""

TODO
print(GEDI.describe)
GEDI.describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])
GEDI_table = GEDI.describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])
GEDI_table.to_csv('C:/Users/herzu/Downloads/GEDI_Deskriptive_Statistik.csv', float_format='%.5f')

"""
"""""
GEDI = gp.read_file(gedi_path)



import pandas as pd
from IPython.display import display
GEDI_table = GEDI.describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])
# Assuming you have the GEDI_table DataFrame
pd.set_option('display.max_columns', None)
display(GEDI_table)

"""""
