import random
from random import randint
import v3.hybrid_v2.Constants as cnst
from v3.hybrid_v2.models.Job import Job
from v3.hybrid_v2.models.JobAlien import JobAlien


class JobAdapter:
    def __init__(self, number_of_jobs, minimum_job_length, maximum_job_length, round_id):
        self.jobs_native = []
        self.jobs_alien = {}
        for i in range(number_of_jobs):
            job_id = f"R{round_id}_J{i}"
            job_length = random.randint(minimum_job_length, maximum_job_length)
            job_duration = random.randint(int(cnst.DECAY_PER_ROUND / 2) if cnst.DECAY_PER_ROUND > 1 else 1,
                                          cnst.DECAY_PER_ROUND * 2)
            job_type = randint(1, cnst.NUM_OF_TYPES)
            self.jobs_native.append(Job(job_id, job_length, job_duration))
            self.jobs_alien[job_id] = JobAlien(job_id, job_length, job_type,job_duration)

    def get_jobs_native(self):
        return self.jobs_native

    def get_jobs_alien(self):
        return self.jobs_alien
