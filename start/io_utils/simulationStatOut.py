import json

def simulationStatOut(ToD, simulation_file):
    try:
        # Load existing data if file is not empty
        try:
            simulation_file.seek(0)
            existing_data = json.load(simulation_file)
        except json.JSONDecodeError:
            existing_data = []

        # Generate a simulation ID based on the number of existing simulations
        simulation_id = len(existing_data) + 1

        # Append new ToD value with simulation ID
        existing_data.append({
            "simulation_id": simulation_id,
            "ToD": ToD
        })

        # Write back to file
        simulation_file.seek(0)
        json.dump(existing_data, simulation_file, indent=4)
        simulation_file.truncate()
    except Exception as e:
        print(f"Error writing to simulation file: {e}")