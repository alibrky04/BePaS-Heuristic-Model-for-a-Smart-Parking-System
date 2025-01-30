from Constants import TIME_BETWEEN_ROUNDS
from time import sleep

def removeJobs(machine_list):
    for _ in range(TIME_BETWEEN_ROUNDS):
            for machine in machine_list:
                for job in list(machine.assigned_jobs.values()):
                    job.duration -= 1
                    if job.duration == 0:
                        machine.removeJob(job.number)
            sleep(1)