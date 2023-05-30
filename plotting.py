from main import *

save_path = 'C:/Users/herzu/Downloads'
gedi_path = 'C:/Users/herzu/Downloads/gedi_data/GEDI_clipped.gpkg'

create_boxplots(gedi_path, save_path)
plot_correlation_matrix(gedi_path, save_path)
create_correlation_plots(gedi_path, save_path)


""""

TODO
print(GEDI.describe)
GEDI.describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])
GEDI_table = GEDI.describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])
GEDI_table.to_csv('C:/Users/herzu/Downloads/GEDI_Deskriptive_Statistik.csv', float_format='%.5f')

"""