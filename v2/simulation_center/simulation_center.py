from v2.branch_and_bound import main as bnb_main
from v2.branch_and_bound import Constants as bnb_constants

from v2.genetic import main as genetic_main
from v2.genetic import Constants as genetic_constants

from v2.local_search import main as ls_main
from v2.local_search import Constants as ls_constants

from v2.nearest_lot import main as nl_main
from v2.nearest_lot import Constants as nl_constants

from itertools import product

models_to_run = {
    "branch_and_bound": [bnb_main, bnb_constants],
    "genetic": [genetic_main, genetic_constants],
    "local_search": [ls_main, ls_constants],
    "nearest_lot": [nl_main, nl_constants]
}

distributions = ["NORMAL", "EXPONENTIAL"]
batch_times = [60, 30, 10]

data_folder_path = "v2/simulation_center/data"

if __name__ == "__main__":
    parameters = product(batch_times, distributions, models_to_run.items())

    for batch_time, distribution, (key, model) in parameters:
        path = f"{data_folder_path}/batch_time/{batch_time}/{distribution}/{key}.json"
        print(f"Running {key} with {distribution} distribution and {batch_time} batch time with path {path}")
        model[0].main(distribution, batch_time, path)