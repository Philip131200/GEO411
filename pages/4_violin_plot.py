import pandas as pd
import streamlit as st
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns

path = r'C:\Users\herzu\Documents\GEO411'
save_path = Path(r'{}'.format(path))

gedi_data_path = Path(r'GEDI_clipped.gpkg')
gedi_data = save_path / gedi_data_path
gedi_data = gpd.read_file(gedi_data)

# Convert 'Acquisition Time' column to datetime format
gedi_data['Acquisition Time'] = pd.to_datetime(gedi_data['Acquisition Time'])

# Extract month from 'Acquisition Time' column
gedi_data['Month'] = gedi_data['Acquisition Time'].dt.month

# Define the rain season and dry season months
rain_season_months = [1, 2, 3, 4, 5, 6]  # November to April
dry_season_months = [month for month in range(1, 13) if month not in rain_season_months]

# Filter data for rain season and dry season
rain_season_data = gedi_data[gedi_data['Month'].isin(rain_season_months)]
dry_season_data = gedi_data[gedi_data['Month'].isin(dry_season_months)]

# Define height ranges and titles for the violinplots
height_ranges = [
    ('Shrub (< 250 cm)', [0, 250]),
    ('Brush (250 - 550 cm)', [250, 550]),
    ('Tree (> 550 cm)', [550, 2100])
]

# Streamlit app
st.title('Violinplots for Different Vegetation Classes')

# Parameter selection
parameter_names = ['Total Canopy Cover', 'Relative Height bin98 (cm)', 'Total Plant Area Index',
                   'Foliage Height Diversity Index']  # Add more parameter names if needed
selected_parameter = st.selectbox('Select a parameter:', parameter_names)

# Create subplots for rain season and dry season
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(16, 12))

# Set y-axis ranges for each class with buffer
y_ranges = {}

# Calculate y-axis ranges for Shrub class with buffer
shrub_data = gedi_data[
    (gedi_data['Relative Height bin98 (cm)'] >= height_ranges[0][1][0]) &
    (gedi_data['Relative Height bin98 (cm)'] <= height_ranges[0][1][1])
]
y_ranges['Shrub'] = [shrub_data[selected_parameter].min() * 0.95, shrub_data[selected_parameter].max() * 1.05]

# Calculate y-axis ranges for Brush class with buffer
brush_data = gedi_data[
    (gedi_data['Relative Height bin98 (cm)'] >= height_ranges[1][1][0]) &
    (gedi_data['Relative Height bin98 (cm)'] <= height_ranges[1][1][1])
]
y_ranges['Brush'] = [brush_data[selected_parameter].min() * 0.95, brush_data[selected_parameter].max() * 1.05]

# Calculate y-axis ranges for Tree class with buffer
tree_data = gedi_data[
    (gedi_data['Relative Height bin98 (cm)'] >= height_ranges[2][1][0]) &
    (gedi_data['Relative Height bin98 (cm)'] <= height_ranges[2][1][1])
]
y_ranges['Tree'] = [tree_data[selected_parameter].min() * 0.95, tree_data[selected_parameter].max() * 1.05]

# Plot violinplots for rain season
for i, (title, height_range) in enumerate(height_ranges):
    filtered_rain_season_data = rain_season_data[
        (rain_season_data['Relative Height bin98 (cm)'] >= height_range[0]) &
        (rain_season_data['Relative Height bin98 (cm)'] <= height_range[1])
    ]
    ax_rain_season = axes[0, i]
    sns.violinplot(data=filtered_rain_season_data, y=selected_parameter, inner='quartile', ax=ax_rain_season,
                   cut=0, scale='width', color='lightgreen', alpha=0.5)
    ax_rain_season.set_title(title)
    ax_rain_season.set_ylabel(selected_parameter, fontsize=10)
    ax_rain_season.set_ylim(y_ranges[title.split()[0]])

    # Calculate and display data percentage
    data_percentage = len(filtered_rain_season_data) / len(gedi_data) * 100
    ax_rain_season.text(0.5, -0.05, f"Data Percentage: {data_percentage:.2f}%", transform=ax_rain_season.transAxes,
                        ha='center', fontweight='bold')

    # Plot violinplots for dry season
    filtered_dry_season_data = dry_season_data[
        (dry_season_data['Relative Height bin98 (cm)'] >= height_range[0]) &
        (dry_season_data['Relative Height bin98 (cm)'] <= height_range[1])
    ]
    ax_dry_season = axes[1, i]
    sns.violinplot(data=filtered_dry_season_data, y=selected_parameter, inner='quartile', ax=ax_dry_season,
                   cut=0, scale='width', color='indianred', alpha=0.5)
    ax_dry_season.set_ylabel(selected_parameter, fontsize=10)
    ax_dry_season.set_ylim(y_ranges[title.split()[0]])

    # Calculate and display data percentage
    data_percentage = len(filtered_dry_season_data) / len(gedi_data) * 100
    ax_dry_season.text(0.5, -0.05, f"Data Percentage: {data_percentage:.2f}%", transform=ax_dry_season.transAxes,
                       ha='center', fontweight='bold')

# Add a legend
legend_labels = ['Rain Season', 'Dry Season']
legend_handles = [
    plt.Rectangle((0, 0), 1, 1, fc='lightgreen', alpha=0.3),
    plt.Rectangle((0, 0), 1, 1, fc='indianred', alpha=0.3)
]
fig.legend(legend_handles, legend_labels, loc='upper right', bbox_to_anchor=(0.99, 0.89), fontsize='medium')

# Adjust spacing between subplots
fig.tight_layout()

# Show the plot using Streamlit
st.pyplot(fig)
