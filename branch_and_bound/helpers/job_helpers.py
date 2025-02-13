import random

import numpy as np
from numpy.random import normal, exponential

from branch_and_bound.Constants import SIMULATION_DISTRIBUTION, MEAN, DEVIATION, SCALE, DECAY_PER_ROUND
from branch_and_bound.models.Job import Job


def create_jobs(number_of_jobs, minimum_job_length, maximum_job_length, round_id):
    new_jobs = []
    for i in range(number_of_jobs):
        job_id = f"R{round_id}_J{i}"
        length = random.randint(minimum_job_length, maximum_job_length)
        duration = random.randint(int(DECAY_PER_ROUND / 2) if DECAY_PER_ROUND > 1 else 1, DECAY_PER_ROUND * 2)
        new_jobs.append(Job(job_id, length, duration))
    return new_jobs


def createDistribution(number_of_jobs):
    if SIMULATION_DISTRIBUTION == "STATIC":
        return number_of_jobs
    if SIMULATION_DISTRIBUTION == "UNIFORM":
        return random.randint(number_of_jobs - int(number_of_jobs / 2) if number_of_jobs > 1 else 1, number_of_jobs * 2)
    elif SIMULATION_DISTRIBUTION == "NORMAL":
        return np.round(np.abs(normal(MEAN, DEVIATION)))
    elif SIMULATION_DISTRIBUTION == "EXPONENTIAL":
        return np.round(np.abs(exponential(SCALE)))
