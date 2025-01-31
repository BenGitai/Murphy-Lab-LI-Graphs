### Import Statements ###
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------

# Worm class initialization
class worm:
    def __init__(self, strain, time, cI):
        self.strain = strain
        self.time = time
        self.cI = cI

# ----------------------------------------------

# Get file location/name
file = input("File Location: ")

# Load CSV as dataframe

df = pd.read_csv('KN_Example_STAM_01.29.2025.csv') # Change string to csv file location

# path needed if the file has a different local path

df = df.dropna(how='all')

# ---------------------------------------------

# Covert dataframe into list of worm objects

worms = []

for index, row in df.iterrows():
    if (row["Strain"] != "Strain"):
        strain = row["Strain"]
        time = row["Time"]
        rep = row["Replicate"]
        size = row["Est. Worm Size"]
        eth = int(row["Eth"])
        but = int(row["But"])
        ori = int(row["Ori"])
        tot = int(row["Tot"])

        # Calculate CI value (cI used as CI is constant index)
        cI = (but - eth) / (tot - ori)

        # New worm created and added to list
        newWorm = worm(strain, time, cI)

        worms.append(newWorm)

# ----------------------------------------------

# Average worms of same strain and time step

oldStrain = worms[0].strain
oldTime = worms[0].time
totCI = 0
strainCount = 1

# Create list of new worms
avgWorms = []

for Worm in worms:
    if (oldStrain == Worm.strain) and (oldTime == Worm.time):
        totCI += Worm.cI
        strainCount += 1
    else:
        #print(Worm.strain)
        
        avgCI = totCI / strainCount
        newWorm = worm(oldStrain, oldTime, avgCI)
        #print(newWorm.strain)
        avgWorms.append(newWorm)
        totCI = 0
        strainCount = 1

        oldStrain = Worm.strain
        oldTime = Worm.time

# --------------------------------------------------

# Convert list of average worms into a cleaned dataframe

import pandas as pd

dfWorms = pd.DataFrame([vars(avgWorm) for avgWorm in avgWorms])

# --------------------------------------------------

# Create a new dataframe based on the newly cleaned 
# dataframe for the LI values instead of the CI values

strains = []
strainsN = []
for index, row in dfWorms[dfWorms["time"] == "N"].iterrows():
    strain = row["strain"]
    ci_n = row["cI"]
    #print(strain, ci_n)
    strains.append(strain)
    strainsN.append(ci_n)

ci_n_dict = dict(zip(strains, strainsN))

# Make a copy of the DataFrame
df_li = dfWorms.copy()

# Subtract the respective CI_N value from each row's CI value
df_li["LI"] = df_li["cI"] - df_li["strain"].map(ci_n_dict)

# Remove the CI column
df_li = df_li.drop(columns=["cI"])

# Remove rows where time is "N"
df_li = df_li[df_li["time"] != "N"]

# ------------------------------------------------

# Reorginize the dataframes to prevent errors when graphing due to missing data

# Count occurrences of each strain and sort by frequency (highest first)
strain_counts = dfWorms["strain"].value_counts()
sorted_strains = strain_counts.index.tolist()  # List of strains in descending order of frequency

# Function to sort by time while keeping "N" first
def sort_by_time(df):
    df["time"] = pd.Categorical(df["time"], categories=sorted(df["time"].unique(), key=lambda x: (x != "N", float(x) if x != "N" else -1)), ordered=True)
    return df.sort_values(["strain", "time"])

# Apply strain order to dfWorms
dfWorms_sorted = dfWorms.copy()
dfWorms_sorted["strain"] = pd.Categorical(dfWorms_sorted["strain"], categories=sorted_strains, ordered=True)
dfWorms_sorted = sort_by_time(dfWorms_sorted)

# Apply strain order to df_li
df_li_sorted = df_li.copy()
df_li_sorted["strain"] = pd.Categorical(df_li_sorted["strain"], categories=sorted_strains, ordered=True)
df_li_sorted = sort_by_time(df_li_sorted)

# Display the reorganized DataFrames
print(dfWorms_sorted)
print(df_li_sorted)

# ------------------------------------------------

# Plot and display the 2 new dataframes

# Set Seaborn style
sns.set_style("whitegrid")

# Create subplots (1 row, 2 columns)
fig, axes = plt.subplots(1, 2, figsize=(14, 6))  # 14 inches wide, 6 inches high

### --- First Plot: CI Values --- ###
for strain, group in dfWorms.groupby("strain"):
    axes[0].plot(group["time"], group["cI"], marker="o", linestyle="-", label=strain)

# Labels and title for CI plot
axes[0].set_xlabel("Time")
axes[0].set_ylabel("CI Value")
axes[0].set_title("CI Value Over Time by Strain")
axes[0].legend(title="Strain")

### --- Second Plot: LI Values --- ###
for strain, group in df_li.groupby("strain"):
    axes[1].plot(group["time"], group["LI"], marker="o", linestyle="-", label=strain)

# Labels and title for LI plot
axes[1].set_xlabel("Time")
axes[1].set_ylabel("LI Value")
axes[1].set_title("LI Value Over Time by Strain")
axes[1].legend(title="Strain")

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plots
plt.show()