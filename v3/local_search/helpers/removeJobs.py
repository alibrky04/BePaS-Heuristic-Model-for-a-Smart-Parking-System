from v3.local_search import Constants as cnst


def removeJobs(machine_list):
    for machine in machine_list:
        for job in list(machine.assigned_jobs.values()):
            job.duration -= cnst.TIME_BETWEEN_ROUNDS
            if job.duration <= 0:
                machine.removeJob(job.number)
