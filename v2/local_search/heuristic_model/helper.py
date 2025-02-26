# prints a certain rank of balance,mainly for debugging
import math

from heuristic_model.calculateMakeSpan import calculateMakeSpan


def printRank(machine_list, output_file):
    spans = []
    makespan = calculateMakeSpan(machine_list)
    for machine in machine_list:
        spans.append((makespan - machine.span) ** 2)
    print("Distance rank is:", math.sqrt(sum(spans)), file=output_file)


# Checks if all machines are even so we can stop the run
def isEven(machines_list, average_job):
    if machines_list.count(machines_list[0].span) == len(machines_list):
        return True
    else:  # might be a case of non-even optimal solution
        if calculateMakeSpan(machines_list) == math.ceil(average_job):
            return True
    return False


# finds the minumum loaded machine in a state
def findMinLoadMachineLegaly(m_list):
    m_list_sorted = sorted(m_list, key=lambda x: x.span)
    return m_list_sorted
