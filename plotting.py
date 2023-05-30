from main import *

save_path = 'C:/Users/herzu/Downloads'
gedi_path = 'C:/Users/herzu/Downloads/gedi_data/GEDI_clipped.gpkg'

create_boxplots(gedi_path, save_path)
plot_correlation_matrix(gedi_path, save_path)
create_correlation_plots(gedi_path, save_path)
