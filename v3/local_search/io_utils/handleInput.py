def handleInput():
    if input("Would you like to generate a new input file? Y/N\n") == "Y":
        num_of_machines = int(input("Please enter the number of machines: \n"))
        min_processing_time = int(input("Please enter the minimum processing time for a single job: \n"))
        max_processing_time = int(input("Please enter the maximum processing time for a single job: \n"))
        num_of_jobs = int(input("Please enter the number of jobs: \n"))

        print("max process time is :", max_processing_time)
        """
         Generate the soon-to-be input file
         input file format will be :

         NUMBER_OF_MACHINES
         JOB_INDEX JOB_SIZE JOB_TYPE

         notice that the total number of jobs will be indicated in the [n-1,0] cell
        """

    # Generate random number of jobs
    else:
        inpt = open("local_search/input.txt", 'r')
        jobs = []
        for index, line in enumerate(inpt):
            if index == 0:
                num_of_machines = int(line)
                print("The number of machines loaded : ", line, "\n")
            elif index == 1:
                num_of_jobs = int(line)
                print("The number of jobs loaded : ", line, "\n")
            elif index == 2:
                min_processing_time = int(line)
                print("The minimum processing time loaded : ", line, "\n")
            elif index == 3:
                max_processing_time = int(line)
                print("The maximum processing time loaded : ", line, "\n")
            else:
                jobs.append(line.split())

        inpt.close()

    return num_of_machines, num_of_jobs, min_processing_time, max_processing_time