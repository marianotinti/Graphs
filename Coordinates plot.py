#Load all necessary libraries and functions for data analysis and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import adjustText
from adjustText import adjust_text

#Load "CoordenadasSite.csv" file with ";" as separator
coordenadas = pd.read_csv("CoordenadasSite.csv", sep=";")
#Show the first 5 rows of the dataset
coordenadas.head()

#Plot "coordenadas" as a scatter plot where "Eje 1" is the X axis and "Eje 2" is the Y axis, color according to "Ax". Make the points bigger and transparent and the size of the plot 10x10 and the limits -1 to 1

plt.figure(figsize=(10,10))
sns.scatterplot(data=coordenadas, x="Axis 1", y="Axis 2", hue="Site/Bacteria", s=100, alpha=0.5)
plt.xlim(-1,0.5)
plt.ylim(-0.75,0.75)
#Add the site names to the plot
#texts = [plt.text(coordenadas["Axis 1"][i], coordenadas["Axis 2"][i], coordenadas["Variable"][i], ha='left', va='center', rotation = 0) for i in range(len(coordenadas))]
#adjust_text(texts, arrowprops=dict(arrowstyle="->", color='r', alpha=0.5))
#Show the plot
plt.show()

#Load "CoordenadasLoc.csv" with ";" as separator
coordenadasloc = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/CoordenadasLoc.csv", sep=";")
coordenadasloc
#Plot "coordenadasloc" as a scatter plot where "Eje 1" is the X axis and "Eje 2" is the Y axis, color according to "Ax". Make the points bigger and transparent and the size of the plot 10x10 and the limits -1 to 1

plt.figure(figsize=(10,5))
sns.scatterplot(data=coordenadasloc, x="Axis 1", y="Axis 2", hue="Bacteria/Location", s=50, alpha=0.5)
plt.xlim(-0.4,0.25)
plt.ylim(-0.1,0.1)
#Add the site names to the plot
texts = [plt.text(coordenadasloc["Axis 1"][i], coordenadasloc["Axis 2"][i], coordenadasloc["Variable"][i], ha='left', va='center', rotation = 55) for i in range(len(coordenadasloc))]
adjust_text(texts, force_explode=(0.5,0,5, force_pull=(1,2), arrowprops=dict(arrowstyle="->", color='r', alpha=0.5))
#Show the plot
plt.show()
