from v2.local_search.Constants import SIMULATION_DISTRIBUTION, MEAN, DEVIATION, SCALE
from random import randint
from numpy.random import normal, exponential
import numpy as np

def createDistribution(num_of_jobs):
    # Uniform distribution
    if SIMULATION_DISTRIBUTION == "UNIFORM":
        return randint(num_of_jobs, num_of_jobs * 2)
    # Normal distribution
    elif SIMULATION_DISTRIBUTION == "NORMAL":
        return int(np.round(np.abs(normal(MEAN, DEVIATION))))
    # Exponential distribution
    elif SIMULATION_DISTRIBUTION == "EXPONENTIAL":
        return int(np.round(np.abs(exponential(SCALE))))