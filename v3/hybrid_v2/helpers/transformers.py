import copy
import v3.hybrid_v2.Constants as cnst

from v3.hybrid_v2.helpers.machine_helpers import create_machines_alien


def turn_assignment_into_chromosome(number_of_job, job_list, best_assignment):
    chromosome_array = [-1 for _ in range(number_of_job)]
    for machine_id, assigment in enumerate(best_assignment):
        for job in assigment:
            for actual_job_index, actual_job in enumerate(job_list):
                if actual_job.job_id == job.job_id:
                    chromosome_array[actual_job_index] = machine_id
    if -1 in chromosome_array:
        raise ValueError("Invalid Conversation check algorithms.")
    return chromosome_array


def turn_locals_solution_into_assigment(native_machines, alien_machines, native_jobs):
    assigment = []
    for native_machine, alien_machine in zip(native_machines, alien_machines):
        assigned_jobs = copy.deepcopy(native_machine.jobs)
        print(f"native_machine: {native_machine}")
        for alien_job_number in alien_machine.assigned_jobs:
            for native_job in native_jobs:
                if native_job.job_id == alien_job_number:
                    assigned_jobs.append(native_job)
        print(f"assigned_jobs: {assigned_jobs}")
        assigment.append(assigned_jobs)

    if len(assigment) != len(native_machines):
        raise ValueError("Invalid Conversation check algorithms.")
    return assigment

def turn_chromosome_into_machines(machines_alien,round_id, native_jobs, alien_jobs, chromosome):
    simulation_machines_alien = create_machines_alien(cnst.NUMBER_OF_MACHINES, machines_alien, round_id)
    for i, job in enumerate(native_jobs):
        alien_job = alien_jobs[job.job_id]
        print(f"i = {i} : native job:{job}  alien job: {alien_jobs[job.job_id]}Best assignment: {chromosome[i]}")
        simulation_machines_alien[chromosome[i]].addJob(alien_job)
    return simulation_machines_alien
    # for each i job in


