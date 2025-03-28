import copy
import time


def branch_and_bound(new_jobs, machines, index, current_best, best_assignment, num_machines, start_time, time_limit):
    # Check if time limit is exceeded AND at least one complete assignment has been found
    if time.time() - start_time >= time_limit:
        return  # Stop further recursion without breaking current assignments

    # Base case: all new jobs have been assigned at least once
    # print(f"index {index}")
    if index == len(new_jobs):
        current_makespan = max(machine.load for machine in machines)
        if current_makespan < current_best[0]:
            current_best[0] = current_makespan
            best_assignment[:] = [copy.deepcopy(machine.jobs) for machine in machines]
        # print(f"index {index} and current_best[0] {current_best[0]}")
        # print(f" best assigment {best_assignment}")
        # for machine in machines:
        #     print(f" machine {machine}")
        # return

    # Lower bound calculation and pruning
    total_remaining = sum(job.length for job in new_jobs[index:])
    current_max = max(machine.load for machine in machines)
    current_min = min(machine.load for machine in machines)
    lower_bound = max(current_max, current_min + total_remaining / num_machines)

    if lower_bound >= current_best[0]:
        return  # Prune this branch

    # Try assigning new_jobs[index] to each machine
    for machine in machines:
        if time.time() - start_time >= time_limit:
            return  # Stop recursion if time limit is exceeded

        orig_load = machine.load
        orig_jobs = machine.jobs[:]  # Shallow copy

        machine.add_job(new_jobs[index])
        branch_and_bound(new_jobs, machines, index + 1, current_best, best_assignment, num_machines, start_time,
                         time_limit)

        # Backtrack
        machine.jobs = orig_jobs
        machine.load = orig_load
