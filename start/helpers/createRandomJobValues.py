from random import randint
from Constants import NUM_OF_TYPES
from Constants import TIME_BETWEEN_ROUNDS

def createRandomJobValues(num_of_machines, num_of_jobs, min_processing_time, max_processing_time, first_index):
    inpt = open("input.txt", 'w')

    inpt.write(str(num_of_machines))
    inpt.write("\n")
    inpt.write(str(num_of_jobs))
    inpt.write("\n")
    inpt.write(str(min_processing_time))
    inpt.write("\n")
    inpt.write(str(max_processing_time))
    inpt.write("\n")

    print("number of jobs generated: ", num_of_jobs)
    
    jobs = []
    for index in range(first_index, first_index + num_of_jobs):
        j = []
        j.append(index)
        job_size = randint(min_processing_time, int(max_processing_time))
        j.append(job_size)
        type = randint(1, NUM_OF_TYPES)
        j.append(type)
        duration = randint(1, TIME_BETWEEN_ROUNDS * 2)
        j.append(duration)
        inpt.write(str(index))
        inpt.write(" ")
        inpt.write(str(job_size))
        inpt.write(" ")
        inpt.write(str(type))
        inpt.write("\n")
        jobs.append(j)
    
    inpt.close()

    return jobs