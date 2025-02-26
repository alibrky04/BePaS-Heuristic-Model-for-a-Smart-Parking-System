from heuristic_model.calculateMakeSpan import calculateMakeSpan
from heuristic_model.helper import isEven
from heuristic_model.routines import oneJobRoutine, oneByOneSwapRoutine, colorChangeRoutine, \
    twoByTwoSwapRoutine, \
    circularSwapRoutine
from io_utils.printMachineStatOut import printMachineStatOut


def localSearch(machine_list, number_of_machines, job_list, number_of_jobs, output_file, debug_file):
    sum_of_jobs = sum(x.length for x in job_list.values())
    avg_job = sum_of_jobs / number_of_jobs

    printMachineStatOut(machine_list, output_file, "Initial state")

    prev = calculateMakeSpan(machine_list)
    even = False
    while not even:
        oneJobRoutine(machine_list, number_of_machines, job_list, number_of_jobs, output_file, debug_file)
        oneByOneSwapRoutine(machine_list, number_of_machines, job_list, number_of_jobs, output_file, debug_file)
        colorChangeRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file)
        twoByTwoSwapRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file)
        circularSwapRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file)
        even = isEven(machine_list, avg_job)
        if even is True:
            break
        if calculateMakeSpan(machine_list) < prev:
            prev = calculateMakeSpan(machine_list)
        else:
            break
