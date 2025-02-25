import os
import random

random.seed(42)

from Controller import Controller
from Simulator import Simulator
from Constants import *

simulator = Simulator()

glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

ct = 0
day = 1

for i in range(NUM_OF_SIMULATIONS):
    distribution = simulator.generateDistribution(genType=GENERATION_TYPE, distType=SIMULATION_DISTRIBUTION, dLength=MAX_ROUNDS)

    W_CAR = distribution

    controller = Controller(COMMAND, glpk_folder_path, distribution, W_CAR[ct], MAP_SIZE)
    
    while ct < MAX_ROUNDS:
        # print('***********************************************\n')

        controller.createCars(doChange=True, new_car_num=W_CAR[ct])

        controller.updateState(ct, day==MAX_DAY)
        # controller.showData()

        controller.removeCars()

        ct += 1

        if ct == day * MAX_ROUNDS and day < MAX_DAY:
            ct = 0
            day += 1
        
        # print()

    controller.storeData()

    ct = 0
    day = 1