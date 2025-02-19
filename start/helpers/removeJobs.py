from Constants import TIME_BETWEEN_ROUNDS

def removeJobs(machine_list):
    for machine in machine_list:
        for job in list(machine.assigned_jobs.values()):
            job.duration -= TIME_BETWEEN_ROUNDS
            print(machine.span)
            if job.duration <= 0:
                machine.removeJob(job.number)
            print("-" + str(machine.span))