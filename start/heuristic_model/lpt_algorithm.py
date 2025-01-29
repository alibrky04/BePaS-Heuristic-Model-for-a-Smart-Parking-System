import copy

from start.heuristic_model.helper import findMinLoadMachineLegaly


def legalLpt(jobs, m_list):
    job_list_sorted_by_length = sorted(jobs, key=lambda x: x.length, reverse=True)
    new_machines_list = copy.deepcopy(m_list)
    for i in range(len(job_list_sorted_by_length)):
        legal = False
        # check assignment for next min loaded machine that is legal
        for j in range(len(new_machines_list)):
            assign_to_machines = findMinLoadMachineLegaly(new_machines_list)
            new_machines_list[assign_to_machines[j].number].addJob(job_list_sorted_by_length[i])
            if new_machines_list[assign_to_machines[j].number].isLegal():
                legal = True
                break
            else:  # revert
                new_machines_list[assign_to_machines[j].number].removeJob(job_list_sorted_by_length[i].number)
        if not legal:
            return []

    return new_machines_list
