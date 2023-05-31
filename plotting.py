from main import *
from pathlib import Path

save_path = 'C:/Users/herzu/Downloads'
gedi_path = 'C:/Users/herzu/Downloads/GEDI_clipped.gpkg'

save_path = Path(r'{}'.format(save_path))
gedi_path = Path(r'{}'.format(gedi_path))

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