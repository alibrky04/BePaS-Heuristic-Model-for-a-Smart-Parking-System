from v2.branch_and_bound import main as bnb_main
from v2.branch_and_bound import Constants as bnb_constants

from v2.genetic import main as genetic_main
from v2.genetic import Constants as genetic_constants

from v2.local_search import main as ls_main
from v2.local_search import Constants as ls_constants

from v2.nearest_lot import main as nl_main
from v2.nearest_lot import Constants as nl_constants

from v3.hybrid_v2 import main as hybrid_main
from v3.hybrid_v2 import Constants as hybrid_constants

from itertools import product

models_to_run = {
    "branch_and_bound": [bnb_main, bnb_constants],
    "genetic": [genetic_main, genetic_constants],
    "local_search": [ls_main, ls_constants],
    "nearest_lot": [nl_main, nl_constants],
    "hybrid": [hybrid_main, hybrid_constants]
}

distributions = ["UNIFORM", "NORMAL", "EXPONENTIAL"]
batch_times = [60, 30, 10]

data_folder_path = "v2/simulation_center/data"

exceptions = []

def batch_time_simulation(folder_name):
    parameters = product(batch_times, distributions, models_to_run.items())

    for batch_time, distribution, (key, model) in parameters:
        if (batch_time, distribution, (key, model)) in exceptions:
            continue
        path = f"{data_folder_path}/{folder_name}/{batch_time}/{distribution}/{key}.json"
        print(f"Running {key} with {distribution} distribution and {batch_time} batch time with path {path}")
        model[0].main(distribution, batch_time, path)

def running_time_simulation(folder_name):
    # TODO: Add time stop to local search

    # TODO: Use local search, branch and bound, and maybe hybrid
    # to change the maximum time they can use to optimize

    # NOTE: Need to increase the number of machines and jobs to make local search take longer,
    # otherwise it will be very fast for the time limits
    pass

if __name__ == "__main__":
    batch_time_simulation("batch_time_2")