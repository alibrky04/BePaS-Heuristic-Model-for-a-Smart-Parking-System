from models.Machine import Machine


def createMachines(number_of_machines, last_iteration_machines, round):
    machines = []
    for i in range(0, number_of_machines):
        if round == 0:
            cur_machine = Machine(i)
        else:
            cur_machine = Machine(i, last_iteration_machines[i].span)
        machines.append(cur_machine)
    return machines
