# Import all necessary libraries for data processing and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

##Define functions##
def get_label_rotation(angle, offset):
    # Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle + offset)
    if angle <= np.pi:
        alignment = "right"
        rotation = rotation + 180
    else: 
        alignment = "left"
    return rotation, alignment

padding = 3
def add_labels(angles, values, labels, offset, ax):
    
    # This is the space between the end of the bar and the label
    padding = 0
    
    # Iterate over angles, values, and labels, to add all of them.
    for angle, value, label, in zip(angles, values, labels):
        angle = angle
        
        # Obtain text rotation and alignment
        rotation, alignment = get_label_rotation(angle, offset)

        # And finally add the text
        # Check if value is over 100
        if value > 100:
            y = 100
        else:
            y = value + padding

        ax.text(
            x=angle, 
            y=y, 
            s=label, 
            ha=alignment, 
            va="center", 
            rotation=rotation, 
            rotation_mode="anchor"
        ) 


#Import the following csv files "Ecoli.csv", "Ecloacae.csv","Klebsiella.csv","AlphaStrep.csv","BetaStrep.csv","PAgglom.csv","Pmirabilis.csv","PVulgaris.csv"
ecoli = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/Ecoli.csv", sep=";")
ecloacae = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/Ecloacae.csv", sep=";")
kleb = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/Klebsiella.csv", sep=";")
alphastrep = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/AlphaStrep.csv", sep=";")
betastrep = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/BetaStrep.csv", sep=";")
pagglom = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/PAgglom.csv", sep=";")
pmirabilis = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/PMirabilis.csv", sep=";")
pvulgaris = pd.read_csv("C:/Users/Mariano/Desktop/FREE/Datos Bejnamin/PVulgaris.csv", sep=";")

#Drop the first two columns of each dataframe
ecoli = ecoli.drop(ecoli.columns[[0,1]], axis=1)
ecloacae = ecloacae.drop(ecloacae.columns[[0,1]], axis=1)
kleb = kleb.drop(kleb.columns[[0,1]], axis=1)
alphastrep = alphastrep.drop(alphastrep.columns[[0,1]], axis=1)
betastrep = betastrep.drop(betastrep.columns[[0,1]], axis=1)
pagglom = pagglom.drop(pagglom.columns[[0,1]], axis=1)
pmirabilis = pmirabilis.drop(pmirabilis.columns[[0,1]], axis=1)
pvulgaris = pvulgaris.drop(pvulgaris.columns[[0,1]], axis=1)

##FOR ecoli##
#Pivot ecoli to long format
ecoli = ecoli.melt(var_name="Antibiotic", value_name="Value")
#Drop the NaN values
ecoli = ecoli.dropna()
#Replace the I values for S
ecoli.loc[ecoli['Value'] == 'I', 'Value'] = 'S'

# Count the occurrences of "R" for each antibiotic
ecolires_counts = ecoli[ecoli['Value'] == 'R']['Antibiotic'].value_counts()
#Count the ocurrences of "S" for each antibiotic
ecolis_counts = ecoli[ecoli['Value'] == 'S']['Antibiotic'].value_counts()

# Calculate the relative frequency by dividing by the total count and multiplying by 100
ecolitotal_count = ecolires_counts + ecolis_counts

ecolirelative_frequency = (ecolires_counts / ecolitotal_count) * 100
#Reset index
ecolirelative_frequency = ecolirelative_frequency.reset_index()
#Rename the columns to "Antibiotic" and "Count"
ecolirelative_frequency.columns = ["Antibiotic", "Count"]
# Print the relative frequency for each antibiotic
print(ecolirelative_frequency)

#Save the dataframe into ecoli_count
ecoli_count = ecolirelative_frequency


# Sort by count
ecoli_count = ecoli_count.sort_values(by=['Count'])
 
# Replace specific values in the "Antibiotic" column
ecoli_count['Antibiotic'] = ecoli_count['Antibiotic'].replace({
    'Naxcel': 'Ceftiofur',
    'Tribrissen ': 'Trimethoprim/Sulfamethoxazole',
    'Timentin ': 'Ticarcillin/Clavulanate',
    'Rifampin ': 'Rifampicin'
})

#Create a column named "Group"
ecoli_count['Group'] = "Ecoli"
# Replace the value in the "Group" column to "Cephalosporin" if the value in the "Antibiotic" column is equal to "Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "]), "Group"] = "Cephalosporin"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Ampicillin ","Oxacillin ", "Ticarcillin ", "Ticarcillin/Clavulanate"]), "Group"] = "Penicillin"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Amikacin","Gentamicin ", "Neomycin "]), "Group"] = "Aminoglycoside"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Erythromycin ","Azithromycin "]), "Group"] = "Macrolide"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Enrofloxacin "]), "Group"] = "Fluoroquinolone"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Rifampicin"]), "Group"] = "Rifamicin"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Trimethoprim/Sulfamethoxazole"]), "Group"] = "Sulfonamide"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Tetracycline ","Doxycycline "]), "Group"] = "Tetracyclin"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Nitrofurantoin "]), "Group"] = "Nitrofuran"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Chloramphenicol "]), "Group"] = "Amphenicol"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Imipenem "]), "Group"] = "Carbapenem"
ecoli_count.loc[ecoli_count['Antibiotic'].isin(["Polymyxin B "]), "Group"] = "Polymyxin"

# Show the updated ecoli_count dataframe
ecoli_count

# Reorder the dataframe
ecoli_count = (
    ecoli_count
    .groupby(["Group"])
    .apply(lambda x: x.sort_values(["Count"], ascending = False))
    .reset_index(drop=True)
)
#Turn "Count" into an integer
ecoli_count['Count'] = ecoli_count['Count'].astype(int)

##FOR pmirabilis##
#Pivot pmirabilis to long format
pmirabilis = pmirabilis.melt(var_name="Antibiotic", value_name="Value")
#Drop the NaN values
pmirabilis = pmirabilis.dropna()
#Replace the I values for S
pmirabilis.loc[pmirabilis['Value'] == 'I', 'Value'] = 'S'

# Count the occurrences of "R" for each antibiotic
pmirabilisres_counts = pmirabilis[pmirabilis['Value'] == 'R']['Antibiotic'].value_counts()
#Count the ocurrences of "S" for each antibiotic
pmirabiliss_counts = pmirabilis[pmirabilis['Value'] == 'S']['Antibiotic'].value_counts()

# Calculate the relative frequency by dividing by the total count and multiplying by 100
pmirabilistotal_count = pmirabilisres_counts + pmirabiliss_counts

pmirabilisrelative_frequency = (pmirabilisres_counts / pmirabilistotal_count) * 100
#Reset index
pmirabilisrelative_frequency = pmirabilisrelative_frequency.reset_index()
#Rename the columns to "Antibiotic" and "Count"
pmirabilisrelative_frequency.columns = ["Antibiotic", "Count"]
# Print the relative frequency for each antibiotic
print(pmirabilisrelative_frequency)

#Replace Nan value in pmirabilisrelative_frequency for 100
pmirabilisrelative_frequency['Count'] = pmirabilisrelative_frequency['Count'].fillna(100)

#Save the dataframe into pmirabilis_count
pmirabilis_count = pmirabilisrelative_frequency

# Sort by count
pmirabilis_count = pmirabilis_count.sort_values(by=['Count'])

# Replace specific values in the "Antibiotic" column
pmirabilis_count['Antibiotic'] = pmirabilis_count['Antibiotic'].replace({
    'Naxcel': 'Ceftiofur',
    'Tribrissen ': 'Trimethoprim/Sulfamethoxazole',
    'Timentin ': 'Ticarcillin/Clavulanate',
    'Rifampin ': 'Rifampicin'
})

#Create a column named "Group"
pmirabilis_count['Group'] = "Pmirabilis"
# Replace the value in the "Group" column to "Cephalosporin" if the value in the "Antibiotic" column is equal to "Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "]), "Group"] = "Cephalosporin"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Ampicillin ","Oxacillin ", "Ticarcillin ", "Ticarcillin/Clavulanate"]), "Group"] = "Penicillin"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Amikacin","Gentamicin ", "Neomycin "]), "Group"] = "Aminoglycoside"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Erythromycin ","Azithromycin "]), "Group"] = "Macrolide"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Enrofloxacin "]), "Group"] = "Fluoroquinolone"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Rifampicin"]), "Group"] = "Rifamicin"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Trimethoprim/Sulfamethoxazole"]), "Group"] = "Sulfonamide"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Tetracycline ","Doxycycline "]), "Group"] = "Tetracyclin"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Nitrofurantoin "]), "Group"] = "Nitrofuran"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Chloramphenicol "]), "Group"] = "Amphenicol"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Imipenem "]), "Group"] = "Carbapenem"
pmirabilis_count.loc[pmirabilis_count['Antibiotic'].isin(["Polymyxin B "]), "Group"] = "Polymyxin"

# Show the updated pmirabilis_count dataframe
pmirabilis_count

# Reorder the dataframe
pmirabilis_count = (
    pmirabilis_count
    .groupby(["Group"])
    .apply(lambda x: x.sort_values(["Count"], ascending = False))
    .reset_index(drop=True)
)
#Turn "Count" into an integer
pmirabilis_count['Count'] = pmirabilis_count['Count'].astype(int)


##FOR pvulgaris##
#Pivot pvulgaris to long format
pvulgaris = pvulgaris.melt(var_name="Antibiotic", value_name="Value")
#Drop the NaN values
pvulgaris = pvulgaris.dropna()
#Replace the I values for S
pvulgaris.loc[pvulgaris['Value'] == 'I', 'Value'] = 'S'

# Count the occurrences of "R" for each antibiotic
pvulgarisres_counts = pvulgaris[pvulgaris['Value'] == 'R']['Antibiotic'].value_counts()
#Count the ocurrences of "S" for each antibiotic
pvulgariss_counts = pvulgaris[pvulgaris['Value'] == 'S']['Antibiotic'].value_counts()

# Calculate the relative frequency by dividing by the total count and multiplying by 100
pvulgaristotal_count = pvulgarisres_counts + pvulgariss_counts

pvulgarisrelative_frequency = (pvulgarisres_counts / pvulgaristotal_count) * 100
#Reset index
pvulgarisrelative_frequency = pvulgarisrelative_frequency.reset_index()
#Rename the columns to "Antibiotic" and "Count"
pvulgarisrelative_frequency.columns = ["Antibiotic", "Count"]
# Print the relative frequency for each antibiotic
print(pvulgarisrelative_frequency)

#Replace Nan value in pvulgarisrelative_frequency for 100
pvulgarisrelative_frequency['Count'] = pvulgarisrelative_frequency['Count'].fillna(100)

#Save the dataframe into pvulgaris_count
pvulgaris_count = pvulgarisrelative_frequency

# Sort by count
pvulgaris_count = pvulgaris_count.sort_values(by=['Count'])

# Replace specific values in the "Antibiotic" column
pvulgaris_count['Antibiotic'] = pvulgaris_count['Antibiotic'].replace({
    'Naxcel': 'Ceftiofur',
    'Tribrissen ': 'Trimethoprim/Sulfamethoxazole',
    'Timentin ': 'Ticarcillin/Clavulanate',
    'Rifampin ': 'Rifampicin'
})

#Create a column named "Group"
pvulgaris_count['Group'] = "Pvulgaris"
# Replace the value in the "Group" column to "Cephalosporin" if the value in the "Antibiotic" column is equal to "Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "]), "Group"] = "Cephalosporin"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Ampicillin ","Oxacillin ", "Ticarcillin ", "Ticarcillin/Clavulanate"]), "Group"] = "Penicillin"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Amikacin","Gentamicin ", "Neomycin "]), "Group"] = "Aminoglycoside"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Erythromycin ","Azithromycin "]), "Group"] = "Macrolide"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Enrofloxacin "]), "Group"] = "Fluoroquinolone"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Rifampicin"]), "Group"] = "Rifamicin"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Trimethoprim/Sulfamethoxazole"]), "Group"] = "Sulfonamide"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Tetracycline ","Doxycycline "]), "Group"] = "Tetracyclin"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Nitrofurantoin "]), "Group"] = "Nitrofuran"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Chloramphenicol "]), "Group"] = "Amphenicol"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Imipenem "]), "Group"] = "Carbapenem"
pvulgaris_count.loc[pvulgaris_count['Antibiotic'].isin(["Polymyxin B "]), "Group"] = "Polymyxin"

# Show the updated pvulgaris_count dataframe
pvulgaris_count

# Reorder the dataframe
pvulgaris_count = (
    pvulgaris_count
    .groupby(["Group"])
    .apply(lambda x: x.sort_values(["Count"], ascending = False))
    .reset_index(drop=True)
)
#Turn "Count" into an integer
pvulgaris_count['Count'] = pvulgaris_count['Count'].astype(int)



##FOR pagglom##
#Pivot pagglom to long format
pagglom = pagglom.melt(var_name="Antibiotic", value_name="Value")
#Drop the NaN values
pagglom = pagglom.dropna()
#Replace the I values for S
pagglom.loc[pagglom['Value'] == 'I', 'Value'] = 'S'

# Count the occurrences of "R" for each antibiotic
pagglomres_counts = pagglom[pagglom['Value'] == 'R']['Antibiotic'].value_counts()
#Count the ocurrences of "S" for each antibiotic
paggloms_counts = pagglom[pagglom['Value'] == 'S']['Antibiotic'].value_counts()

# Calculate the relative frequency by dividing by the total count and multiplying by 100
pagglomtotal_count = pagglomres_counts + paggloms_counts

pagglomrelative_frequency = (pagglomres_counts / pagglomtotal_count) * 100
#Reset index
pagglomrelative_frequency = pagglomrelative_frequency.reset_index()
#Rename the columns to "Antibiotic" and "Count"
pagglomrelative_frequency.columns = ["Antibiotic", "Count"]
# Print the relative frequency for each antibiotic
print(pagglomrelative_frequency)

#Save the dataframe into pagglom_count
pagglom_count = pagglomrelative_frequency

# Sort by count
pagglom_count = pagglom_count.sort_values(by=['Count'])

# Replace specific values in the "Antibiotic" column
pagglom_count['Antibiotic'] = pagglom_count['Antibiotic'].replace({
    'Naxcel': 'Ceftiofur',
    'Tribrissen ': 'Trimethoprim/Sulfamethoxazole',
    'Timentin ': 'Ticarcillin/Clavulanate',
    'Rifampin ': 'Rifampicin'
})

#Create a column named "Group"
pagglom_count['Group'] = "Pagglom"
# Replace the value in the "Group" column to "Cephalosporin" if the value in the "Antibiotic" column is equal to "Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "]), "Group"] = "Cephalosporin"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Ampicillin ","Oxacillin ", "Ticarcillin ", "Ticarcillin/Clavulanate"]), "Group"] = "Penicillin"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Amikacin","Gentamicin ", "Neomycin "]), "Group"] = "Aminoglycoside"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Erythromycin ","Azithromycin "]), "Group"] = "Macrolide"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Enrofloxacin "]), "Group"] = "Fluoroquinolone"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Rifampicin"]), "Group"] = "Rifamicin"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Trimethoprim/Sulfamethoxazole"]), "Group"] = "Sulfonamide"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Tetracycline ","Doxycycline "]), "Group"] = "Tetracyclin"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Nitrofurantoin "]), "Group"] = "Nitrofuran"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Chloramphenicol "]), "Group"] = "Amphenicol"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Imipenem "]), "Group"] = "Carbapenem"
pagglom_count.loc[pagglom_count['Antibiotic'].isin(["Polymyxin B "]), "Group"] = "Polymyxin"

# Show the updated pagglom_count dataframe
pagglom_count

# Reorder the dataframe
pagglom_count = (
    pagglom_count
    .groupby(["Group"])
    .apply(lambda x: x.sort_values(["Count"], ascending = False))
    .reset_index(drop=True)
)
#Turn "Count" into an integer
pagglom_count['Count'] = pagglom_count['Count'].astype(int)



#FOR alphastrep##
#Pivot alphastrep to long format
alphastrep = alphastrep.melt(var_name="Antibiotic", value_name="Value")
#Drop the NaN values
alphastrep = alphastrep.dropna()
#Replace the I values for S
alphastrep.loc[alphastrep['Value'] == 'I', 'Value'] = 'S'

# Count the occurrences of "R" for each antibiotic
alphastrep_res_counts = alphastrep[alphastrep['Value'] == 'R']['Antibiotic'].value_counts()
#Count the ocurrences of "S" for each antibiotic
alphastrep_s_counts = alphastrep[alphastrep['Value'] == 'S']['Antibiotic'].value_counts()

# Calculate the relative frequency by dividing by the total count and multiplying by 100
alphastrep_total_count = alphastrep_res_counts + alphastrep_s_counts

alphastrep_relative_frequency = (alphastrep_res_counts / alphastrep_total_count) * 100
#Reset index
alphastrep_relative_frequency = alphastrep_relative_frequency.reset_index()
#Rename the columns to "Antibiotic" and "Count"
alphastrep_relative_frequency.columns = ["Antibiotic", "Count"]
# Print the relative frequency for each antibiotic
print(alphastrep_relative_frequency)

#Save the dataframe into alphastrep_count
alphastrep_count = alphastrep_relative_frequency

# Sort by count
alphastrep_count = alphastrep_count.sort_values(by=['Count'])

# Replace specific values in the "Antibiotic" column
alphastrep_count['Antibiotic'] = alphastrep_count['Antibiotic'].replace({
    'Naxcel': 'Ceftiofur',
    'Tribrissen': 'Trimethoprim/Sulfamethoxazole',
    'Timentin': 'Ticarcillin/Clavulanate',
    'Rifampin ': 'Rifampicin'
})

#Create a column named "Group"
alphastrep_count['Group'] = "Alphastrep"
# Replace the value in the "Group" column to "Cephalosporin" if the value in the "Antibiotic" column is equal to "Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "]), "Group"] = "Cephalosporin"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Ampicillin ","Oxacillin", "Ticarcillin", "Ticarcillin/Clavulanate", "Penicillin"]), "Group"] = "Penicillin"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Amikacin","Gentamicin ", "Neomycin "]), "Group"] = "Aminoglycoside"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Erythromycin","Azithromycin "]), "Group"] = "Macrolide"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Enrofloxacin", "Ciprofloxacin "]), "Group"] = "Fluoroquinolone"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Rifampicin"]), "Group"] = "Rifamicin"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Trimethoprim/Sulfamethoxazole"]), "Group"] = "Sulfonamide"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Tetracycline","Doxycycline "]), "Group"] = "Tetracyclin"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Nitrofurantoin "]), "Group"] = "Nitrofuran"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Chloramphenicol "]), "Group"] = "Amphenicol"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Imipenem "]), "Group"] = "Carbapenem"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Polymyxin B "]), "Group"] = "Polymyxin"
alphastrep_count.loc[alphastrep_count['Antibiotic'].isin(["Vancomycin"]), "Group"] = "Glycopeptide"
# Show the updated alphastrep_count dataframe
alphastrep_count

# Reorder the dataframe
alphastrep_count = (
    alphastrep_count
    .groupby(["Group"])
    .apply(lambda x: x.sort_values(["Count"], ascending = False))
    .reset_index(drop=True)
)
#Turn "Count" into an integer
alphastrep_count['Count'] = alphastrep_count['Count'].astype(int)

alphastrep_count

#FOR betastrep##
#Pivot betastrep to long format
betastrep = betastrep.melt(var_name="Antibiotic", value_name="Value")
#Drop the NaN values
betastrep = betastrep.dropna()
#Replace the I values for S
betastrep.loc[betastrep['Value'] == 'I', 'Value'] = 'S'

# Count the occurrences of "R" for each antibiotic
betastrep_res_counts = betastrep[betastrep['Value'] == 'R']['Antibiotic'].value_counts()
#Count the ocurrences of "S" for each antibiotic
betastrep_s_counts = betastrep[betastrep['Value'] == 'S']['Antibiotic'].value_counts()
betastrep_res_counts ###DIVIDO POR CERO!!! CHEQUEAR###
# Calculate the relative frequency by dividing by the total count and multiplying by 100
betastrep_total_count = betastrep_res_counts + betastrep_s_counts
betastrep_s_counts

betastrep_relative_frequency = (betastrep_res_counts / betastrep_total_count) * 100
#Reset index
betastrep_relative_frequency = betastrep_relative_frequency.reset_index()
#Rename the columns to "Antibiotic" and "Count"
betastrep_relative_frequency.columns = ["Antibiotic", "Count"]
# Replace the Nan value for Amikacin in "Count" for 100
betastrep_relative_frequency['Count'] = betastrep_relative_frequency['Count'].fillna(100)
# Print the relative frequency for each antibiotic
print(betastrep_relative_frequency)

#Save the dataframe into betastrep_count
betastrep_count = betastrep_relative_frequency

# Sort by count
betastrep_count = betastrep_count.sort_values(by=['Count'])

# Replace specific values in the "Antibiotic" column
betastrep_count['Antibiotic'] = betastrep_count['Antibiotic'].replace({
    'Naxcel': 'Ceftiofur',
    'Tribrissen': 'Trimethoprim/Sulfamethoxazole',
    'Timentin': 'Ticarcillin/Clavulanate',
    'Rifampin ': 'Rifampicin'
})

#Create a column named "Group"
betastrep_count['Group'] = "Betastrep"
# Replace the value in the "Group" column to "Cephalosporin" if the value in the "Antibiotic" column is equal to "Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "]), "Group"] = "Cephalosporin"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Ampicillin ","Oxacillin", "Ticarcillin", "Ticarcillin/Clavulanate", "Penicillin"]), "Group"] = "Penicillin"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Amikacin","Gentamicin ", "Neomycin "]), "Group"] = "Aminoglycoside"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Erythromycin","Azithromycin "]), "Group"] = "Macrolide"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Enrofloxacin", "Ciprofloxacin "]), "Group"] = "Fluoroquinolone"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Rifampicin"]), "Group"] = "Rifamicin"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Trimethoprim/Sulfamethoxazole"]), "Group"] = "Sulfonamide"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Tetracycline","Doxycycline "]), "Group"] = "Tetracyclin"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Nitrofurantoin "]), "Group"] = "Nitrofuran"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Chloramphenicol "]), "Group"] = "Amphenicol"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Imipenem "]), "Group"] = "Carbapenem"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Polymyxin B "]), "Group"] = "Polymyxin"
betastrep_count.loc[betastrep_count['Antibiotic'].isin(["Vancomycin"]), "Group"] = "Glycopeptide"
# Show the updated betastrep_count dataframe
betastrep_count

# Reorder the dataframe
betastrep_count = (
    betastrep_count
    .groupby(["Group"])
    .apply(lambda x: x.sort_values(["Count"], ascending = False))
    .reset_index(drop=True)
)
#Turn "Count" into an integer
betastrep_count['Count'] = betastrep_count['Count'].astype(int)

betastrep_count


##FOR kleb##
#Pivot kleb to long format
kleb = kleb.melt(var_name="Antibiotic", value_name="Value")
#Drop the NaN values
kleb = kleb.dropna()
#Replace the I values for S
kleb.loc[kleb['Value'] == 'I', 'Value'] = 'S'

# Count the occurrences of "R" for each antibiotic
kleb_res_counts = kleb[kleb['Value'] == 'R']['Antibiotic'].value_counts()
#Count the ocurrences of "S" for each antibiotic
kleb_s_counts = kleb[kleb['Value'] == 'S']['Antibiotic'].value_counts()

# Calculate the relative frequency by dividing by the total count and multiplying by 100
kleb_total_count = kleb_res_counts + kleb_s_counts

kleb_relative_frequency = (kleb_res_counts / kleb_total_count) * 100
#Reset index
kleb_relative_frequency = kleb_relative_frequency.reset_index()
#Rename the columns to "Antibiotic" and "Count"
kleb_relative_frequency.columns = ["Antibiotic", "Count"]
# Print the relative frequency for each antibiotic
print(kleb_relative_frequency)

#Save the dataframe into kleb_count
kleb_count = kleb_relative_frequency

# Sort by count
kleb_count = kleb_count.sort_values(by=['Count'])

# Replace specific values in the "Antibiotic" column
kleb_count['Antibiotic'] = kleb_count['Antibiotic'].replace({
    'Naxcel': 'Ceftiofur',
    'Tribrissen ': 'Trimethoprim/Sulfamethoxazole',
    'Timentin ': 'Ticarcillin/Clavulanate',
    'Rifampin ': 'Rifampicin'
})

#Create a column named "Group"
kleb_count['Group'] = "Kleb"
# Replace the value in the "Group" column to "Cephalosporin" if the value in the "Antibiotic" column is equal to "Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "
kleb_count.loc[kleb_count['Antibiotic'].isin(["Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "]), "Group"] = "Cephalosporin"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Ampicillin ","Oxacillin ", "Ticarcillin ", "Ticarcillin/Clavulanate"]), "Group"] = "Penicillin"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Amikacin","Gentamicin ", "Neomycin "]), "Group"] = "Aminoglycoside"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Erythromycin ","Azithromycin "]), "Group"] = "Macrolide"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Enrofloxacin "]), "Group"] = "Fluoroquinolone"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Rifampicin"]), "Group"] = "Rifamicin"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Trimethoprim/Sulfamethoxazole"]), "Group"] = "Sulfonamide"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Tetracycline ","Doxycycline "]), "Group"] = "Tetracyclin"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Nitrofurantoin "]), "Group"] = "Nitrofuran"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Chloramphenicol "]), "Group"] = "Amphenicol"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Imipenem "]), "Group"] = "Carbapenem"
kleb_count.loc[kleb_count['Antibiotic'].isin(["Polymyxin B "]), "Group"] = "Polymyxin"

# Show the updated kleb_count dataframe
kleb_count

# Reorder the dataframe
kleb_count = (
    kleb_count
    .groupby(["Group"])
    .apply(lambda x: x.sort_values(["Count"], ascending = False))
    .reset_index(drop=True)
)
#Turn "Count" into an integer
kleb_count['Count'] = kleb_count['Count'].astype(int)


##FOR ecloacae##
#Pivot ecloacae to long format
ecloacae = ecloacae.melt(var_name="Antibiotic", value_name="Value")
#Drop the NaN values
ecloacae = ecloacae.dropna()
#Replace the I values for S
ecloacae.loc[ecloacae['Value'] == 'I', 'Value'] = 'S'

# Count the occurrences of "R" for each antibiotic
ecloacae_res_counts = ecloacae[ecloacae['Value'] == 'R']['Antibiotic'].value_counts()
#Count the ocurrences of "S" for each antibiotic
ecloacae_s_counts = ecloacae[ecloacae['Value'] == 'S']['Antibiotic'].value_counts()

# Calculate the relative frequency by dividing by the total count and multiplying by 100
ecloacae_total_count = ecloacae_res_counts + ecloacae_s_counts

ecloacae_relative_frequency = (ecloacae_res_counts / ecloacae_total_count) * 100
#Reset index
ecloacae_relative_frequency = ecloacae_relative_frequency.reset_index()
#Rename the columns to "Antibiotic" and "Count"
ecloacae_relative_frequency.columns = ["Antibiotic", "Count"]
# Print the relative frequency for each antibiotic
print(ecloacae_relative_frequency)

#Save the dataframe into ecloacae_count
ecloacae_count = ecloacae_relative_frequency


# Sort by count
ecloacae_count = ecloacae_count.sort_values(by=['Count'])
 
# Replace specific values in the "Antibiotic" column
ecloacae_count['Antibiotic'] = ecloacae_count['Antibiotic'].replace({
    'Naxcel': 'Ceftiofur',
    'Tribrissen ': 'Trimethoprim/Sulfamethoxazole',
    'Timentin ': 'Ticarcillin/Clavulanate',
    'Rifampin ': 'Rifampicin'
})

#Create a column named "Group"
ecloacae_count['Group'] = "Ecloacae"
# Replace the value in the "Group" column to "Cephalosporin" if the value in the "Antibiotic" column is equal to "Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Ceftiofur", "Cefuroxime ", "Ceftriaxone ", "Ceftazidime ", "Cefazolin "]), "Group"] = "Cephalosporin"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Ampicillin ","Oxacillin ", "Ticarcillin ", "Ticarcillin/Clavulanate"]), "Group"] = "Penicillin"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Amikacin","Gentamicin ", "Neomycin "]), "Group"] = "Aminoglycoside"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Erythromycin ","Azithromycin "]), "Group"] = "Macrolide"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Enrofloxacin "]), "Group"] = "Fluoroquinolone"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Rifampicin"]), "Group"] = "Rifamicin"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Trimethoprim/Sulfamethoxazole"]), "Group"] = "Sulfonamide"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Tetracycline ","Doxycycline "]), "Group"] = "Tetracyclin"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Nitrofurantoin "]), "Group"] = "Nitrofuran"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Chloramphenicol "]), "Group"] = "Amphenicol"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Imipenem "]), "Group"] = "Carbapenem"
ecloacae_count.loc[ecloacae_count['Antibiotic'].isin(["Polymyxin B "]), "Group"] = "Polymyxin"

# Show the updated ecloacae_count dataframe
ecloacae_count
# Reorder the dataframe
ecloacae_count = (
    ecloacae_count
    .groupby(["Group"])
    .apply(lambda x: x.sort_values(["Count"], ascending = False))
    .reset_index(drop=True)
)
#Turn "Count" into an integer
ecloacae_count['Count'] = ecloacae_count['Count'].astype(int)



        
##Prepare data for plotting ecoli##
# Grab the group values
ECOLIGROUP = ecoli_count["Group"].values
#Add padding
PAD = 3
ECOLIVALUES = ecoli_count["Count"].values
ECOLIANGLES_N = len(ECOLIVALUES) + PAD * len(np.unique(ECOLIGROUP))
ECOLIANGLES = np.linspace(0, 2 * np.pi, num=ECOLIANGLES_N, endpoint=False)
ECOLILABELS = ecoli_count["Antibiotic"].values
# Obtain size of each group
ECOLIGROUPS_SIZE = [len(i[1]) for i in ecoli_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
ECOLIWIDTH = (2 * np.pi) / len(ECOLIANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
ECOLIIDXS = []
for size in ECOLIGROUPS_SIZE:
    ECOLIIDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD
# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2



## Initialize Figure and Axis ##
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})

# Specify offset
ax.set_theta_offset(OFFSET)
# Set limits for radial (y) axis. The negative lower bound creates the hole in the middle.
ax.set_ylim(-100, 100)
# Remove all spines
ax.set_frame_on(False)
# Remove grid and tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_xticks([])
ax.set_yticks([])
# Use different colors for each group!
ECOLIGROUPS_SIZE = [len(i[1]) for i in ecoli_count.groupby("Group")]
ECOLICOLORS = [f"C{i}" for i, size in enumerate(ECOLIGROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    ECOLIANGLES[ECOLIIDXS], ECOLIVALUES, width=ECOLIWIDTH, color=ECOLICOLORS, 
    edgecolor="white", linewidth=2
)

add_labels(ECOLIANGLES[ECOLIIDXS], ECOLIVALUES, ECOLILABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], ECOLIGROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(ECOLIANGLES[offset + PAD], ECOLIANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    

    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["20%", "40%", "60%", "80%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(ECOLIANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD

# Show the plot
plt.show()
        
##Prepare data for plotting ecloacae##
# Grab the group values
ECLOACAEGROUP = ecloacae_count["Group"].values
#Add padding
PAD = 3
ECLOACAEVALUES = ecloacae_count["Count"].values
ECLOACAEANGLES_N = len(ECLOACAEVALUES) + PAD * len(np.unique(ECLOACAEGROUP))
ECLOACAEANGLES = np.linspace(0, 2 * np.pi, num=ECLOACAEANGLES_N, endpoint=False)
ECLOACAELABELS = ecloacae_count["Antibiotic"].values
# Obtain size of each group
ECLOACAEGROUPS_SIZE = [len(i[1]) for i in ecloacae_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
ECLOACAEWIDTH = (2 * np.pi) / len(ECLOACAEANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
ECLOACAEIDXS = []
for size in ECLOACAEGROUPS_SIZE:
    ECLOACAEIDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD
# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

## Initialize Figure and Axis ##
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})

# Specify offset
ax.set_theta_offset(OFFSET)
# Set limits for radial (y) axis. The negative lower bound creates the hole in the middle.
ax.set_ylim(-100, 100)
# Remove all spines
ax.set_frame_on(False)
# Remove grid and tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_xticks([])
ax.set_yticks([])
# Use different colors for each group!
ECLOACAEGROUPS_SIZE = [len(i[1]) for i in ecloacae_count.groupby("Group")]
ECLOACAECOLORS = [f"C{i}" for i, size in enumerate(ECLOACAEGROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    ECLOACAEANGLES[ECLOACAEIDXS], ECLOACAEVALUES, width=ECLOACAEWIDTH, color=ECLOACAECOLORS, 
    edgecolor="white", linewidth=2
)

add_labels(ECLOACAEANGLES[ECLOACAEIDXS], ECLOACAEVALUES, ECLOACAELABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], ECLOACAEGROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(ECLOACAEANGLES[offset + PAD], ECLOACAEANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    

    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["20%", "40%", "60%", "80%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(ECLOACAEANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD

# Show the plot
plt.show()
 
##Prepare data for plotting pagglom##
# Grab the group values
PAGGLOMGROUP = pagglom_count["Group"].values
#Add padding
PAD = 3
PAGGLOMVALUES = pagglom_count["Count"].values
PAGGLOMANGLES_N = len(PAGGLOMVALUES) + PAD * len(np.unique(PAGGLOMGROUP))
PAGGLOMANGLES = np.linspace(0, 2 * np.pi, num=PAGGLOMANGLES_N, endpoint=False)
PAGGLOMLABELS = pagglom_count["Antibiotic"].values
# Obtain size of each group
PAGGLOMGROUPS_SIZE = [len(i[1]) for i in pagglom_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
PAGGLOMWIDTH = (2 * np.pi) / len(PAGGLOMANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
PAGGLOMIDXS = []
for size in PAGGLOMGROUPS_SIZE:
    PAGGLOMIDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD
# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

## Initialize Figure and Axis ##
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})

# Specify offset
ax.set_theta_offset(OFFSET)
# Set limits for radial (y) axis. The negative lower bound creates the hole in the middle.
ax.set_ylim(-100, 100)
# Remove all spines
ax.set_frame_on(False)
# Remove grid and tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_xticks([])
ax.set_yticks([])
# Use different colors for each group!
PAGGLOMGROUPS_SIZE = [len(i[1]) for i in pagglom_count.groupby("Group")]
PAGGLOMCOLORS = [f"C{i}" for i, size in enumerate(PAGGLOMGROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    PAGGLOMANGLES[PAGGLOMIDXS], PAGGLOMVALUES, width=PAGGLOMWIDTH, color=PAGGLOMCOLORS, 
    edgecolor="white", linewidth=2
)

add_labels(PAGGLOMANGLES[PAGGLOMIDXS], PAGGLOMVALUES, PAGGLOMLABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], PAGGLOMGROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(PAGGLOMANGLES[offset + PAD], PAGGLOMANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    

    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["20%", "40%", "60%", "80%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(PAGGLOMANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD

# Show the plot
plt.show()

##Prepare data for plotting pmirabilis##
# Grab the group values
PMIRABILISGROUP = pmirabilis_count["Group"].values
#Add padding
PAD = 3
PMIRABILISVALUES = pmirabilis_count["Count"].values
PMIRABILISANGLES_N = len(PMIRABILISVALUES) + PAD * len(np.unique(PMIRABILISGROUP))
PMIRABILISANGLES = np.linspace(0, 2 * np.pi, num=PMIRABILISANGLES_N, endpoint=False)
PMIRABILISLABELS = pmirabilis_count["Antibiotic"].values
# Obtain size of each group
PMIRABILISGROUPS_SIZE = [len(i[1]) for i in pmirabilis_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
PMIRABILISWIDTH = (2 * np.pi) / len(PMIRABILISANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
PMIRABILISIDXS = []
for size in PMIRABILISGROUPS_SIZE:
    PMIRABILISIDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD
# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

## Initialize Figure and Axis ##
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})

# Specify offset
ax.set_theta_offset(OFFSET)
# Set limits for radial (y) axis. The negative lower bound creates the hole in the middle.
ax.set_ylim(-100, 100)
# Remove all spines
ax.set_frame_on(False)
# Remove grid and tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_xticks([])
ax.set_yticks([])
# Use different colors for each group!
PMIRABILISGROUPS_SIZE = [len(i[1]) for i in pmirabilis_count.groupby("Group")]
PMIRABILISCOLORS = [f"C{i}" for i, size in enumerate(PMIRABILISGROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    PMIRABILISANGLES[PMIRABILISIDXS], PMIRABILISVALUES, width=PMIRABILISWIDTH, color=PMIRABILISCOLORS, 
    edgecolor="white", linewidth=2
)

add_labels(PMIRABILISANGLES[PMIRABILISIDXS], PMIRABILISVALUES, PMIRABILISLABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], PMIRABILISGROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(PMIRABILISANGLES[offset + PAD], PMIRABILISANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    

    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["20%", "40%", "60%", "80%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(PMIRABILISANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD

# Show the plot
plt.show()



##Prepare data for plotting pvulgaris##
# Grab the group values
PVULGARISGROUP = pvulgaris_count["Group"].values
#Add padding
PAD = 3
PVULGARISVALUES = pvulgaris_count["Count"].values
PVULGARISANGLES_N = len(PVULGARISVALUES) + PAD * len(np.unique(PVULGARISGROUP))
PVULGARISANGLES = np.linspace(0, 2 * np.pi, num=PVULGARISANGLES_N, endpoint=False)
PVULGARISLABELS = pvulgaris_count["Antibiotic"].values
# Obtain size of each group
PVULGARISGROUPS_SIZE = [len(i[1]) for i in pvulgaris_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
PVULGARISWIDTH = (2 * np.pi) / len(PVULGARISANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
PVULGARISIDXS = []
for size in PVULGARISGROUPS_SIZE:
    PVULGARISIDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD
# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

## Initialize Figure and Axis ##
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})

# Specify offset
ax.set_theta_offset(OFFSET)
# Set limits for radial (y) axis. The negative lower bound creates the hole in the middle.
ax.set_ylim(-100, 100)
# Remove all spines
ax.set_frame_on(False)
# Remove grid and tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_xticks([])
ax.set_yticks([])
# Use different colors for each group!
PVULGARISGROUPS_SIZE = [len(i[1]) for i in pvulgaris_count.groupby("Group")]
PVULGARISCOLORS = [f"C{i}" for i, size in enumerate(PVULGARISGROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    PVULGARISANGLES[PVULGARISIDXS], PVULGARISVALUES, width=PVULGARISWIDTH, color=PVULGARISCOLORS, 
    edgecolor="white", linewidth=2
)

add_labels(PVULGARISANGLES[PVULGARISIDXS], PVULGARISVALUES, PVULGARISLABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], PVULGARISGROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(PVULGARISANGLES[offset + PAD], PVULGARISANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    

    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["20%", "40%", "60%", "80%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(PVULGARISANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD

# Show the plot
plt.show()


##Prepare data for plotting kleb##
# Grab the group values
KLEBGROUP = kleb_count["Group"].values
#Add padding
PAD = 3
KLEBVALUES = kleb_count["Count"].values
KLEBANGLES_N = len(KLEBVALUES) + PAD * len(np.unique(KLEBGROUP))
KLEBANGLES = np.linspace(0, 2 * np.pi, num=KLEBANGLES_N, endpoint=False)
KLEBLABELS = kleb_count["Antibiotic"].values
# Obtain size of each group
KLEBGROUPS_SIZE = [len(i[1]) for i in kleb_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
KLEBWIDTH = (2 * np.pi) / len(KLEBANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
KLEBIDXS = []
for size in KLEBGROUPS_SIZE:
    KLEBIDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD
# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

## Initialize Figure and Axis ##
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})

# Specify offset
ax.set_theta_offset(OFFSET)
# Set limits for radial (y) axis. The negative lower bound creates the hole in the middle.
ax.set_ylim(-100, 100)
# Remove all spines
ax.set_frame_on(False)
# Remove grid and tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_xticks([])
ax.set_yticks([])
# Use different colors for each group!
KLEBGROUPS_SIZE = [len(i[1]) for i in kleb_count.groupby("Group")]
KLEBCOLORS = [f"C{i}" for i, size in enumerate(KLEBGROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    KLEBANGLES[KLEBIDXS], KLEBVALUES, width=KLEBWIDTH, color=KLEBCOLORS, 
    edgecolor="white", linewidth=2
)

add_labels(KLEBANGLES[KLEBIDXS], KLEBVALUES, KLEBLABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], KLEBGROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(KLEBANGLES[offset + PAD], KLEBANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    

    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["20%", "40%", "60%", "80%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(KLEBANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD
#Export the plot
plt.savefig('kleb.png', dpi=300, bbox_inches='tight')
# Show the plot
plt.show()


##Prepare data for plotting alphastrep##
# Grab the group values
ALPHASTREPGROUP = alphastrep_count["Group"].values
#Add padding
PAD = 3
ALPHASTREPVALUES = alphastrep_count["Count"].values
ALPHASTREPANGLES_N = len(ALPHASTREPVALUES) + PAD * len(np.unique(ALPHASTREPGROUP))
ALPHASTREPANGLES = np.linspace(0, 2 * np.pi, num=ALPHASTREPANGLES_N, endpoint=False)
ALPHASTREPLABELS = alphastrep_count["Antibiotic"].values
# Obtain size of each group
ALPHASTREPGROUPS_SIZE = [len(i[1]) for i in alphastrep_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
ALPHASTREPWIDTH = (2 * np.pi) / len(ALPHASTREPANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
ALPHASTREPIDXS = []
for size in ALPHASTREPGROUPS_SIZE:
    ALPHASTREPIDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD
# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

## Initialize Figure and Axis ##
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})

# Specify offset
ax.set_theta_offset(OFFSET)
# Set limits for radial (y) axis. The negative lower bound creates the hole in the middle.
ax.set_ylim(-100, 100)
# Remove all spines
ax.set_frame_on(False)
# Remove grid and tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_xticks([])
ax.set_yticks([])
# Use different colors for each group!
ALPHASTREPGROUPS_SIZE = [len(i[1]) for i in alphastrep_count.groupby("Group")]
ALPHASTREPCOLORS = [f"C{i}" for i, size in enumerate(ALPHASTREPGROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    ALPHASTREPANGLES[ALPHASTREPIDXS], ALPHASTREPVALUES, width=ALPHASTREPWIDTH, color=ALPHASTREPCOLORS, 
    edgecolor="white", linewidth=2
)

add_labels(ALPHASTREPANGLES[ALPHASTREPIDXS], ALPHASTREPVALUES, ALPHASTREPLABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"], ALPHASTREPGROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(ALPHASTREPANGLES[offset + PAD], ALPHASTREPANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    

    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["20%", "40%", "60%", "80%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(ALPHASTREPANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD

# Show the plot
plt.show()


##Prepare data for plotting betastrep##
# Grab the group values
BETASTREPGROUP = betastrep_count["Group"].values
#Add padding
PAD = 3
BETASTREPVALUES = betastrep_count["Count"].values
BETASTREPANGLES_N = len(BETASTREPVALUES) + PAD * len(np.unique(BETASTREPGROUP))
BETASTREPANGLES = np.linspace(0, 2 * np.pi, num=BETASTREPANGLES_N, endpoint=False)
BETASTREPLABELS = betastrep_count["Antibiotic"].values
# Obtain size of each group
BETASTREPGROUPS_SIZE = [len(i[1]) for i in betastrep_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
BETASTREPWIDTH = (2 * np.pi) / len(BETASTREPANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
BETASTREPIDXS = []
for size in BETASTREPGROUPS_SIZE:
    BETASTREPIDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD
# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

## Initialize Figure and Axis ##
fig, ax = plt.subplots(figsize=(20, 20), subplot_kw={"projection": "polar"})

# Specify offset
ax.set_theta_offset(OFFSET)
# Set limits for radial (y) axis. The negative lower bound creates the hole in the middle.
ax.set_ylim(-100, 100)
# Remove all spines
ax.set_frame_on(False)
# Remove grid and tick marks
ax.xaxis.grid(False)
ax.yaxis.grid(False)
ax.set_xticks([])
ax.set_yticks([])
# Use different colors for each group!
BETASTREPGROUPS_SIZE = [len(i[1]) for i in betastrep_count.groupby("Group")]
BETASTREPCOLORS = [f"C{i}" for i, size in enumerate(BETASTREPGROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    BETASTREPANGLES[BETASTREPIDXS], BETASTREPVALUES, width=BETASTREPWIDTH, color=BETASTREPCOLORS, 
    edgecolor="white", linewidth=2
)

add_labels(BETASTREPANGLES[BETASTREPIDXS], BETASTREPVALUES, BETASTREPLABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"], BETASTREPGROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(BETASTREPANGLES[offset + PAD], BETASTREPANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    

    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["20%", "40%", "60%", "80%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(BETASTREPANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD

# Show the plot
plt.show()
