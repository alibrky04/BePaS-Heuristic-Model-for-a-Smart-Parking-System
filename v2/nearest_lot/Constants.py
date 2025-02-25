# Constants
# Determine different number of jobs that'll be used

# Map size of the simulation
MAP_SIZE = 50

# This is the maximum capacity of a parking lot
MAX_CAPACITY = 500

# Maximum number of days
MAX_DAY = 2

# This is the number of machines
NUM_OF_LOTS = 50

# This is the number of jobs. Only used in uniform distribution
NUM_OF_CARS = 50

# This is the minimum processing time of a job
MIN_PEOPLE = 1

# This is the maximum processing time of a job
MAX_PEOPLE = 5

# This is batch time of rounds by minutes
BATCH_TIME = 10

# This is the length of the simulation. !!! ONLY FOR 1 DAY !!!
MAX_ROUNDS = int((60 / BATCH_TIME) * 24)

# This is the time between rounds
TIME_BETWEEN_ROUNDS = BATCH_TIME

# Number of simulations
NUM_OF_SIMULATIONS = 20

# Distribution generation type
GENERATION_TYPE = 3 # 1 = Discrete, fixed 2 = Discrete, variable 3 = Continuous, fixed 4 = Continuous, variable

# Simulation distribution
SIMULATION_DISTRIBUTION = 2 # 1= uniform, 2 = normal, 3 = exponential

# Simulation distribution parameters
MEAN = 75
DEVIATION = 25

SCALE = 75

# A few non-mandatory constants
COMMAND = ''
DATAFILE = ''

SIM_OUTPUT_FILE = "v2/nearest_lot/output/simulation.json"