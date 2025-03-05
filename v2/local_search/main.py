from v2.local_search.helpers.createMachines import createMachines
from v2.local_search.helpers.createJobs import createJobs
from v2.local_search.helpers.createRandomJobValues import createRandomJobValues
from v2.local_search.helpers.removeJobs import removeJobs
from v2.local_search.helpers.calculateToD import calculateToD
from v2.local_search.helpers.createDistribution import createDistribution

from v2.local_search.heuristic_model.initialAssing import initialAssign
from v2.local_search.heuristic_model.local_search_algorithm import localSearch
from v2.local_search.heuristic_model.lpt_algorithm import legalLpt

from v2.local_search.io_utils.printMachineStat import printMachineStat
from v2.local_search.io_utils.printMachineStatOut import printMachineStatOut
from v2.local_search.io_utils.simulationStatOut import simulationStatOut

from v2.local_search import Constants as cnst

import os

def main(distribution, batch_time, sim_output_file):
    # Initialize parameters
    cnst.SIMULATION_DISTRIBUTION = distribution
    cnst.BATCH_TIME = batch_time
    cnst.NUMBER_OF_ROUNDS = int((60 / batch_time) * 48)
    cnst.DECAY_PER_ROUND = batch_time
    cnst.SIM_OUTPUT_FILE = sim_output_file
    
    debug_file = open(os.path.join(os.path.dirname(__file__), "output/debug_out.txt"), "w")
    out_file = open(os.path.join(os.path.dirname(__file__), "output/output.txt"), "w")
    simulation_file = open(cnst.SIM_OUTPUT_FILE, "w+")

    # num_of_machines, num_of_jobs, min_processing_time, max_processing_time = handleInput()

    for _ in range(cnst.NUM_OF_SIMULATIONS):
        ToD = []
        simulation_machines = None
        
        for i in range(cnst.MAX_ROUNDS):
            # Check cnst.py for the distribution types
            # num_of_jobs is only used for the uniform distribution
            rand_job_num = createDistribution(cnst.NUM_OF_JOBS)

            raw_jobs = createRandomJobValues(cnst.NUM_OF_MACHINES, rand_job_num, cnst.MIN_PROCESSING_TIME, cnst.MAX_PROCESSING_TIME, i)

            print("Number of Machines:", cnst.NUM_OF_MACHINES, file=out_file)

            print(cnst.NUM_OF_JOBS, "jobs:", file=out_file)
            for job in raw_jobs:
                print(job, file=out_file)

            print("---------------------------------", file=out_file)

            machine_list = createMachines(cnst.NUM_OF_MACHINES, simulation_machines, i) 
            job_list = createJobs(raw_jobs, debug_file)
            printMachineStatOut.out_stat_counter = 0
            if cnst.NUM_OF_JOBS > 500:
                machines_list = legalLpt(job_list, machine_list)
            else:
                initialAssign(job_list, machine_list)
            printMachineStat(machine_list, debug_file)
            localSearch(machine_list, cnst.NUM_OF_MACHINES, job_list, cnst.NUM_OF_JOBS, out_file, debug_file)

            if i == 0:
                simulation_machines = machine_list.copy()
            else:
                for j in range(cnst.NUM_OF_MACHINES):
                    simulation_machines[j].span = machine_list[j].span
                    for job in machine_list[j].assigned_jobs.values():
                        simulation_machines[j].assigned_jobs[job.number] = job
                    simulation_machines[j].types = machine_list[j].types.copy()
                    simulation_machines[j].types_sums = machine_list[j].types_sums.copy()

            ToD.append(calculateToD(machine_list))

            printMachineStatOut(simulation_machines, out_file, "Final state")
            removeJobs(simulation_machines)
            printMachineStatOut(simulation_machines, out_file, "Final state after waiting period")
        
        simulationStatOut(ToD, cnst.NUM_OF_MACHINES, rand_job_num, cnst.MIN_PROCESSING_TIME, cnst.MAX_PROCESSING_TIME, simulation_file)

    debug_file.close()
    out_file.close()
    simulation_file.close()