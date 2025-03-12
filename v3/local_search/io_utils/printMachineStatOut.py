from v3.local_search.heuristic_model.calculateMakeSpan import calculateMakeSpan


def printMachineStatOut(machine_list, out_file,action):
    print("---------------MACHINES STATS # %s %s--------------------------\n" % (
    printMachineStatOut.out_stat_counter, action), file=out_file)
    for machine in machine_list:
        cur_job_list = machine.retrieveJobsList()
        print("machine number ", machine.number, "assigned jobs [number,length,type]:", file=out_file)
        l = []
        for job_number, job in cur_job_list.items():
            l.append(job)
        print("".join(str(l)), file=out_file)

        print("Assigned types: ", machine.getTypes(), file=out_file)
        print("Types histogram: ", machine.types, "Sum of each type: ", machine.types_sums, "Makespan : ", machine.span,
              file=out_file)
        print("\n", file=out_file)
    print("Max makespan is : ", calculateMakeSpan(machine_list), file=out_file)
    print("------------------------------------------------\n", file=out_file)
    printMachineStatOut.out_stat_counter = printMachineStatOut.out_stat_counter + 1