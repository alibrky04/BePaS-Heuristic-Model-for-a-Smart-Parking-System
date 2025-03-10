from v1.local_search.helpers.createMachines import createMachines
from v1.local_search.helpers.createJobs import createJobs
from v1.local_search.helpers.createRandomJobValues import createRandomJobValues
from v1.local_search.helpers.removeJobs import removeJobs
from v1.local_search.helpers.calculateToD import calculateToD
from v1.local_search.helpers.createDistribution import createDistribution

from v1.local_search.heuristic_model.initialAssing import initialAssign
from v1.local_search.heuristic_model.local_search_algorithm import localSearch
from v1.local_search.heuristic_model.lpt_algorithm import legalLpt

from v1.local_search.io_utils.printMachineStat import printMachineStat
from v1.local_search.io_utils.printMachineStatOut import printMachineStatOut
from v1.local_search.io_utils.simulationStatOut import simulationStatOut

from v1.local_search.Constants import *

import os
import random

random.seed(42)

if __name__ == "__main__":
    debug_file = open(os.path.join(os.path.dirname(__file__), "output/debug_out.txt"), "w")
    out_file = open(os.path.join(os.path.dirname(__file__), "output/output.txt"), "w")
    simulation_file = open(os.path.join(os.path.dirname(__file__), "simulationData/simulation4.json"), "r+")

    # num_of_machines, num_of_jobs, min_processing_time, max_processing_time = handleInput()

    for _ in range(NUM_OF_SIMULATIONS):
        ToD = []
        simulation_machines = None
        
        for i in range(MAX_ROUNDS):
            # Check constants.py for the distribution types
            # num_of_jobs is only used for the uniform distribution
            rand_job_num = createDistribution(NUM_OF_JOBS)

            raw_jobs = createRandomJobValues(NUM_OF_MACHINES, rand_job_num, MIN_PROCESSING_TIME, MAX_PROCESSING_TIME, i)

            print("Number of Machines:", NUM_OF_MACHINES, file=out_file)

            print(NUM_OF_JOBS, "jobs:", file=out_file)
            for job in raw_jobs:
                print(job, file=out_file)

            print("---------------------------------", file=out_file)

            machine_list = createMachines(NUM_OF_MACHINES, simulation_machines, i) 
            job_list = createJobs(raw_jobs, debug_file)
            printMachineStatOut.out_stat_counter = 0
            if NUM_OF_JOBS > 500:
                machines_list = legalLpt(job_list, machine_list)
            else:
                initialAssign(job_list, machine_list)
            printMachineStat(machine_list, debug_file)
            localSearch(machine_list, NUM_OF_MACHINES, job_list, NUM_OF_JOBS, out_file, debug_file)

            if i == 0:
                simulation_machines = machine_list.copy()
            else:
                for j in range(NUM_OF_MACHINES):
                    simulation_machines[j].span = machine_list[j].span
                    for job in machine_list[j].assigned_jobs.values():
                        simulation_machines[j].assigned_jobs[job.number] = job
                    simulation_machines[j].types = machine_list[j].types.copy()
                    simulation_machines[j].types_sums = machine_list[j].types_sums.copy()

            ToD.append(calculateToD(machine_list))

            printMachineStatOut(simulation_machines, out_file, "Final state")
            removeJobs(simulation_machines)
            printMachineStatOut(simulation_machines, out_file, "Final state after waiting period")
        
        simulationStatOut(ToD, NUM_OF_MACHINES, rand_job_num, MIN_PROCESSING_TIME, MAX_PROCESSING_TIME, simulation_file)

    debug_file.close()
    out_file.close()
    simulation_file.close()