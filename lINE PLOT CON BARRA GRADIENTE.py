# Load all necessary libraries for data analysis and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Load "Fluidintestine.csv" with ";" as a separator
import matplotlib.cm as cm

df = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos proyecto con FARMACIA/Publicacion/PSA/Fluidintestine.csv", sep=";", header=0, index_col=0)
#Print the first 5 rows of the dataframe
print(df.head())
#Select the first line and save it as a list
list = df.iloc[0]

#Select the first column of the dataframe
list
#Plot the data as lines, with a separate line for each column. USing the "crest" color gradient (limint the lightness to 75) according to the value in the header of the column
plt.figure(figsize=(10, 6), grid=False)
plot= sns.lineplot(data=df, dashes=False, palette="crest", linewidth=1.5, legend=False)
plt.colorbar(plot)
ax = sns.barplot(x=df.index, y=list, hue=list, palette='crest', dodge=False)

####
plt.xlabel('Time (h)')
plt.ylabel('ABZO Concentration (ug/L)')
#Make the labels in the X axis go in steps of 1
plt.xticks(np.arange(0, 24, 1))
#Make the grid lighter
plt.grid(alpha=0.1)
plt.show()