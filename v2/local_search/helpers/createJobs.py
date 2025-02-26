from models.Job import Job


def createJobs(unprocessed_jobs, debug_file):
    jobs_dict = {}
    for job in unprocessed_jobs:
        cur_job = Job(int(job[0]), int(job[1]), int(job[2]), int(job[3]))
        print("Created job: index:", cur_job.number, "Length:", cur_job.length, "Type:", cur_job.type, "Duration:",
              cur_job.duration, file=debug_file)
        jobs_dict[cur_job.number] = cur_job
    print("-----------------FINISHED CREATING JOB OBJECTS----------------------\n\n", file=debug_file)
    return jobs_dict
