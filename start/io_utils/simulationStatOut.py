from Constants import SIMULATION_DISTRIBUTION, MEAN, DEVIATION, SCALE, MAX_ROUNDS

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

        if SIMULATION_DISTRIBUTION == 1:
            simulation_distribution = "uniform"
        elif SIMULATION_DISTRIBUTION == 2:
            simulation_distribution = "normal"
        elif SIMULATION_DISTRIBUTION == 3:
            simulation_distribution = "exponential"

        existing_data.append({
            "simulation_id": simulation_id,
            "simulation_distribution": simulation_distribution,
            "ToD": ToD_str,
            "car_batch_size": MAX_ROUNDS/2,
            "num_of_machines": num_of_machines,
            "num_of_jobs": num_of_jobs,
            "min_processing_time": min_processing_time,
            "max_processing_time": max_processing_time,
            "mean": MEAN,
            "deviation": DEVIATION,
            "scale": SCALE
        })

        simulation_file.seek(0)
        json.dump(existing_data, simulation_file, indent=4)
        simulation_file.truncate()
    except Exception as e:
        print(f"Error writing to simulation file: {e}")