import geopandas as gp
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def load_gedi_gpkg(path_l2a, path_l2b, time_range, save_path):

    gedi_data_l2a = gp.read_file(path_l2a)
    gedi_data_l2a = gedi_data_l2a.loc[:, ['Relative Height bin98 (cm)', 'geometry']]
    gedi_data_l2b = gp.read_file(path_l2b)

    gedi_data = gedi_data_l2b.merge(gedi_data_l2a, how='inner', on='geometry')
    gedi_data['time'] = pd.to_datetime(gedi_data['Acquisition Time'])
    gedi_data = gedi_data.set_index('time')
    if time_range is not None:
        assert len(time_range) == 2, 'time_range must be a list of two elements'
        gedi_data = gedi_data.sort_index().loc[f'{time_range[0]}':f'{time_range[1]}']

    gedi_data.to_file(save_path / 'GEDI_clipped.gpkg', driver='GPKG')
    print('finished load_gedi_gpkg')
    return gedi_data


def create_boxplots(gedi, save_filepath):
    parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                       'Foliage Height Diversity Index']
    gedi_data = gp.read_file(gedi)

    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 8))

    # Schleife über die Variablennamen und Erstellen der Boxplots
    for i, variable_name in enumerate(parameter_names):
        row = i // 2
        col = i % 2
        ax = axs[row, col]
        data = gedi_data[variable_name].dropna().values
        ax.boxplot(data)
        # Manuelle Änderung der Überschrift
        if variable_name == 'Total Canopy Cover':
            ax.set_title('Total Canopy Cover')
        elif variable_name == 'Relative Height bin98 (cm)':
            ax.set_title('Relative Height bin98 (cm)')
        elif variable_name == 'Total Plant Area Index':
            ax.set_title('Total Plant Area Index')
        elif variable_name == 'Foliage Height Diversity Index':
            ax.set_title('Foliage Height Diversity Index')

    # Save the figure
    plt.savefig(save_filepath / 'boxplot.png')
    print('finished create_boxplots')
    # Show the plot
    plt.show()


def plot_correlation_matrix(gedi, save_filepath):
    parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                       'Foliage Height Diversity Index']
    gedi_data = gp.read_file(gedi)
    # Create a DataFrame from the GeoDataFrame
    df = gedi_data[parameter_names].dropna()

    # Calculate the correlation matrix
    corr_matrix = df.corr()
    # Set up the figure and axes
    fig, ax = plt.subplots(figsize=(10, 8))
    # Plot the correlation matrix using seaborn
    sns.heatmap(corr_matrix, cmap='coolwarm', annot=True, fmt=".2f", cbar=True, square=True, ax=ax)
    # Set the x-axis tick labels
    ax.set_xticklabels(parameter_names, rotation=45, ha='right')
    # Set the y-axis tick labels
    ax.set_yticklabels(parameter_names, rotation=0)
    # Set the title
    ax.set_title("Correlation Matrix")

    # Save the plot
    plt.tight_layout()
    plt.savefig(save_filepath / 'correlationmatrix.png')
    print('finished plot_correlation_matrix')
    # Show the plot
    plt.show()


def create_correlation_plots(gedi, save_filepath):
    parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                       'Foliage Height Diversity Index']
    # Read the GEDI geopackage into a GeoDataFrame
    gedi_data = gp.read_file(gedi)

    # Create PairGrid object
    g = sns.PairGrid(gedi_data[parameter_names], diag_sharey=False)
    g.map_upper(plt.scatter, alpha=0.5, s=5)
    g.map_lower(sns.kdeplot, cmap='viridis', fill=True)
    g.map_diag(sns.histplot, kde=True)

    # Loop over variable names and add regression lines and R^2 texts
    for i, var1 in enumerate(parameter_names):
        for j, var2 in enumerate(parameter_names):
            if i != j:
                x = gedi_data[var1]
                y = gedi_data[var2]
                ax = g.axes[j, i]
                scatter = ax.scatter(x, y, c='#430154', alpha=0.9, s=5)
                sns.kdeplot(data=gedi_data, x=var1, y=var2, cmap='viridis', fill=True, ax=ax)
                if var2 == 'Foliage_height':
                    ax.figure.colorbar(scatter, ax=ax)
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                textstr = f'R² = {r_value**2:.2f}'
                ax.annotate(textstr, xy=(0.1, 0.9), xycoords='axes fraction', ha='left', fontsize=8)
                ax.plot(x, slope*x + intercept, color='r', linewidth=0.5)

    # Adjust plot titles
    for i, label in enumerate(parameter_names):
        g.axes[i, 0].set_ylabel(label)
        g.axes[-1, i].set_xlabel(label)

        plt.savefig(save_filepath / 'correlationplot.png')
    # Show the plot
    print('finished create_correlation_plots')
    plt.show()


def create_statistics(gedi, save_filepath):
    parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                       'Foliage Height Diversity Index']
    gedi_data = gp.read_file(gedi)
    gedi_table = gedi_data[parameter_names].describe(percentiles=[.02, .25, .5, .75, .98])
    print('finished create_statistics')
    gedi_table.to_csv(save_filepath / 'GEDI_Deskriptive_Statistik.csv', float_format='%.5f', sep=';', decimal=',')


def create_violinplot(gedi, save_filepath):
    gedi_data = gp.read_file(gedi)
    height_ranges = [
        ('Shrub (< 250 cm)', [0, 250]),
        ('Brush (250 - 550 cm)', [250, 550]),
        ('Tree (> 550 cm)', [550, float('inf')])
    ]

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(16, 6))

    for i, (title, height_range) in enumerate(height_ranges):
        filtered_data = gedi_data[(gedi_data['Relative Height bin98 (cm)'] >= height_range[0]) &
                                  (gedi_data['Relative Height bin98 (cm)'] < height_range[1])]
        ax = axes[i]
        sns.violinplot(data=filtered_data, y='Relative Height bin98 (cm)', inner='quartile', ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Relative Height bin98 (cm)')
        ax.set_ylabel('')

        data_percent = len(filtered_data) / len(gedi_data) * 100
        ax.text(0.95, 0.95, f'Data Percentage: {data_percent:.2f}%', transform=ax.transAxes, ha='right', va='top',
                fontsize=8, fontweight='bold')

    fig.suptitle('Violinplots For Different Vegetation Classes')
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    plt.tight_layout()
    plt.savefig(save_filepath / 'violinplot.png')
    plt.show()
