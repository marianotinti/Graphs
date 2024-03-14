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



# Loaded variable 'df' from URI: c:\Users\Mariano\Desktop\FREE\Datos proyecto con FARMACIA\Publicacion\drive-download-20240215T230238Z-001\Albendazole Control-93Subjects.csv
CTRLdf_clean = pd.read_csv(r'C:\Users\Mariano\Desktop\FREE\Datos proyecto con FARMACIA\Publicacion\drive-download-20240215T230238Z-001\V5 CLEAN Albendazole Control-250Subjects.csv', sep=";")

#Pivot the dataframe to wide format separating subjects according to the “RECORD” column and the “TIME” column as the index but i have duplicate entries in the " TIME" column
CTRLdf_pivot = CTRLdf_clean.pivot_table(index=' TIME', columns='RECORD', values='DV')

# Calculate the mean of all values for each row for every except the first column and except the first row
CTRLmean_df = CTRLdf_pivot.iloc[1:, 1:].mean(axis=1)
mean_df.head(10)
#Save mean_Df as "meancontrolv2df.csv"

mean_df.to_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\meancontrolv2df.csv')

#Calculate the median of all values for each row for every except the first column and except the first row
CTRLmedian_df = CTRLdf_pivot.iloc[1:, 1:].median(axis=1)


#import timelist.csv as a dataframe called "timelist"
CTRLtimelist = pd.read_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\timelist.csv', sep=";")
#transform timelist to a list
CTRLtimelist = CTRLtimelist['0'].tolist()
#Import timelist.csv as a dataframe called "dftimelist"
dftimelist = pd.read_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\timelist.csv')
#transform dftimelist to a list
dftimelist = dftimelist['0'].tolist()

#Replace the index of the dataframe mean_df with the values of the dataframe timelist
##PARA LA MEDIA NO HACE FALTA?
CTRLmedian_df.index = CTRLtimelist
#print(mean_df)

#Load "Puntos Control.csv" as a dataframe called df_puntoscontrol which has no header
df_puntoscontrol = pd.read_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\Puntos Control.csv', header=None, sep=";")


#Create a list with the values 0, 0.3333333333333333, 0.5, 1, 1.5, 2, 4, 6, 8, 10, 12, 24
listforobvs = [0, 0.3333333333333333, 0.5, 1, 1.5, 2, 4, 6, 8, 10, 12, 24]

#Replace the index of the dataframe df_puntoscontrol with the values of the list listforobvs
df_puntoscontrol.index = listforobvs

#Load "95Probability contourCTRK.csv" as a dataframe called "df_90probcontour" which has a header
CTRLdf_95Probcontour = pd.read_csv(r'c:\\Users\\Mariano\\Desktop\\FREE\\Datos proyecto con FARMACIA\\Publicacion\\drive-download-20240215T230238Z-001\\V5 ProbContour Albendazole Control-250Subjects.csv', sep=";")

##PLOT
#Create a plot called "plotcontrol"
# Create a plot object called "plotcontrol"
fig, plotcontrol = plt.subplots(figsize=(10, 6))
plotcontrol.set_title('Plot Control')

# Add median line in purple color and smooth it
plotcontrol.plot(CTRLmedian_df.index, CTRLmedian_df, color='purple', label='Median', alpha=0.9, linewidth=2)
#Add the Upper and Lower 95% probability contour as filled area from df_90probcontour in purple color and smooth it
plotcontrol.fill_between(CTRLdf_95Probcontour['TIME'], CTRLdf_95Probcontour['Upper'], CTRLdf_95Probcontour['Lower'], color='purple', alpha=0.1, label='95% Prediction Interval')
#Add the legend for the mean line
plotcontrol.legend(loc='upper right')

#Add the points from each column in the dataframe df_puntoscontrol as scatter plot in a purple color gradient, join the points with a smoot line, with each column with a different grade of purple over the mean line
for i in range(0, len(df_puntoscontrol.columns)):
    plotcontrol.plot(df_puntoscontrol.index, df_puntoscontrol.iloc[:, i], color='purple', alpha=0.2, linewidth=1)
    plotcontrol.scatter(df_puntoscontrol.index, df_puntoscontrol.iloc[:, i], color='purple', alpha=0.7, s=15)

#Add the legend for the scatter plot
plotcontrol.legend(loc='upper right')

# Customize plot elements
#The ticks from the x axis must represent the values in the column "TIME" (not the index) of the dataframe df_pivot but just the values that are multiples of 2
plotcontrol.set_xticks(range(0, 25, 2))
plotcontrol.set_xlabel('Time (h)')
plotcontrol.set_ylabel('ABZSO Plasma Concentration (μg/ml)')
plotcontrol.set_title('Simulation of the PBPK model for the Control formulation of Albendazole')

#Make the lines start at the origin of the plot
plt.tight_layout()  
#Add a grid to the plot, very subtle
plotcontrol.grid(alpha=0.3)
# Adjust spacing for better readability

plt.show()
plt.figure(figsize=(10, 6))
plt.title('Plot Control')