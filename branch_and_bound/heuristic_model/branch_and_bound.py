import copy

def branch_and_bound(new_jobs, machines, index, current_best, best_assignment, num_machines):
    """
    Recursive BnB: assign new_jobs (already sorted in descending order by length)
    to the machines (which already have some jobs from previous rounds) in order to
    minimize the makespan (maximum machine load).

    Parameters:
      new_jobs: list of Job objects to assign.
      machines: list of Machine objects representing current state.
      index: current index in new_jobs that we want to assign.
      current_best: a single-element list containing the current best makespan found.
      best_assignment: list (of lists) that will hold the best job assignment for each machine.
      num_machines: total number of machines.
    """
    # Base: all new jobs have been assigned
    if index == len(new_jobs):
        current_makespan = max(machine.load for machine in machines)
        if current_makespan < current_best[0]:
            current_best[0] = current_makespan
            # Record the best assignment (deep copy the list of jobs for each machine)
            best_assignment[:] = [copy.deepcopy(machine.jobs) for machine in machines]
        return

    # Lower bound: the maximum between the current maximum load and
    # the ideal additional load if remaining work is evenly distributed.
    total_remaining = sum(job.length for job in new_jobs[index:])
    current_max = max(machine.load for machine in machines)
    current_min = min(machine.load for machine in machines)
    lb = max(current_max, current_min + total_remaining / num_machines)
    if lb >= current_best[0]:
        return  # prune this branch

    # Try assigning new_jobs[index] to each machine in turn.
    for machine in machines:
        # Save current state of this machine
        orig_load = machine.load
        orig_jobs = machine.jobs[:]  # shallow copy is enough since jobs are immutable in length

        # Assign job to machine
        machine.add_job(new_jobs[index])
        branch_and_bound(new_jobs, machines, index + 1, current_best, best_assignment, num_machines)
        # Backtrack: remove the job
        machine.jobs = orig_jobs
        machine.load = orig_load
