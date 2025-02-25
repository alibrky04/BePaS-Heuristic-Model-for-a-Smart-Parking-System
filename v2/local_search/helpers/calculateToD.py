import math

def calculateToD(simulation_machines):
    ToD = 0
    minimumLoad = math.inf
    
    for machine in simulation_machines:
        minimumLoad = min(minimumLoad, machine.span)

    for machine in simulation_machines:
        ToD += machine.span - minimumLoad

    return ToD