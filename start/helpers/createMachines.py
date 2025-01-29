from start.models.Machine import Machine


def createMachines(number_of_machines):
    machines = []
    for i in range(0, number_of_machines):
        cur_machine = Machine(i)
        machines.append(cur_machine)
    return machines
