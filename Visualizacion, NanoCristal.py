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



#Import NCCleanV2_PIVOT.csv
NCdf_pivot = pd.read_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\NCCleanV2_PIVOT.csv')

#Calculate the median of all values for each row for every except the first column and except the first row
NCmedian_df = NCdf_pivot.iloc[1:, 1:].median(axis=1)
#Add the values from the TIME column from NCdf_pivot as the index
NCmedian_df.index = NCdf_pivot.iloc[1:, 0]

#Create a list with the values of the colunm "TIME" of the dataframe df_pivot
NCtimelist= NCdf_pivot.iloc[1:, 0].tolist()

#Add the Value "0" as the first value in the list NCtimelist
NCtimelist.insert(0, 0)
#Replace the index of the dataframe df_pivot with the values in the column "TIME", skipping the first line
NCdf_pivot.index = NCtimelist

#Load "Puntos NC.csv" as a dataframe called df_puntoscontrol which has no header
df_puntosNC = pd.read_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\Puntos NC.csv', header=None)


#Create a list with the values 0, 0.3333333333333333, 0.5, 1, 1.5, 2, 4, 6, 8, 10, 12, 24
listforobvs = [0, 0.3333333333333333, 0.5, 1, 1.5, 2, 4, 6, 8, 10, 12, 24]
#Replace the index of the dataframe df_puntoscontrol with the values of the list listforobvs
df_puntosNC.index = listforobvs

#Load "95Probability contourCTRK.csv" as a dataframe called "df_90probcontour" which has a header
NCdf_95Probcontour = pd.read_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\Median NC 95 Prob contour.csv')

###  PLOT  ##
# Create a plot object called "plotNC" and add all the following steps
fig, plotNC = plt.subplots(figsize=(10, 6))

# Add median line in purple color and smooth it
plotNC.plot(NCmedian_df.index, NCmedian_df, color='blue', label='Median', alpha=0.9, linewidth=2)
#Add the Upper and Lower 95% probability contour as filled area from df_90probcontour in purple color and smooth it
plotNC.fill_between(NCdf_95Probcontour['TIME'], NCdf_95Probcontour['Upper'], NCdf_95Probcontour['Lower'], color='blue', alpha=0.1, label='95% Prediction Interval')
#Add the legend for the mean line
plotNC.legend(loc='upper right')

#Add the points from each column in the dataframe df_puntoscontrol as scatter plot in a purple color gradient, join the points with a smoot line, with each column with a different grade of purple over the mean line
for i in range(0, len(df_puntosNC.columns)):
    plotNC.plot(df_puntosNC.index, df_puntosNC.iloc[:, i], color='blue', alpha=0.2, linewidth=1)
    plotNC.scatter(df_puntosNC.index, df_puntosNC.iloc[:, i], color='blue', alpha=0.7, s=15, label='Observation')
    
#Add the legend for the scatter plot
plotNC.legend(loc='upper right')

# Customize plot elements
#The ticks from the x axis must represent the values in the column "TIME" (not the index) of the dataframe df_pivot but just the values that are multiples of 2
plotNC.set_xticks(range(0, 25, 2))
plotNC.set_xlabel('Time (h)')
plotNC.set_ylabel('ABZSO Plasma Concentration (μg/ml)')
plotNC.set_title('Simulation of the PBPK model for the Nanocrystal formulation of Albendazole')

#Make the lines start at the origin of the plot
plt.tight_layout()  
#Add a grid to the plot, very subtle
plotNC.grid(alpha=0.3)
# Adjust spacing for better readability

plt.show()
fig, plotNC = plt.subplots(figsize=(10, 6))