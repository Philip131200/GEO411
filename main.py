import geopandas as gp
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path


def create_boxplots(gedi, save_filepath):
    variable_names = ['Canopy_cover', 'Height_98', 'Plant_area', 'Foliage_height']
    gedi = gp.read_file(gedi)

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

    # Schleife über die Variablennamen und Erstellen der Boxplots
    for i, variable_name in enumerate(variable_names):
        row = i // 2
        col = i % 2
        ax = axs[row, col]
        data = gedi[variable_name].dropna().values
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

    # Save the figure
    plt.savefig(save_filepath / r'boxplot.png')

    # Show the plot
    plt.show()


def plot_correlation_matrix(gedi, save_filepath):
    variable_names = ['Canopy_cover', 'Height_98', 'Plant_area', 'Foliage_height']
    variable_labels = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                       'Foliage Height Diversity Index']
    gedi = gp.read_file(gedi)
    # Create a DataFrame from the GeoDataFrame
    df = gedi[variable_names].dropna()
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
    # Save the plot
    plt.tight_layout()
    plt.savefig(save_filepath / r'correlationamtrix.png')
    # Show the plot
    plt.show()


def create_correlation_plots(gedi, save_filepath):
    variable_names = ['Canopy_cover', 'Height_98', 'Plant_area', 'Foliage_height']
    variable_labels = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                       'Foliage Height Diversity Index']
    # Read the GEDI geopackage into a GeoDataFrame
    gedi = gp.read_file(gedi)

    # Create PairGrid object
    g = sns.PairGrid(gedi[variable_names], diag_sharey=False)
    g.map_upper(plt.scatter, alpha=0.5, s=5)
    g.map_lower(sns.kdeplot, cmap='viridis', fill=True)
    g.map_diag(sns.histplot, kde=True)

    # Loop over variable names and add regression lines and R^2 texts
    for i, var1 in enumerate(variable_names):
        for j, var2 in enumerate(variable_names):
            if i != j:
                x = gedi[var1]
                y = gedi[var2]
                ax = g.axes[j, i]
                scatter = ax.scatter(x, y, c='#430154', alpha=0.9, s=5)
                sns.kdeplot(data=gedi, x=var1, y=var2, cmap='viridis', fill=True, ax=ax)
                if var2 == 'Foliage_height':
                    ax.figure.colorbar(scatter, ax=ax)
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                textstr = f'R² = {r_value**2:.2f}'
                ax.annotate(textstr, xy=(0.1, 0.9), xycoords='axes fraction', ha='left', fontsize=8)
                ax.plot(x, slope*x + intercept, color='r', linewidth=0.5)

    # Adjust plot titles
    for i, label in enumerate(variable_labels):
        g.axes[i, 0].set_ylabel(label)
        g.axes[-1, i].set_xlabel(label)

        plt.savefig(save_filepath / r'correlationplot.png')
    # Show the plot
    plt.show()
