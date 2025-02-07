### Import Statements ###
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# -----------------------------------------------

# Worm class initialization
class worm:
    def __init__(self, strain, time, cI):
        self.strain = strain
        self.time = time
        self.cI = cI

# ----------------------------------------------

# Get the single file path from user
file = input("Enter the path of the CSV file: ")

# Check if file exists
if not os.path.isfile(file):
    print("Error: File not found!")
    exit()

print(f"\nProcessing file: {file}")

try:
    # Load CSV as dataframe
    df = pd.read_csv(file)
    df = df.dropna(how='all')

    # ---------------------------------------------

    # Convert dataframe into list of worm objects
    worms = []
    for index, row in df.iterrows():
        if row["Strain"] != "Strain":  # Avoid header issues
            strain = row["Strain"]
            time = row["Time"]

            # Convert specific time values
            if time == "30":
                time = "0.5"
            elif time == "60":
                time = "1"

            # Handle missing columns
            eth = float(row["Eth"]) if "Eth" in df.columns else 0
            but = float(row["But"]) if "But" in df.columns else 0
            ori = float(row["Ori"]) if "Ori" in df.columns else 0
            tot = float(row["Tot"]) if "Tot" in df.columns else 1  # Avoid division by zero

            # Calculate CI value
            if tot - ori != 0:
                cI = (but - eth) / (tot - ori)
            else:
                cI = 0  # Default CI value if invalid
                print("CI Error")

            # New worm created and added to list
            worms.append(worm(strain, time, cI))

    # ----------------------------------------------

    # Compute means and standard error for CI values
    dfWorms = pd.DataFrame([vars(w) for w in worms])

    dfWorms_summary = dfWorms.groupby(["strain", "time"]).agg(
        mean_cI=("cI", "mean"),
        se_cI=("cI", lambda x: np.std(x) / np.sqrt(len(x)))  # Standard error calculation
    ).reset_index()

    # ----------------------------------------------

    # Create LI DataFrame
    strains = dfWorms[dfWorms["time"] == "N"]["strain"].tolist()
    strainsN = dfWorms[dfWorms["time"] == "N"]["cI"].tolist()
    ci_n_dict = dict(zip(strains, strainsN))

    df_li = dfWorms.copy()
    df_li["LI"] = df_li["cI"] - df_li["strain"].map(ci_n_dict)
    df_li = df_li.drop(columns=["cI"])
    df_li = df_li[df_li["time"] != "N"]

    # Compute means and standard error for LI values
    df_li_summary = df_li.groupby(["strain", "time"]).agg(
        mean_LI=("LI", "mean"),
        se_LI=("LI", lambda x: np.std(x) / np.sqrt(len(x)))  # Standard error calculation
    ).reset_index()

    # --------------------------------------------

    # Reorganize DataFrames
    strain_counts = dfWorms["strain"].value_counts()
    sorted_strains = strain_counts.index.tolist()

    def sort_by_time(df):
        df["time"] = pd.Categorical(df["time"], categories=sorted(df["time"].unique(), key=lambda x: (x != "N", float(x) if x != "N" else -1)), ordered=True)
        return df.sort_values(["strain", "time"])

    dfWorms_summary["strain"] = pd.Categorical(dfWorms_summary["strain"], categories=sorted_strains, ordered=True)
    dfWorms_sorted = sort_by_time(dfWorms_summary)

    df_li_summary["strain"] = pd.Categorical(df_li_summary["strain"], categories=sorted_strains, ordered=True)
    df_li_sorted = sort_by_time(df_li_summary)

    # --------------------------------------------

    # Set Seaborn style
    sns.set_style("whitegrid")

    # Create subplots (1 row, 2 columns)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))  

    ### --- First Plot: CI Values with Error Bars --- ###
    for strain, group in dfWorms_sorted.groupby("strain", observed=False):
        axes[0].errorbar(group["time"], group["mean_cI"], yerr=group["se_cI"], marker="o", linestyle="-", label=strain, capsize=5)

    axes[0].set_xlabel("Time")
    axes[0].set_ylabel("CI Value")
    axes[0].set_title("CI Value Over Time by Strain")
    axes[0].legend(title="Strain")

    ### --- Second Plot: LI Values with Error Bars --- ###
    for strain, group in df_li_sorted.groupby("strain", observed=False):
        axes[1].errorbar(group["time"], group["mean_LI"], yerr=group["se_LI"], marker="o", linestyle="-", label=strain, capsize=5)

    axes[1].set_xlabel("Time")
    axes[1].set_ylabel("LI Value")
    axes[1].set_title("LI Value Over Time by Strain")
    axes[1].legend(title="Strain")

    plt.tight_layout()

    save_path = file.replace(".csv", ".png")

        # Ensure the directory exists
        #os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the plot
    plt.savefig(save_path)
    # Show the plots
    plt.show()

    # --------------------------------------------

except Exception as e:
    print(f"Error processing {file}: {e}")
