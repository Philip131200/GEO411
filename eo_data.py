import xarray as xr
import matplotlib.pyplot as plt
import datetime as datetime

plt.style.use('seaborn-v0_8-paper')

# Öffnen der NetCDF-Datei
dataset = xr.open_dataset(r'C:\Users\herzu\Documents\GEO411\dataset.nc')

# Extrahieren der Variablen vv, vh und ndvi
vv = dataset['vv']
vh = dataset['vh']
ndvi = dataset['ndvi']

# Berechnung des monatlichen Medians über x und y
monthly_median = dataset.groupby('time.month').median(dim=['x', 'y'])

fig, ax1 = plt.subplots(figsize=(16, 4))
ax1.set_xlim([datetime.datetime(2018, 12, 15), datetime.datetime(2022, 1, 15)])

# Erzeugen der ersten y-Achse für vv und vh
vv_median = vv.median(dim=['x', 'y'])
vh_median = vh.median(dim=['x', 'y'])
vv_median.sel(time=slice('2019-01-01', '2021-12-31')).plot.line('o-', label='VV (Monthly Median)',
                                                                ax=ax1, color='blue')
vh_median.sel(time=slice('2019-01-01', '2021-12-31')).plot.line('o-', label='VH (Monthly Median)',
                                                                ax=ax1, color='darkkhaki')
ax1.set_ylabel('VV / VH Backscatter', fontsize=12)
ax1.tick_params(axis='y', labelsize=11)
plt.xlabel('Time', fontsize=11)
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=0, ha='center', fontsize=11)

# Erzeugen der zweiten y-Achse für ndvi
ax2 = ax1.twinx()
# Berechnung des monatlichen Medians über x, y und separate Darstellung von ndvi
ndvi_monthly_median = ndvi.groupby('time.month').median(dim=['x', 'y'])
ndvi_monthly_median.sel(time=slice('2019-01-01', '2021-12-31')).plot.line('o-', label='NDVI (Monthly Median)',
                                                                          color='green', ax=ax2)
ax2.set_ylabel('NDVI', fontsize=11)
ax2.tick_params(axis='y', labelsize=11)

ax1.grid(True)
ax2.grid(True)

# Hinzufügen von Beschriftungen, Titel und Legende
# Legenden aus beiden Achsen kombinieren
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
ax1.legend(lines, labels, loc='upper right')

# Hintergrundfarben für die Monate festlegen
ax1.axvspan('2019-05-01', '2019-10-31', facecolor='indianred', alpha=0.3)
ax1.axvspan('2020-05-01', '2020-10-31', facecolor='indianred', alpha=0.3)
ax1.axvspan('2021-05-01', '2021-10-31', facecolor='indianred', alpha=0.3)
ax1.axvspan('2018-12-15', '2019-04-30', facecolor='lightgreen', alpha=0.3)
ax1.axvspan('2019-11-01', '2020-04-30', facecolor='lightgreen', alpha=0.3)
ax1.axvspan('2020-11-01', '2021-04-30', facecolor='lightgreen', alpha=0.3)
ax1.axvspan('2021-11-01', '2022-01-15', facecolor='lightgreen', alpha=0.3)

# Anzeigen des Plots
plt.show()
