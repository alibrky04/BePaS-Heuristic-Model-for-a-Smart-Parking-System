from enum import Enum


class Algorithm(Enum):
    LOCAL_SEARCH = 0
    BRANCH_AND_BOUND = 1
    GENETIC = 2


def find_combinations_sorted(total):
    combinations = []
    for local_search in range(total, -1, -1):  # Start from the largest LOCAL_SEARCH
        for branch_and_bound in range(total - local_search, -1, -1):  # Start from the largest BRANCH_AND_BOUND
            genetic = total - local_search - branch_and_bound
            combinations.append({
                Algorithm.LOCAL_SEARCH.name: local_search,
                Algorithm.BRANCH_AND_BOUND.name: branch_and_bound,
                Algorithm.GENETIC.name: genetic
            })
    return combinations


def round_manager(configuration, round_number):
    if round_number <= configuration.get(Algorithm.LOCAL_SEARCH.name):
        return Algorithm.LOCAL_SEARCH
    elif round_number <= configuration.get(Algorithm.LOCAL_SEARCH.name) + configuration.get(
            Algorithm.BRANCH_AND_BOUND.name):
        return Algorithm.BRANCH_AND_BOUND
    elif round_number <= configuration.get(Algorithm.LOCAL_SEARCH.name) + configuration.get(
            Algorithm.BRANCH_AND_BOUND.name) + configuration.get(Algorithm.GENETIC.name):
        return Algorithm.GENETIC
