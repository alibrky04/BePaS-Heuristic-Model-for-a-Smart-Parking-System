import os

from v2.nearest_lot.Controller import Controller
from v2.nearest_lot.Simulator import Simulator
from v2.nearest_lot import Constants as cnst

def main(dist, batch_time, sim_output_file):
    # Initialize parameters
    cnst.SIMULATION_DISTRIBUTION = dist
    cnst.BATCH_TIME = batch_time
    cnst.MAX_ROUNDS = int((60 / batch_time) * 48)
    cnst.TIME_BETWEEN_ROUNDS = batch_time
    cnst.SIM_OUTPUT_FILE = sim_output_file
    
    simulator = Simulator()

    glpk_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'GLPK'))

    ct = 0
    day = 1

    for i in range(cnst.NUM_OF_SIMULATIONS):
        distribution = simulator.generateDistribution(genType=cnst.GENERATION_TYPE, distType=cnst.SIMULATION_DISTRIBUTION, dLength=cnst.MAX_ROUNDS)

        W_CAR = distribution

        controller = Controller(cnst.COMMAND, glpk_folder_path, distribution, W_CAR[ct], cnst.MAP_SIZE)
        
        while ct < cnst.MAX_ROUNDS:
            # print('***********************************************\n')

            controller.createCars(doChange=True, new_car_num=W_CAR[ct])

            controller.updateState(ct, day==cnst.MAX_DAY)
            # controller.showData()

            controller.removeCars()

            ct += 1

            if ct == day * cnst.MAX_ROUNDS and day < cnst.MAX_DAY:
                ct = 0
                day += 1
            
            # print()

        controller.storeData()

        ct = 0
        day = 1