import matplotlib.pyplot as plt
import numpy as np
import os
import json

class plot_creater():
	def __init__(self):
		self.data_folder_path = "v2/simulation_center/data"

	def batch_time_plot(self):
		batch_time_folder = f"{self.data_folder_path}/batch_time"

		batch_times = ["60", "30", "10"]
		distributions = ["UNIFORM", "NORMAL", "EXPONENTIAL"]
		models = ["branch_and_bound", "genetic", "local_search", "nearest_lot"]

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
			fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

			for i, batch_time in enumerate(batch_times):
				ax = axes[i]
				ax.set_xlabel("Batch")
				ax.set_ylabel("ToD")

				for model in models:
					if len(data[distribution][batch_time][model]) > 0:
						ax.plot(data[distribution][batch_time][model], label=model)

				ax.legend()

			plt.tight_layout()
			plt.subplots_adjust(top=0.85)
			plt.show()
			
plot_creater().batch_time_plot()