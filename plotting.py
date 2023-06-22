from main import *
from pathlib import Path

path = r'C:\Users\herzu\Documents\GEO411'
save_path = Path(r'{}'.format(path))

gedi_data = Path(r'GEDI_clipped.gpkg')
#gedi_data = Path(r'GEDI_clipped_log.gpkg')
#l2a_gpkg = Path(r'L2A.gpkg')
#l2b_gpkg = Path(r'L2B.gpkg')

gedi_path = save_path / gedi_data
#path_l2a = save_path / l2a_gpkg
#path_l2b = save_path / l2b_gpkg

time_range = ['2019-04-28', '2022-04-29']

#load_gedi_gpkg(path_l2a, path_l2b, time_range, save_path)  # muss vor den anderen Funktionen ausgeführt werden

#create_boxplots(gedi_path, save_path)
#plot_correlation_matrix(gedi_path, save_path)
#create_correlation_plots(gedi_path, save_path)
#create_statistics(gedi_path, save_path)
#create_violinplot(gedi_path, save_path)
create_df_classes(gedi_path, save_path)
csv_names = ['Shrub.csv', 'Brush.csv', 'Tree.csv']

for vegetation_classes in csv_names:
    data_shrub = save_path / vegetation_classes
    create_violinplot_month(data_shrub, save_path)
