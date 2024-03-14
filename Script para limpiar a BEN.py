#Load pandas as pd
import micropip
import pandas as pd
micropip install openpyxl

#Load all the basic libraries to perform data analysis and data wrangling
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import warnings
import time
import datetime
import gc
import pickle
import pandas as pd
import pandas as pd


#Load "BENJAMN_DATA_CSV_SITES REEMPLAZADOS.csv" as df
df = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/BENJAMIN_DATA_CSV.csv")
#Load "IDSMO.csv" and "IDSITES.csv" which have ";" as separator
IDSMO = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/IDSMO.csv", sep=";")
IDSITES = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/IDSITES.csv", sep=";")

#Create a dictionary with the values in IDSMO where is the key and Organisms. 

#Replace the values in the column "MO" in df with the values in IDSMO, using id as the key

df["MO"] = df["MO"].replace(IDSMO.set_index("ID")["Organisms"].to_dict())
#Replace the values in the column "SITE" in df with the values in IDSITES, using id as the key
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace(IDSITES.set_index("ID")["Culture Site"].to_dict())

#Replace the following values in "CULTURE_SITE" in the following way:
#Replace "LF FOOT" and "LF Heel Bulb" with "LF Foot"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"LF FOOT": "LF Foot", "LF Heel Bulb": "LF Foot"})
#Replace "RF FOOT" and "RF Heel Bulb" with "RF Foot"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"RF FOOT": "RF Foot", "RF Heel Bulb": "RF Foot"})
#Replace "LH FOOT" and "LH Heel Bulb" with "LH Foot"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"LH FOOT": "LH Foot", "LH Heel Bulb": "LH Foot"})
#Replace "RH FOOT" and "RH Heel Bulb" with "RH Foot"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"RH FOOT": "RH Foot", "RH Heel Bulb": "RH Foot"})
#Replace "Foot (unspecified)", "Heel Bulb Unspecified", "Coffin Bone Unspecified", "Coffin Joint" and "Navicular Bursa" with "FOOT (Unspecified)"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"Foot (unspecified)": "FOOT (Unspecified)", "Heel Bulb Unspecified": "FOOT (Unspecified)", "Coffin Bone Unspecified": "FOOT (Unspecified)", "Coffin Joint": "FOOT (Unspecified)", "Navicular Bursa": "FOOT (Unspecified)"})
#Replace "LF Coffin Bone", "RF Coffin Bone", "LH Coffin Bone" and "RH Coffin Bone" with "COFFIN BONE"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"LF Coffin Bone": "COFFIN BONE", "RF Coffin Bone": "COFFIN BONE", "LH Coffin Bone": "COFFIN BONE", "RH Coffin Bone": "COFFIN BONE"})
#Replace "LF Sequestrum", "RF Sequestrum", "LH Sequestrum" and "RH Sequestrum" and "Sequestrum Unspecified" with "COFFIN BONE"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"LF Sequestrum": "COFFIN BONE", "RF Sequestrum": "COFFIN BONE", "LH Sequestrum": "COFFIN BONE", "RH Sequestrum": "COFFIN BONE", "Sequestrum Unspecified": "COFFIN BONE"})
#Replace "LF Puncture Wound", "RF Puncture Wound", "LH Puncture Wound","RH Puncture Wound", "Puncture Wound Unspecified", "LF Laceration","RF Laceration", "LH Laceration", "RH Laceration" and "Foot Laceration Unspecified" with "WOUND"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"LF Puncture Wound": "WOUND", "RF Puncture Wound": "WOUND", "LH Puncture Wound": "WOUND", "RH Puncture Wound": "WOUND", "Puncture Wound Unspecified": "WOUND", "LF Laceration": "WOUND", "RF Laceration": "WOUND", "LH Laceration": "WOUND", "RH Laceration": "WOUND", "Foot Laceration Unspecified": "WOUND"})
#Replace "LF Coronary Band", "RF Coronary Band", "LH Coronary Band", "RH Coronary Band" and "Coronary Band Unspecified" with "CORONARY BAND"
df["CULTURE_SITE"] = df["CULTURE_SITE"].replace({"LF Coronary Band": "CORONARY BAND", "RF Coronary Band": "CORONARY BAND", "LH Coronary Band": "CORONARY BAND", "RH Coronary Band": "CORONARY BAND", "Coronary Band Unspecified": "CORONARY BAND"})

#Create a column named "Polymicrobial" in df
df["Polymicrobial"] = "No"
#If an ID has more than one "MO" replace the value in Polymicrobial with "Yes"
df.loc[df["ID"].duplicated(keep=False), "Polymicrobial"] = "Yes"
 #Create a copy of df named df2
df2 = df.copy()

#In df2, eliminate the lines with duplicated values in "ID"
df2 = df2.drop_duplicates(subset="ID", keep="first")
df2.head()
#Show the data
df.head()
#Export the df as "BENJAMIN_DATA_CSV_SITES REEMPLAZADOS.csv"
df.to_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/BENJAMIN_DATA_REPLACED.csv", index=False)
#Export the df2 as "BENJAMIN_DATA_POLYMICROBIAL.csv"
df.to_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/BENJAMIN_DATA_POLYMICROBIAL.csv", index=False)
#Count the values in "CULTURE_SITE"
df["CULTURE_SITE"].value_counts()