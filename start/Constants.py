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

# This is the number of machines
NUM_OF_MACHINES = 50

# This is the number of jobs. Only used in uniform distribution
NUM_OF_JOBS = 50

# This is the minimum processing time of a job
MIN_PROCESSING_TIME = 1

# This is the maximum processing time of a job
MAX_PROCESSING_TIME = 5

# This is batch time of rounds by minutes
BATCH_TIME = 30

# This is the length of the simulation
MAX_ROUNDS = int((60 / BATCH_TIME) * 48)

# This is the time between rounds
TIME_BETWEEN_ROUNDS = BATCH_TIME

# Number of simulations
NUM_OF_SIMULATIONS = 20

# Simulation distribution
SIMULATION_DISTRIBUTION = 2 # 1 = uniform, 2 = normal, 3 = exponential

# Simulation distribution parameters
MEAN = 75
DEVIATION = 25

SCALE = 100