from v3.local_search.heuristic_model.calculateMakeSpan import calculateMakeSpan


def printMachineStat(machine_list, debug_file=None):
    if debug_file:
        print("---------------MACHINES STATS--------------------------\n", file=debug_file)
        for machine in machine_list:
            cur_job_list = machine.retrieveJobsList()
            print("machine # ", machine.number, "assigned jobs #:", file=debug_file)
            l = []
            for job in cur_job_list:
                l.append(job)
            print("".join(str(l)), file=debug_file)

            print("Types: ", machine.types, "Makespan : ", machine.span, file=debug_file)
        print("Max makespan is : ", calculateMakeSpan(machine_list), file=debug_file)
        print("------------------------------------------------\n", file=debug_file)
    else:
        print("---------------MACHINES STATS--------------------------\n")
        for machine in machine_list:
            cur_job_list = machine.retrieveJobsList()
            print("machine # ", machine.number, "assigned jobs #:")
            l = []
            for job in cur_job_list:
                l.append(job)
            print("".join(str(l)))

            print("Types: ", machine.types, "Makespan : ", machine.span)
        print("Max makespan is : ", calculateMakeSpan(machine_list))
        print("------------------------------------------------\n")
