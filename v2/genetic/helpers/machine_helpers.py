from v2.genetic.models.Machine import Machine


def calculate_makespan(machines):
    return max(machine.load for machine in machines)


def create_machines(number_of_machines):
    return [Machine(i) for i in range(number_of_machines)]


def calculate_tod(machine_list):
    tod = 0
    min_round_makespan = min(machine.load for machine in machine_list)

    for machine in machine_list:
        tod += machine.load - min_round_makespan

    return tod
