from v2.local_search.heuristic_model.calculateMakeSpan import calculateMakeSpan
from v2.local_search.heuristic_model.helper import isEven
from v2.local_search.heuristic_model.routines import *

import v2.local_search.Constants as cnst
import time
import copy

def localSearch(machine_list, number_of_machines, job_list, number_of_jobs):
    start_time = time.time()
    sum_of_jobs = sum(x.length for x in job_list.values())
    avg_job = sum_of_jobs / number_of_jobs

    prev = calculateMakeSpan(machine_list)
    even = False
    latest_best_state = copy.deepcopy(machine_list)

    while not even:
        oneJobRoutine(machine_list, number_of_machines, job_list, number_of_jobs, start_time)
        oneByOneSwapRoutine(machine_list, number_of_machines, job_list, number_of_jobs, start_time)
        colorChangeRoutine(machine_list, number_of_machines, number_of_jobs, start_time)
        twoByTwoSwapRoutine(machine_list, number_of_machines, number_of_jobs, start_time)
        circularSwapRoutine(machine_list, number_of_machines, number_of_jobs, start_time)
        even = isEven(machine_list, avg_job)

        if cnst.MODEL_TIME_LIMIT:
            print("a")
            if time.time() - start_time > cnst.MODEL_TIME_LIMIT:  # Check after completing the while loop iteration
                machine_list[:] = latest_best_state[:]  # Restore latest valid state
                return

        if even is True:
            break

        new_make_span = calculateMakeSpan(machine_list)
        if new_make_span < prev:
            prev = new_make_span
            latest_best_state = copy.deepcopy(machine_list)
        else:
            break
