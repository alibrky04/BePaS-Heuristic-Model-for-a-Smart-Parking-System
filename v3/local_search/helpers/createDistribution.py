from v3.local_search import Constants as cnst
from random import randint
from numpy.random import normal, exponential
import numpy as np

def createDistribution(number_of_jobs):
    # Uniform distribution
    if cnst.SIMULATION_DISTRIBUTION == "STATIC":
        return number_of_jobs
    elif cnst.SIMULATION_DISTRIBUTION == "UNIFORM":
        return randint(number_of_jobs, number_of_jobs * 2)
    # Normal distribution
    elif cnst.SIMULATION_DISTRIBUTION == "NORMAL":
        return int(np.round(np.abs(normal(cnst.MEAN, cnst.DEVIATION))))
    # Exponential distribution
    elif cnst.SIMULATION_DISTRIBUTION == "EXPONENTIAL":
        return int(np.round(np.abs(exponential(cnst.SCALE))))