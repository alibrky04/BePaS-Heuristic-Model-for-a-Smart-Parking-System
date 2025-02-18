import os
from time import sleep
from Controller import Controller
from Simulator import Simulator

simulator = Simulator()

EPOCH = 24
WAIT_TIME = 10
MAX_SIM = 1
MAX_DAY = 2
P_LOT = 5
MAX_CAPACITY = 25
MAP_SIZE = 50
SIM_TYPE = 3
nearModelType = 1

if SIM_TYPE == 1:
    COMMAND = 'glpsol --model SPS.mod --data SPS.dat --display SPS.out'
    DATAFILE = 'SPS/GLPK/SPS.dat'
elif SIM_TYPE == 2:
    COMMAND = 'glpsol --model SPS_CAR.mod --data SPS_CAR.dat --display SPS_CAR.out'
    DATAFILE = 'SPS/GLPK/SPS_CAR.dat'
elif SIM_TYPE == 3:
    COMMAND = ''
    DATAFILE = ''

glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

ct = 0
counter = 0
sim_count = 0
day = 1
#deviation = 1
#mean = 2
genType = 2
distType = 1

while sim_count < MAX_SIM:
    distribution = simulator.generateDistribution(genType=genType, distType=distType, dLength=EPOCH)

    W_CAR = distribution

    controller = Controller(COMMAND, glpk_folder_path, distribution, P_LOT, W_CAR[ct], MAX_CAPACITY, MAP_SIZE)
    
    while ct < EPOCH:
        print('***********************************************\n')

        controller.createCars(doChange=True, new_car_num=W_CAR[ct])

        if SIM_TYPE == 1 or SIM_TYPE == 2:
            controller.writeData(DATAFILE, model=SIM_TYPE)
            controller.runSolver()

        controller.updateState(ct, day==MAX_DAY, simType=SIM_TYPE, nearModelType=nearModelType)
        controller.showData()

        while counter < WAIT_TIME:
            controller.removeCars()
            sleep(1)
            counter += 1

        counter = 0
        ct += 1

        if ct == day * EPOCH and day < MAX_DAY:
            ct = 0
            day += 1
        
        print()

    print(f'Simulation {sim_count + 1} has ended.')

    controller.storeData(start_hour=EPOCH * (MAX_DAY - 1), sim_count=sim_count)

    print('Data is recorded.')
    print('Next simulation will start in 5 seconds.\n')

    ct = 0
    day = 1

    sleep(5)
    
    sim_count += 1

"""
while genType < 5:
    with open('SPS/Datas/SimData.txt', 'a') as file:
        file.write(f'genType: {genType}\ndistType: {distType}\nEND\n\n')

    if distType == 1:
        distType = 2
    else:
        distType = 1
        genType += 1

    sim_count = 0
"""

"""
while mean <= 16:
    
    with open('SPS/Datas/SimData.txt', 'a') as file:
        file.write(f'Mean: {mean}\nEND\n\n')

    mean += 1
    deviation = mean/2
    sim_count = 0
"""