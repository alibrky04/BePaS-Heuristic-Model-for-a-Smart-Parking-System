# Constants
# Determine different number of jobs that'll be used
import time

NUM_OF_TYPES = 5

#Project also provides a random job genreation. This parameters determines number of random jobs
# to be created
MAX_NUM_OF_JOBS = 1000

# determines mimimum number of jobs
MIN_NUM_OF_JOBS = 1

# I have no idea what this does rn
file_times = (time.time()/10000)

# This is the length of the simulation
MAX_ROUNDS = 5

# This is the time between rounds
TIME_BETWEEN_ROUNDS = 12

# Number of simulations
NUM_OF_SIMULATIONS = 1

# Simulation distribution
SIMULATION_DISTRIBUTION = 1 # 1 = uniform, 2 = normal, 3 = exponential

# Simulation distribution parameters
MEAN = 150
DEVIATION = 25

SCALE = 150