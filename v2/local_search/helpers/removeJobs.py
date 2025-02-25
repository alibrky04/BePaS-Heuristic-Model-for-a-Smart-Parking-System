from  v1.local_search.Constants import TIME_BETWEEN_ROUNDS

def removeJobs(machine_list):
    for machine in machine_list:
        for job in list(machine.assigned_jobs.values()):
            job.duration -= TIME_BETWEEN_ROUNDS
            if job.duration <= 0:
                machine.removeJob(job.number)