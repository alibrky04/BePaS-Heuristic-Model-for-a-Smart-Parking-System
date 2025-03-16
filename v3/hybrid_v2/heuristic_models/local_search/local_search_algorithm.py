import copy
import time

from v3.hybrid_v2.helpers.local_search.helper import isEven
from v3.hybrid_v2.heuristic_models.local_search.routines import *


def localSearch(machine_list, number_of_machines, job_list, number_of_jobs, time_limit):
    start_time = time.time()  # Start tracking time
    sum_of_jobs = sum(x.length for x in job_list.values())
    avg_job = sum_of_jobs / number_of_jobs
    prev = calculateMakeSpan(machine_list)
    even = False
    latest_best_state = copy.deepcopy(machine_list)

    while not even:
        oneJobRoutine(machine_list, number_of_machines, job_list, number_of_jobs)
        oneByOneSwapRoutine(machine_list, number_of_machines, job_list, number_of_jobs)
        colorChangeRoutine(machine_list, number_of_machines, number_of_jobs)
        twoByTwoSwapRoutine(machine_list, number_of_machines, number_of_jobs)
        circularSwapRoutine(machine_list, number_of_machines, number_of_jobs)
        even = isEven(machine_list, avg_job)

        if time.time() - start_time > time_limit:  # Check after completing the while loop iteration
            machine_list[:] = latest_best_state[:]  # Restore latest valid state
            return

        new_make_span = calculateMakeSpan(machine_list)
        if new_make_span < prev:
            prev = new_make_span
            latest_best_state = copy.deepcopy(machine_list)
        else:
            break
