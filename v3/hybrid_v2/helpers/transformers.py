def turn_assignment_into_chromosome(number_of_job, job_list, best_assignment):
    chromosome_array = [-1 for _ in range(number_of_job)]
    for machine_id, assigment in enumerate(best_assignment):
        for job in assigment:
            for actual_job_index, actual_job in enumerate(job_list):
                if actual_job.job_id == job.job_id:
                    chromosome_array[actual_job_index] = machine_id
    if -1 in chromosome_array:
        raise ValueError("Invalid Conversation check algorithms.")
    return chromosome_array

