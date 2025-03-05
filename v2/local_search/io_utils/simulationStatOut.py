from v2.local_search import Constants as cnst

import json

def simulationStatOut(ToD, num_of_machines, num_of_jobs, min_processing_time, max_processing_time, simulation_file):
    try:
        ToD_str = ', '.join(map(str, ToD))
        
        try:
            simulation_file.seek(0)
            existing_data = json.load(simulation_file)
        except json.JSONDecodeError:
            existing_data = []

        simulation_id = len(existing_data) + 1

        if cnst.SIMULATION_DISTRIBUTION == "UNIFORM":
            simulation_distribution = "uniform"
        elif cnst.SIMULATION_DISTRIBUTION == "NORMAL":
            simulation_distribution = "normal"
        elif cnst.SIMULATION_DISTRIBUTION == "EXPONENTIAL":
            simulation_distribution = "exponential"
        elif cnst.SIMULATION_DISTRIBUTION == "STATIC":
            simulation_distribution = "static"

        existing_data.append({
            "simulation_id": simulation_id,
            "simulation_distribution": simulation_distribution,
            "ToD": ToD_str,
            "car_batch_size": cnst.MAX_ROUNDS/2,
            "num_of_machines": num_of_machines,
            "num_of_jobs": num_of_jobs,
            "min_processing_time": min_processing_time,
            "max_processing_time": max_processing_time,
            "mean": cnst.MEAN,
            "deviation": cnst.DEVIATION,
            "scale": cnst.SCALE
        })

        simulation_file.seek(0)
        json.dump(existing_data, simulation_file, indent=4)
        simulation_file.truncate()
    except Exception as e:
        print(f"Error writing to simulation file: {e}")