from helpers.createMachines import createMachines
from helpers.createJobs import createJobs
from helpers.createRandomJobValues import createRandomJobValues
from helpers.removeJobs import removeJobs
from heuristic_model.initialAssing import initialAssign
from heuristic_model.local_search_algorithm import localSearch
from heuristic_model.lpt_algorithm import legalLpt

from io_utils.handleInput import handleInput
from io_utils.printMachineStat import printMachineStat
from io_utils.printMachineStatOut import printMachineStatOut

from Constants import MAX_ROUNDS
from Constants import TIME_BETWEEN_ROUNDS

import os
from time import sleep

if __name__ == "__main__":
    debug_file = open(os.path.join(os.path.dirname(__file__), "output/debug_out.txt"), "w")
    out_file = open(os.path.join(os.path.dirname(__file__), "output/output.txt"), "w")

    num_of_machines, num_of_jobs, min_processing_time, max_processing_time = handleInput()
    
    for _ in range(MAX_ROUNDS):
        raw_jobs = createRandomJobValues(num_of_jobs, min_processing_time, max_processing_time)

        print("Number of Machines:", num_of_machines, file=out_file)

        print(num_of_jobs, "jobs:", file=out_file)
        for job in raw_jobs:
            print(job, file=out_file)

        print("---------------------------------", file=out_file)

        machine_list = createMachines(num_of_machines)
        job_list = createJobs(raw_jobs, debug_file)
        printMachineStatOut.out_stat_counter = 0
        if num_of_jobs > 500:
            machines_list = legalLpt(job_list, machine_list)
        else:
            initialAssign(job_list, machine_list)
        printMachineStat(machine_list, debug_file)
        localSearch(machine_list, num_of_machines, job_list, num_of_jobs, out_file, debug_file)

        printMachineStatOut(machine_list, out_file, "Final state")

        removeJobs(machine_list)

        printMachineStatOut(machine_list, out_file, "Final state after waiting period")
        
        # TODO: Need a way to save the remaining jobs after the waiting period (jobs with duration > 0)
        # lockJobs()
        # TODO: initialAssign() should be edited so the locked jobs are also assigned to the new machines

    debug_file.close()
    out_file.close()