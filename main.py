import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

GEDI = 'C:/Users/herzu/Downloads/GEDI_clipped.gpkg'
GEDI = gp.read_file(GEDI)



variable_name = 'Canopy_cover'

print(GEDI.describe)
GEDI.describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])
GEDI_table = GEDI.describe(percentiles=[.1, 2, 3, 4, 5, 6, 7, 8, 9])
GEDI_table.to_csv('C:/Users/herzu/Downloads/GEDI_Deskriptive_Statistik.csv', float_format='%.5f')


# Laden der Geopackage-Datei und Extrahieren der Spalten
variable_names = ['Canopy_cover', 'Height_98', 'Plant_area', 'Foliage_height']

# Erstellen des Rasters mit vier Boxplots
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

# Schleife über die Variablennamen und Erstellen der Boxplots
for i, variable_name in enumerate(variable_names):
    row = i // 2
    col = i % 2
    ax = axs[row, col]
    data = GEDI[variable_name].dropna().values
    ax.boxplot(data)
    # Manuelle Änderung der Überschrift
    if variable_name == 'Canopy_cover':
        ax.set_title('Total Canopy Cover')
    elif variable_name == 'Height_98':
        ax.set_title('Relative Height bin98 (cm)')
    elif variable_name == 'Plant_area':
        ax.set_title('Total Plant Area Index')
    elif variable_name == 'Foliage_height':
        ax.set_title('Foliage Height Diversity Index')

# Anzeigen des Diagramms
plt.show()


import geopandas as gpd
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the geopackage and extract the columns
variable_names = ['Canopy_cover', 'Height_98', 'Plant_area', 'Foliage_height']
variable_labels = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index', 'Foliage Height Diversity Index']

# Create a DataFrame from the GeoDataFrame
df = GEDI[variable_names].dropna()

# Calculate the correlation matrix
corr_matrix = df.corr()

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(10, 8))

# Plot the correlation matrix using seaborn
sns.heatmap(corr_matrix, cmap='coolwarm', annot=True, fmt=".2f", cbar=True, square=True, ax=ax)

# Set the x-axis tick labels
ax.set_xticklabels(variable_labels, rotation=45, ha='right')

# Set the y-axis tick labels
ax.set_yticklabels(variable_labels, rotation=0)

# Set the title
ax.set_title("Correlation Matrix")

# Show the plot
plt.show()

import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Laden der Geopackage-Datei und Extrahieren der Spalten
variable_names = ['Canopy_cover', 'Height_98', 'Plant_area', 'Foliage_height']
variable_labels = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index', 'Foliage Height Diversity Index']

# Erstellen des Raster-Korrelationsplots
g = sns.pairplot(GEDI[variable_names].dropna(), kind='scatter', diag_kind='kde', plot_kws={'s': 5})

# Schleife über die Variablennamen und Hinzufügen der Regressionsgeraden und R^2-Texte
for i, var1 in enumerate(variable_names):
    for j, var2 in enumerate(variable_names):
        if i != j:
            x = GEDI[var1]
            y = GEDI[var2]
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            textstr = f'R² = {r_value**2:.2f}'
            g.axes[j, i].annotate(textstr, xy=(0.1, 0.9), xycoords='axes fraction', ha='left', fontsize=8)
            g.axes[j, i].plot(x, slope*x + intercept, color='r', linewidth=0.5)

# Schleife über die Variablennamen und Hinzufügen der Punktdichte
for i, var1 in enumerate(variable_names):
    for j, var2 in enumerate(variable_names):
        if i != j:
            x = GEDI[var1]
            y = GEDI[var2]
            ax = g.axes[j, i]
            scatter = ax.scatter(x, y, c='#430154', alpha=0.9, s=5)
            sns.kdeplot(data=GEDI, x=var1, y=var2, cmap='viridis', fill=True, ax=ax)
        if j == 'Foliage Height Diversity Index':
            ax.figure.colorbar(scatter, ax=ax)

# Anpassen der Überschriften der Plots
for i, label in enumerate(variable_labels):
    g.axes[i, 0].set_ylabel(label)
    g.axes[-1, i].set_xlabel(label)

# Anzeigen des Diagramms
plt.show()
#g.savefig('GEDI_Parameter/Korrelation_v2.png')

