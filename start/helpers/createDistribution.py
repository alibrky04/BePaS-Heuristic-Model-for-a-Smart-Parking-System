from Constants import SIMULATION_DISTRIBUTION, MEAN, DEVIATION, SCALE
from random import randint
from numpy.random import normal, exponential
import numpy as np

def createDistribution(num_of_jobs):
    # Uniform distribution
    if SIMULATION_DISTRIBUTION == 1:
        return randint(num_of_jobs, num_of_jobs * 2)
    # Normal distribution
    elif SIMULATION_DISTRIBUTION == 2:
        return np.round(np.abs(normal(MEAN, DEVIATION)))
    # Exponential distribution
    elif SIMULATION_DISTRIBUTION == 3:
        return np.round(np.abs(exponential(SCALE)))