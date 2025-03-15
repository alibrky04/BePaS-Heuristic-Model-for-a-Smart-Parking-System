from v3.hybrid_v2.models.Machine import Machine
from v3.hybrid_v2.models.MachineAlien import MachineAlien
import v3.hybrid_v2.Constants as cnst

def create_machines(number_of_machines):
    return [Machine(i) for i in range(number_of_machines)]


def calculate_tod(machine_list):
    tod = 0
    min_round_makespan = min(machine.load for machine in machine_list)

    for machine in machine_list:
        tod += machine.load - min_round_makespan

    return tod


def create_machines_alien(number_of_machines, last_iteration_machines, simulation_round):
    machines = []
    for i in range(number_of_machines):
        if simulation_round == 1:
            cur_machine = MachineAlien(i)
        else:
            cur_machine = MachineAlien(i, last_iteration_machines[i].span)
        machines.append(cur_machine)
    return machines


def removeJobs(machine_list):
    for machine in machine_list:
        for job in list(machine.assigned_jobs.values()):
            job.duration -= cnst.DECAY_PER_ROUND
            if job.duration <= 0:
                machine.removeJob(job.number)


