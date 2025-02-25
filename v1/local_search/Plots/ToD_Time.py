import json
import matplotlib.pyplot as plt
import numpy as np
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "plot_data.json")

def tod_time_line_plot():
    with open(file_path, "r") as file:
        data = json.load(file)
    
    tod_values = [list(map(int, entry["ToD"].split(", "))) for entry in data]

    avg_tod = np.mean(tod_values, axis=0)
    
    x_values = range(1, 25)
    plt.figure(figsize=(10, 5))
    plt.plot(x_values, avg_tod[24::], marker='o', linestyle='-', color='b', label='ToD')
    plt.xlabel("Time")
    plt.ylabel("ToD")

    plt.legend()
    plt.grid(True)
    plt.show()
