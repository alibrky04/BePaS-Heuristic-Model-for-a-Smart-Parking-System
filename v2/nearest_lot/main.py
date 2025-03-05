import os

from v2.nearest_lot.Controller import Controller
from v2.nearest_lot.Simulator import Simulator
from v2.nearest_lot.Constants import *

def main(dist, batch_time, sim_output_file):
    from v2.nearest_lot import Constants
    
    # Initialize parameters
    Constants.SIMULATION_DISTRIBUTION = dist
    Constants.BATCH_TIME = batch_time
    Constants.MAX_ROUNDS = int((60 / batch_time) * 48)
    Constants.TIME_BETWEEN_ROUNDS = batch_time
    Constants.SIM_OUTPUT_FILE = sim_output_file
    
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