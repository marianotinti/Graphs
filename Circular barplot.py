# Import all necessary libraries for data processing and visualization
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

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
#For ecoli, perform a count for each value that appears in each column
ecoli_count = ecoli.apply(pd.Series.value_counts)


# Drop rows named "I" and "S" from ecoli_count dataframe
ecoli_count = ecoli_count.drop(["I","S"])

# Pivot the data to long format
ecoli_count = ecoli_count.melt(var_name="Antibiotic", value_name="Count")

# Drop the NaN values
ecoli_count = ecoli_count.dropna()

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
#Add a column named "RCount" with the values of the relative frequencies of the "Count" column
ecoli_count['RCount'] = ecoli_count['Count']/ecoli_count['Count'].sum()
#Multiply the RCount column by 100
ecoli_count['RCount'] = ecoli_count['RCount']*1000
#Show the updated ecoli_count dataframe
ecoli_count
#Turn the "Count" column into an integer
ecoli_count['Count'] = ecoli_count['Count'].astype(int)
#Order the dataframe by the "Group" column
ecoli_count = ecoli_count.sort_values(by=['Group'])


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
# Grab the group values
GROUP = ecoli_count["Group"].values
#Add padding
PAD = 3
VALUES = ecoli_count["RCount"].values
ANGLES_N = len(VALUES) + PAD * len(np.unique(GROUP))
ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)
LABELS = ecoli_count["Antibiotic"].values
# Obtain size of each group
GROUPS_SIZE = [len(i[1]) for i in ecoli_count.groupby("Group")]

# Determine the width of each bar. 
# The circumference is '2 * pi', so we divide that total width over the number of bars.
WIDTH = (2 * np.pi) / len(ANGLES)
# Obtaining the right indexes is now a little more complicated
offset = 0
IDXS = []
for size in GROUPS_SIZE:
    IDXS += list(range(offset + PAD, offset + size + PAD))
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
GROUPS_SIZE = [len(i[1]) for i in ecoli_count.groupby("Group")]
COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]
# Add bars, subsetting angles to use only those that correspond to non-empty bars
ax.bar(
    ANGLES[IDXS], VALUES, width=WIDTH, color=COLORS, 
    edgecolor="white", linewidth=2
)

add_labels(ANGLES[IDXS], VALUES, LABELS, OFFSET, ax)

#Add group labels
offset = 0 
for group, size in zip(["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"], GROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(ANGLES[offset + PAD], ANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -20, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    
    # Add reference lines at 20, 40, 60, and 80
    x2 = np.linspace(ANGLES[offset], ANGLES[offset + PAD - 1], num=50)
    ax.plot(x2, [20] * 50, color="#bebebe", lw=0.8,)
    ax.plot(x2, [40] * 50, color="#bebebe", lw=0.8)
    ax.plot(x2, [60] * 50, color="#bebebe", lw=0.8)
    ax.plot(x2, [80] * 50, color="#bebebe", lw=0.8)
    #Add reference text to indicate the value of the reference lines for each of the previous lines
    reference_values = [20, 40, 60, 80]
    reference_texts = ["2%", "4%", "6%", "8%"]

    for value, text in zip(reference_values, reference_texts):
        ax.text(ANGLES[offset+1], value, text, color="#bebebe", fontsize=14, 
                fontweight="bold", ha="center", va="center")

    offset += size + PAD

# Show the plot
plt.show()