from v2.local_search import Constants as cnst
from random import randint
from numpy.random import normal, exponential
import numpy as np

def createDistribution(num_of_jobs):
    # Uniform distribution
    if cnst.SIMULATION_DISTRIBUTION == "UNIFORM":
        return randint(num_of_jobs, num_of_jobs * 2)
    # Normal distribution
    elif cnst.SIMULATION_DISTRIBUTION == "NORMAL":
        return int(np.round(np.abs(normal(cnst.MEAN, cnst.DEVIATION))))
    # Exponential distribution
    elif cnst.SIMULATION_DISTRIBUTION == "EXPONENTIAL":
        return int(np.round(np.abs(exponential(cnst.SCALE))))