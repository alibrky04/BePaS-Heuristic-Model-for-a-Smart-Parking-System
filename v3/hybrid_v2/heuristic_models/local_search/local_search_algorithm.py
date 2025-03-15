import copy
import time

from v3.hybrid_v2.helpers.local_search.helper import isEven
from v3.hybrid_v2.heuristic_models.local_search.routines import *


def localSearch(machine_list, number_of_machines, job_list, number_of_jobs, output_file, debug_file, time_limit):
    start_time = time.time()  # Start tracking time
    sum_of_jobs = sum(x.length for x in job_list.values())
    avg_job = sum_of_jobs / number_of_jobs
    prev = calculateMakeSpan(machine_list)
    even = False
    latest_best_state = copy.deepcopy(machine_list)

    while not even:
        print(f"time remaining: {time.time() - start_time}")
        oneJobRoutine(machine_list, number_of_machines, job_list, number_of_jobs, output_file, debug_file)
        oneByOneSwapRoutine(machine_list, number_of_machines, job_list, number_of_jobs, output_file, debug_file)
        colorChangeRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file)
        twoByTwoSwapRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file)
        circularSwapRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file)
        even = isEven(machine_list, avg_job)

        if time.time() - start_time > time_limit:  # Check after completing the while loop iteration
            print("Time limit exceeded! Rolling back to the latest valid state.")
            machine_list[:] = latest_best_state[:]  # Restore latest valid state
            return

        new_make_span = calculateMakeSpan(machine_list)
        if new_make_span < prev:
            prev = new_make_span
            latest_best_state = copy.deepcopy(machine_list)
        else:
            break
