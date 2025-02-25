from models.Machine import Machine


def create_machines(number_of_machines):
    return [Machine(i) for i in range(number_of_machines)]

def calculate_tod(machine_list):
    max_round_makespan = max(machine.load for machine in machine_list)
    min_round_makespan = min(machine.load for machine in machine_list)
    return max_round_makespan - min_round_makespan
