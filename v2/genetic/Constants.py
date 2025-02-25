#Number of simulations to be performed
NUMBER_OF_SIMULATIONS = 3

#In each simulation certain amount (round) of cars come to lot
NUMBER_OF_ROUNDS = 10

#MINIMUM duration of Jobs
MINIMUM_JOB_LENGTH = 1

#Maximum duration of jobs
MAXIMUM_JOB_LENGTH = 6

#Number of Machines
NUMBER_OF_MACHINES = 3

NUMBER_OF_JOBS_PER_ROUND = 10

# unit of time passed each round
DECAY_PER_ROUND = 10

# population size for genetic algorithm. aka how many candidate solutions we're keeping in each generations
NUMBER_OF_CHROMOSOMES = 20

# number of generations ie how many time we need to mutate solutions to find the optimal one
NUMBER_OF_GEN = 50

# Simulation distribution
SIMULATION_DISTRIBUTION = "STATIC" # 1 = UNIFORM, 2 = NORMAL, 3 = EXPONENTIAL, 4= STATIC

# Simulation distribution parameters
MEAN = 16
DEVIATION = 2

SCALE = 16

SIM_OUTPUT_FILE = "output/simulation.json"