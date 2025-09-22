import json
import os
from itertools import product
from scipy.stats import f_oneway
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# -------------------------------
# Configurations
# -------------------------------
data_folder_path = "v2/simulation_center/data/batch_time"
output_folder = "v2/simulation_center/results"
os.makedirs(output_folder, exist_ok=True)

algorithms = ["branch_and_bound", "genetic", "local_search", "nearest_lot", "hybrid"]
batch_times = [60, 30, 10]
distributions = ["UNIFORM", "NORMAL", "EXPONENTIAL"]

# -------------------------------
# Helper functions
# -------------------------------
def load_tod(path):
    """Load ToD array from a JSON file and convert to integers."""
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return []
    with open(path, 'r') as f:
        data = json.load(f)
        tod_values = []
        for sim in data:
            tod_str = sim["ToD"]
            tod_list = [int(x.strip()) for x in tod_str.split(",")]
            tod_values.extend(tod_list)
        return tod_values

# -------------------------------
# Load all data into categories
# -------------------------------
category_data = {}  # {(batch_time, distribution): {algorithm: ToD list}}

for batch_time, distribution in product(batch_times, distributions):
    category_key = (batch_time, distribution)
    category_data[category_key] = {}
    
    for alg in algorithms:
        file_path = os.path.join(data_folder_path, str(batch_time), distribution, f"{alg}.json")
        tod_list = load_tod(file_path)
        category_data[category_key][alg] = tod_list

# -------------------------------
# Perform ANOVA
# -------------------------------
anova_results = []

for category, alg_data in category_data.items():
    tod_lists = [alg_data[alg] for alg in algorithms if alg_data[alg]]
    
    if len(tod_lists) < 2:
        print(f"Skipping category {category}, not enough data.")
        continue
    
    F_stat, p_val = f_oneway(*tod_lists)
    anova_results.append({
        "batch_time": category[0],
        "distribution": category[1],
        "F_stat": F_stat,
        "p_value": p_val
    })

anova_df = pd.DataFrame(anova_results)
anova_csv_path = os.path.join(output_folder, "anova_results.csv")
anova_df.to_csv(anova_csv_path, index=False)
print(f"ANOVA results saved to {anova_csv_path}")

# -------------------------------
# Perform Tukey HSD and store results
# -------------------------------
all_tukey_results = []

for category, alg_data in category_data.items():
    tod_lists = [alg_data[alg] for alg in algorithms if alg_data[alg]]
    if len(tod_lists) < 2:
        continue

    # Prepare long-format DataFrame
    df = pd.DataFrame({
        "ToD": [value for alg_list in tod_lists for value in alg_list],
        "Algorithm": [alg for alg, alg_list in zip(algorithms, tod_lists) for _ in alg_list]
    })

    tukey = pairwise_tukeyhsd(df["ToD"], df["Algorithm"], alpha=0.05)
    tukey_df = pd.DataFrame(data=tukey._results_table.data[1:], columns=tukey._results_table.data[0])
    tukey_df["batch_time"] = category[0]
    tukey_df["distribution"] = category[1]
    all_tukey_results.append(tukey_df)

if all_tukey_results:
    tukey_results_df = pd.concat(all_tukey_results, ignore_index=True)
    tukey_csv_path = os.path.join(output_folder, "tukey_results.csv")
    tukey_results_df.to_csv(tukey_csv_path, index=False)
    print(f"Tukey HSD results saved to {tukey_csv_path}")
