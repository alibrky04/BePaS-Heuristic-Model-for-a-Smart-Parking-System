from helpers.createMachines import createMachines
from helpers.createJobs import createJobs
from start.heuristic_model.initialAssing import initialAssign
from start.heuristic_model.local_search_algorithm import localSearch
from start.heuristic_model.lpt_algorithm import legalLpt

from start.io.handleInput import handleInput
from start.io.printMachineStat import printMachineStat
from start.io.printMachineStatOut import printMachineStatOut

if __name__ == "__main__":
    print("hello")

    debug_file = open("./output/debug_out.txt", "w")
    out_file = open("./output/output.txt", "w")

    num_of_machines, raw_jobs = handleInput()
    num_of_jobs = len(raw_jobs)

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
        initialAssign(job_list,machine_list)
    printMachineStat(machine_list,debug_file)
    localSearch(machine_list,num_of_machines,job_list,num_of_jobs,out_file,debug_file)

    printMachineStatOut(machine_list,out_file,"Final state")

    debug_file.close()
    out_file.close()
