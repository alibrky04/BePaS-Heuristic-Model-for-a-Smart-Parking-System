import matplotlib.pyplot as plt
import numpy as np
import os
import json
import seaborn as sns
import pandas as pd

class plot_creater():
	def __init__(self):
		self.data_folder_path = "v2/simulation_center/data"

	def batch_time_plot(self):
		batch_time_folder = f"{self.data_folder_path}/batch_time"

		batch_times = ["60", "30", "10"]
		distributions = ["UNIFORM", "NORMAL", "EXPONENTIAL"]
		models = ["hybrid", "branch_and_bound", "genetic", "local_search", "nearest_lot"]

		data = {dist: {bt: {model: [] for model in models} for bt in batch_times} for dist in distributions}

		for batch_time in batch_times:
			for distribution in distributions:
				path = os.path.join(batch_time_folder, batch_time, distribution)
				for file in os.listdir(path):
					if file.endswith(".json"):
						model_name = file.replace(".json", "")
						if model_name in models:
							with open(os.path.join(path, file), "r") as f:
								simulations = json.load(f)

							all_tod_lists = []
							for sim in simulations:
								tod_list = list(map(int, sim["ToD"].split(", ")))
								tod_list = tod_list[len(tod_list) // 2:]
								all_tod_lists.append(tod_list)

							all_tod_lists = np.array(all_tod_lists)
							avg_tod = np.mean(all_tod_lists, axis=0)

							data[distribution][batch_time][model_name] = avg_tod

		for distribution in distributions:
			for batch_time in batch_times:
				plt.figure(figsize=(8, 5))
				plt.xlabel("Time (Hour)", fontsize=20)
				plt.ylabel("ToD", fontsize=20)

				for model in models:
					values = data[distribution][batch_time][model]
					if len(values) > 0:
						time_axis = np.linspace(0, 24, len(values))
						plt.plot(time_axis, values, marker='o', label=model)

				# TODO:	
				plt.xticks(np.arange(0, 25, 2), fontsize=18)
				plt.yticks(fontsize=18)
				plt.ylim(0, 2700)
				# plt.legend(fontsize=16, loc="upper left", bbox_to_anchor=(0, 0.85))
				plt.grid(linewidth=0.75)
				plt.tight_layout()
				plt.show()
		
	def time_limit_plot(self):
		pass

	def heatmap_plot(self, anova_csv_path="v2/simulation_center/results/anova_results.csv"):
		"""
		Plots a heatmap of ANOVA F-statistics for batch_time vs distribution.
		"""
		# Load CSV
		anova_df = pd.read_csv(anova_csv_path)

		# Pivot for heatmap
		heatmap_data = anova_df.pivot(index='batch_time', columns='distribution', values='F_stat')

		# Plot
		plt.figure(figsize=(8, 6))
		sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", annot_kws={"weight": "bold", "fontsize":12})
		plt.xlabel("Distribution", fontsize=14, fontweight="bold")
		plt.ylabel("Batch Time (min)", fontsize=14, fontweight="bold")
		plt.xticks(fontsize=14, fontweight="bold")
		plt.yticks(fontsize=14, fontweight="bold")
		plt.tight_layout()
		plt.show()
	
	def tukey_heatmap_plot(self, tukey_csv_path="v2/simulation_center/results/tukey_results.csv"):
		"""
		Plots a heatmap of Tukey HSD mean differences between heuristic models.
		Cells are colored by mean difference, and significant differences are highlighted.
		"""
		# Load CSV
		tukey_df = pd.read_csv(tukey_csv_path)

		batch_times = tukey_df['batch_time'].unique()
		distributions = tukey_df['distribution'].unique()
		models = sorted(list(set(tukey_df['group1']).union(set(tukey_df['group2']))))

		for batch_time in batch_times:
			for distribution in distributions:
				# Filter for specific batch time and distribution
				subset = tukey_df[(tukey_df['batch_time'] == batch_time) & 
								(tukey_df['distribution'] == distribution)]

				# Create an empty matrix
				heatmap_data = pd.DataFrame(0, index=models, columns=models, dtype=float)

				for _, row in subset.iterrows():
					heatmap_data.loc[row['group1'], row['group2']] = row['meandiff']
					heatmap_data.loc[row['group2'], row['group1']] = row['meandiff']  # symmetric

				# Mask the diagonal
				mask = np.eye(len(models), dtype=bool)

				plt.figure(figsize=(8, 6))
				sns.heatmap(
					heatmap_data,
					annot=True,
					fmt=".1f",
					cmap="RdBu_r",
					center=0,
					mask=mask,
					annot_kws={"weight": "bold", "fontsize": 12}  # Bold annotations
				)

				plt.xlabel("Model", fontsize=14, fontweight="bold")
				plt.ylabel("Model", fontsize=14, fontweight="bold")
				plt.xticks(fontsize=12, fontweight="bold")
				plt.yticks(fontsize=12, fontweight="bold")
				plt.tight_layout()
				plt.show()

pt = plot_creater()
pt.tukey_heatmap_plot()