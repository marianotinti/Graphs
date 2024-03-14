#Load all necessary libraries and functions to perform data exploring and data visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
import seaborn as sns

from scipy.interpolate import interp1d
from scipy.interpolate import make_interp_spline
import os
import sys
import re


# Load variable 'df' from URI: c:\Users\Mariano\Desktop\FREE\Datos proyecto con FARMACIA\Publicacion\drive-download-20240215T230238Z-001\Albendazole Control-93Subjects.csv
DSdf_clean = pd.read_csv(r'C:\Users\Mariano\Desktop\FREE\Datos proyecto con FARMACIA\Publicacion\drive-download-20240215T230238Z-001\MEDIAN Albendazole DS-2-500Subjects.csv', sep=";")

#Pivot the dataframe to wide format separating subjects according to the “RECORD” column and the “TIME” column as the index but i have duplicate entries in the " TIME" column
DSdf_pivot = DSdf_clean.pivot_table(index=' TIME', columns='RECORD', values='DV')



#Calculate the median of all values for each row for every except the first column and except the first row
DSmedian_df = DSdf_pivot.iloc[0:, 1:].median(axis=1)
#Add the values from the "TIME" column from NCdf_pivot as the index
DSmedian_df
#Create a list with the values of the column "TIME" of the dataframe df_pivot
# Create a list with the values from the "TIME" column of the dataframe DSdf_pivot
DS_timelist = DSdf_pivot.index

#Add DStimelist as the index for DSmedian_df
DSmedian_df.index = DS_timelist
#Load "Puntos NC.csv" as a dataframe called df_puntoscontrol which has no header
df_puntosDS = pd.read_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\Puntos DS.csv', header=None, sep=";")


#Create a list with the values 0, 0.3333333333333333, 0.5, 1, 1.5, 2, 4, 6, 8, 10, 12, 24
listforobvs = [0, 0.3333333333333333, 0.5, 1, 1.5, 2, 4, 6, 8, 10, 12, 24]

#Replace the index of the dataframe df_puntoscontrol with the values of the list listforobvs
df_puntosDS.index = listforobvs

#Load "95Probability contourCTRK.csv" as a dataframe called "df_90probcontour" which has a header
DSdf_95Probcontour = pd.read_csv(r'C:\Users\Mariano\Desktop\FREE\Datos proyecto con FARMACIA\Publicacion\drive-download-20240215T230238Z-001\MEDIAN 95 Prob Contour AlbendazoleDS.csv', sep=";")

###  PLOT  ##
# Create a plot object called "plotDS" and add all the following steps
fig, plotDS = plt.subplots(figsize=(10, 6))

# Add median line in purple color and smooth it
plotDS.plot(DSmedian_df.index, DSmedian_df, color='green', label='Median', alpha=0.9, linewidth=2)
#Add the Upper and Lower 95% probability contour as filled area from df_90probcontour in purple color and smooth it
plotDS.fill_between(DSdf_95Probcontour['TIME'], DSdf_95Probcontour['Upper'], DSdf_95Probcontour['Lower'], color='green', alpha=0.1, label='95% Prediction Interval')
#Add the legend for the mean line
plotDS.legend(loc='upper right')

#Add the points from each column in the dataframe df_puntoscontrol as scatter plot in a purple color gradient, join the points with a smoot line, with each column with a different grade of purple over the mean line
for i in range(0, len(df_puntosDS.columns)):
    plotDS.plot(df_puntosDS.index, df_puntosDS.iloc[:, i], color='green', alpha=0.2, linewidth=1)
    plotDS.scatter(df_puntosDS.index, df_puntosDS.iloc[:, i], color='green', alpha=0.7, s=15, label='Observation')
    
#Add the legend for the scatter plot
plotDS.legend(loc='upper right')

# Customize plot elements
#The ticks from the x axis must represent the values in the column "TIME" (not the index) of the dataframe df_pivot but just the values that are multiples of 2
plotDS.set_xticks(range(0, 25, 2))
plotDS.set_xlabel('Time (h)')
plotDS.set_ylabel('ABZSO Plasma Concentration (μg/ml)')
plotDS.set_title('Simulation of the PBPK model for the Solid dispersion formulation of Albendazole')

#Make the lines start at the origin of the plot
plt.tight_layout()  
#Add a grid to the plot, very subtle
plotDS.grid(alpha=0.3)
# Adjust spacing for better readability

plt.show()
fig, plotDS = plt.subplots(figsize=(10, 6))

#Plot the objects "plotcontrol", "plotNC" and "plotDS" together 
# Assuming that plotcontrol and plotNC are also matplotlib objects similar to plotDS
# You can use the subplots function to create a figure with multiple subplots

fig, axs = plt.subplots(3, figsize=(10, 18))








# Create a figure with multiple subplots
fig, axs = plt.subplots(3, figsize=(5, 5))

# Plot for plotcontrol
axs[0].plot(CTRLmedian_df.index, CTRLmedian_df, color='purple', label='Median', alpha=0.9, linewidth=2)
axs[0].fill_between(CTRLdf_95Probcontour['TIME'], CTRLdf_95Probcontour['Upper'], CTRLdf_95Probcontour['Lower'], color='purple', alpha=0.1, label='95% Prediction Interval')

for i in range(0, len(df_puntoscontrol.columns)):
    axs[0].plot(df_puntoscontrol.index, df_puntoscontrol.iloc[:, i], color='purple', alpha=0.2, linewidth=1)
    axs[0].scatter(df_puntoscontrol.index, df_puntoscontrol.iloc[:, i], color='purple', alpha=0.7, s=15, label='Observation' if i == 0 else "")

axs[0].legend(loc='upper right')
axs[0].set_xticks(range(0, 25, 2))
axs[0].set_title('Simulations for the Control formulation of ABZ')
axs[0].grid(alpha=0.3)

# Plot for plotNC
axs[1].plot(NCmedian_df.index, NCmedian_df, color='blue', label='Median', alpha=0.9, linewidth=2)
axs[1].fill_between(NCdf_95Probcontour['TIME'], NCdf_95Probcontour['Upper'], NCdf_95Probcontour['Lower'], color='blue', alpha=0.1, label='95% Prediction Interval')

for i in range(0, len(df_puntosNC.columns)):
    axs[1].plot(df_puntosNC.index, df_puntosNC.iloc[:, i], color='blue', alpha=0.2, linewidth=1)
    axs[1].scatter(df_puntosNC.index, df_puntosNC.iloc[:, i], color='blue', alpha=0.7, s=15, label='Observation' if i == 0 else "")

axs[1].legend(loc='upper right')
axs[1].set_xticks(range(0, 25, 2))
axs[1].set_ylabel('ABZSO Plasma Concentration (μg/ml)')
axs[1].set_title('Simulations for the Nanocrystal formulation of ABZ')
axs[1].grid(alpha=0.3)

# Plot for plotDS
axs[2].plot(DSmedian_df.index, DSmedian_df, color='green', label='Median', alpha=0.9, linewidth=2)
axs[2].fill_between(DSdf_95Probcontour['TIME'], DSdf_95Probcontour['Upper'], DSdf_95Probcontour['Lower'], color='green', alpha=0.1, label='95% Prediction Interval')

for i in range(0, len(df_puntosDS.columns)):
    axs[2].plot(df_puntosDS.index, df_puntosDS.iloc[:, i], color='green', alpha=0.2, linewidth=1)
    axs[2].scatter(df_puntosDS.index, df_puntosDS.iloc[:, i], color='green', alpha=0.7, s=15, label='Observation' if i == 0 else "")

axs[2].legend(loc='upper right')
axs[2].set_xticks(range(0, 25, 2))
axs[2].set_xlabel('Time (h)')
axs[2].set_title('Simulations for the Solid dispersion formulation of ABZ')
axs[2].grid(alpha=0.3)

plt.tight_layout()
plt.show()
