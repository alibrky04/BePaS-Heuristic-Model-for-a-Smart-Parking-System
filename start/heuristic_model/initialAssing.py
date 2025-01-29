def initialAssign(job_list, machine_list):
    for j in job_list:
        if j.type == 1 or j.type == 2 or j.type == 3:
            machine_list[0].addJob(j)
        else:
            machine_list[1].addJob(j)