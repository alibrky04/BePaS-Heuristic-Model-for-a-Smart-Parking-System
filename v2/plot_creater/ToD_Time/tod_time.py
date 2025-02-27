import os
import json
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

def plot_tod_time():
    folder_path = Path("v2/plot_creater/ToD_Time/data")

    data_dict = {}
    for model_folder in folder_path.iterdir():
        if model_folder.is_dir():
            model_name = model_folder.name

            for json_file in model_folder.glob("*.json"):
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if isinstance(data, list):
                    tod_values_by_index = []

                    for entry in data:
                        tod_values = list(map(int, entry["ToD"].split(", ")))
                        if not tod_values_by_index:
                            tod_values_by_index = [[] for _ in range(len(tod_values))]

                        for idx, value in enumerate(tod_values):
                            tod_values_by_index[idx].append(value)

                    batch_size = int(data[0]["car_batch_size"])

                else:
                    tod_values = list(map(int, data["ToD"].split(",")))
                    tod_values_by_index = [[] for _ in range(len(tod_values))]

                    for idx, value in enumerate(tod_values):
                        tod_values_by_index[idx].append(value)

                    batch_size = int(data["car_batch_size"])

                avg_tod_values = [np.mean(values) / 2 for values in tod_values_by_index]

                if batch_size not in data_dict:
                    data_dict[batch_size] = {}

                if model_name not in data_dict[batch_size]:
                    data_dict[batch_size][model_name] = []

                data_dict[batch_size][model_name].append(avg_tod_values)

    selected_batch_sizes = sorted(data_dict.keys())[:3]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

    for i, batch_size in enumerate(selected_batch_sizes):
        ax = axes[i]
        for model_name, avg_tod_lists in data_dict[batch_size].items():
            avg_tod_per_index = np.mean(avg_tod_lists, axis=0)
            
            x_values = np.arange(1, len(avg_tod_per_index) + 1)

            if model_name == "nearest_lot_model":
                y_values = avg_tod_per_index[:batch_size]
                ax.plot(x_values[:batch_size], y_values, label=model_name, marker='o')
            else:
                middle_index = len(avg_tod_per_index) // 2
                y_values = avg_tod_per_index[middle_index:]
                ax.plot(x_values[middle_index:], y_values, label=model_name, marker='o')

        ax.set_xlabel("Batch Size")
        ax.set_ylabel("ToD")
        ax.legend()

    plt.tight_layout()
    plt.show()

plot_tod_time()