import json

from v1.branch_and_bound.Constants import *


def simulation_stat_out(ToD, num_of_jobs, simulation_file):
    try:
        ToD_str = ', '.join(map(str, ToD))

        try:
            simulation_file.seek(0)
            existing_data = json.load(simulation_file)
        except json.JSONDecodeError:
            existing_data = []

        simulation_id = len(existing_data) + 1

        if SIMULATION_DISTRIBUTION == "UNIFORM":
            simulation_distribution = "uniform"
        elif SIMULATION_DISTRIBUTION == "NORMAL":
            simulation_distribution = "normal"
        elif SIMULATION_DISTRIBUTION == "EXPONENTIAL":
            simulation_distribution = "exponential"
        elif SIMULATION_DISTRIBUTION == "STATIC":
            simulation_distribution = "static"

        existing_data.append({
            "simulation_id": simulation_id,
            "simulation_distribution": simulation_distribution,
            "ToD": ToD_str,
            "car_batch_size": NUMBER_OF_ROUNDS/2,
            "num_of_machines": NUMBER_OF_MACHINES,
            "num_of_jobs": num_of_jobs,
            "min_processing_time": MINIMUM_JOB_LENGTH,
            "max_processing_time": MAXIMUM_JOB_LENGTH,
            "mean": MEAN,
            "deviation": DEVIATION,
            "scale": SCALE
        })

        # Write back to file
        simulation_file.seek(0)
        json.dump(existing_data, simulation_file, indent=4)
        simulation_file.truncate()
    except Exception as e:
        print(f"Error writing to simulation file: {e}")