#Number of simulations to be performed
NUMBER_OF_SIMULATIONS = 20

# This is batch time of rounds by minutes
BATCH_TIME = 60

# In each simulation certain amount (round) of cars come to lot
NUMBER_OF_ROUNDS = int((60 / BATCH_TIME) * 48)

# MINIMUM duration of Jobs
MINIMUM_JOB_LENGTH = 1

# Maximum duration of jobs
MAXIMUM_JOB_LENGTH = 5

# Number of Machines
NUMBER_OF_MACHINES = 250

NUMBER_OF_JOBS_PER_ROUND = 250

DECAY_PER_ROUND = BATCH_TIME

# Simulation distribution
SIMULATION_DISTRIBUTION = "UNIFORM" # 1 = UNIFORM, 2 = NORMAL, 3 = EXPONENTIAL, 4= STATIC

# Simulation distribution parameters
MEAN = 75
DEVIATION = 25

SCALE = 75

# Time limit for the model in seconds
MODEL_TIME_LIMIT = 30

SIM_OUTPUT_FILE = "output/simulation.json"