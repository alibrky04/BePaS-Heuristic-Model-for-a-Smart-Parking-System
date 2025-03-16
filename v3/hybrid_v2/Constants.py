# Number of simulations to be performed
NUMBER_OF_SIMULATIONS = 20

NUM_OF_TYPES = 5

BATCH_TIME = 60

# unit of time passed each round in minutes
DECAY_PER_ROUND = BATCH_TIME

# {(local search, branch & bound, genetic): local search + branch & bound + genetic = ((60 / DECAY_PER_ROUND) * 48) ^ local search, branch & bound, genetic % DECAY_PER_ROUND = 0 }

# In each simulation certain amount (round) of cars come to lot
# 48 days is the time
# NUMBER_OF_ROUNDS = int((60 / DECAY_PER_ROUND) * 48)
NUMBER_OF_ROUNDS = int((60 / BATCH_TIME) * 48)

# MINIMUM duration of Jobs
MINIMUM_JOB_LENGTH = 1

# Maximum duration of jobs
MAXIMUM_JOB_LENGTH = 5

# Number of Machines
NUMBER_OF_MACHINES = 50

NUMBER_OF_JOBS_PER_ROUND = 50

# population size for genetic algorithm. aka how many candidate solutions we're keeping in each generations
NUMBER_OF_CHROMOSOMES = 20

# number of generations ie how many time we need to mutate solutions to find the optimal one
NUMBER_OF_GEN = 50

# Simulation distribution
SIMULATION_DISTRIBUTION = "UNIFORM"  # 1 = UNIFORM, 2 = NORMAL, 3 = EXPONENTIAL, 4= STATIC

# Simulation distribution parameters
MEAN = 75
DEVIATION = 25

SCALE = 75

BRANCH_BOUND_MODEL_TIME_LIMIT = 5
GENETIC_MODEL_TIME_LIMIT = 5
LOCAL_SEARCH_TIME_LIMIT = 5
SIM_OUTPUT_FILE = "output/simulation.json"


