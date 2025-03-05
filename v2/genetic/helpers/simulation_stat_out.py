import json

from v2.genetic import Constants as cnst


def simulation_stat_out(ToD, num_of_jobs, simulation_file):
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
            "car_batch_size": cnst.NUMBER_OF_ROUNDS/2,
            "num_of_machines": cnst.NUMBER_OF_MACHINES,
            "num_of_jobs": num_of_jobs,
            "min_processing_time": cnst.MINIMUM_JOB_LENGTH,
            "max_processing_time": cnst.MAXIMUM_JOB_LENGTH,
            "mean": cnst.MEAN,
            "deviation": cnst.DEVIATION,
            "scale": cnst.SCALE
        })

        # Write back to file
        simulation_file.seek(0)
        json.dump(existing_data, simulation_file, indent=4)
        simulation_file.truncate()
    except Exception as e:
        print(f"Error writing to simulation file: {e}")