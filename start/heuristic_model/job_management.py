from heuristic_model.calculateMakeSpan import calculateMakeSpan
from models.Machine import Machine


def removeAllJobs(machine_list):
    for machine in machine_list:
        cur_jobs = dict(machine.assigned_jobs)
        for key, job in cur_jobs.items():
            if key != job.number:
                print("SOMETHING WENT WRONG")
            num = job.number
            machine.removeJob(num)
            print("REMOVED  -- machine#: ", machine.number, "assigned jobs: ", job)

    print("---------------MACHINES' REMAINING JOB LISTS-----------------------\n")

    for machine in machine_list:
        cur_jobs = dict(machine.assigned_jobs)
        for key, job in cur_jobs.items():
            if key != job.number:
                print("SOMETHING WENT WRONG")
            num = job.number
            print("LEFT  -- machine#: ", machine.number, "assigned jobs: ", job)


def moveJob(origin_machine: Machine, target_machine: Machine, job_to_move):
    # if target_machine.checkDiffTypes() <= 3:  # assuming isLegal already checked, this one is for debug
    cur_job = origin_machine.retrieveJob(job_to_move)
    origin_machine.removeJob(job_to_move)
    target_machine.addJob(cur_job)
    return True


def swapJobs(origin_machine: Machine, target_machine: Machine, origin_job, target_job):
    # if target_machine.checkDiffTypes() <= 3:
    temp = origin_machine.retrieveJob(origin_job)
    origin_machine.removeJob(origin_job)
    target_machine.addJob(temp)
    temp = target_machine.retrieveJob(target_job)
    target_machine.removeJob(target_job)
    origin_machine.addJob(temp)
    return True

def checkSwapSpan(machine_list, job_list ,origin_machine: Machine, target_machine: Machine, origin_job, target_job):
    cur_span = calculateMakeSpan(machine_list)
    origin_span = origin_machine.span
    target_span = target_machine.span
    local_max_span = max(origin_span, target_span)
    origin_job_span = job_list[origin_job].length
    target_job_span = job_list[target_job].length
    new_local_max_span = max(origin_span - origin_job_span + target_job_span,
                             target_span - target_job_span + origin_job_span)
    if new_local_max_span < cur_span:  # by swapping the jobs we won't exceed the current makespan
        if new_local_max_span < local_max_span:
            return True
        else:
            return False
    else:
        return False


def checkMoveSpan(machine_list, job_list, origin_machine: Machine, target_machine: Machine, job_to_move):
    cur_span = calculateMakeSpan(machine_list)
    origin_span = origin_machine.span
    target_span = target_machine.span
    local_max_span = max(origin_span, target_span)
    job_span = job_list[job_to_move].length
    new_local_max_span = max(origin_span - job_span, target_span + job_span)
    if cur_span == target_span:
        return False  # assuming job length is at least 1 , it won't be good to move to that machine, which is already at max span
    elif cur_span > target_span + job_span:  # by moving the job we won't exceed the current max span
        if new_local_max_span < local_max_span:  # if still making an improvement
            return True
        else:
            return False
    else:
        return False


# Moves all the jobs of a given type to another machine
def moveColor(origin_machine: Machine, target_machine: Machine, color_to_move):
    for key, val in origin_machine.assigned_jobs.copy().items():
        if val.type == color_to_move:
            if not moveJob(origin_machine, target_machine, val.number):
                return False

    return True  # something failed


# Check if we should change the color
def checkColorChangeSpan(machine_list, origin_machine: Machine, target_machine: Machine, color_to_move):
    cur_span = calculateMakeSpan(machine_list)
    target_span = target_machine.span

    if cur_span == target_span:
        return False
    elif cur_span > target_span + origin_machine.types_sums[color_to_move - 1]:
        return True
    else:
        return False


# Checks if a move is legal
def isLegalMove(target_machine: Machine, job_type):
    check = target_machine.checkDiffTypes()  # count how many diff types we have on target machine
    if check < 3:
        return True  # we surely have free space so no further checking is needed
    elif check == 3 and job_type in target_machine.getTypes():  # check if the kinds we do have is of the same as new job
        return True
    else:  # might be a mistake - but still check so we don't have more than 3 types
        return False


# Returns how many different types do we have
def howManyTypes(type_hist):
    count = 0
    for t in type_hist:
        if t > 0:
            count = count + 1
    return count


# simulate how many types will be at each machine after swapping 1-1
def swapSim(origin_machine: Machine, target_machine: Machine, origin_job_type, target_job_type):
    origin_type_hist = origin_machine.types.copy()
    target_type_hist = target_machine.types.copy()

    # simulate removing of the jobs
    origin_type_hist[origin_job_type - 1] = origin_type_hist[origin_job_type - 1] - 1
    target_type_hist[target_job_type - 1] = target_type_hist[target_job_type - 1] - 1

    # simulate adding of the jobs
    origin_type_hist[target_job_type - 1] = origin_type_hist[target_job_type - 1] + 1
    target_type_hist[origin_job_type - 1] = target_type_hist[origin_job_type - 1] + 1

    # calculate the new different types count
    types_in_origin = howManyTypes(origin_type_hist)
    types_in_target = howManyTypes(target_type_hist)

    return types_in_origin, types_in_target


# Check if a certain 1-1 swap is legal
def isLegalSwap(origin_machine: Machine, target_machine: Machine, origin_job_type, target_job_type):
    origin_type_count = origin_machine.checkDiffTypes()
    target_type_count = target_machine.checkDiffTypes()

    if origin_type_count < 3 and target_type_count < 3:
        return True  # we surely have free space so no further checking is needed
    if origin_job_type == target_job_type:  # same job type is always legal (might not be worth it , but will be checked later)
        return True
    else:  # at least one of the machines has less than 3 types
        new_origin_count, new_target_count = swapSim(origin_machine, target_machine, origin_job_type, target_job_type)
        if new_target_count > 3 or new_origin_count > 3:  # no can do
            return False
        if new_origin_count <= 3 and new_target_count <= 3:  # we're still fine, probably last of a kind was deducted and added new type
            return True

        if origin_type_count < 3 and target_type_count == 3:
            if new_target_count <= 3:
                return True
        if origin_type_count == 3 and target_type_count < 3:
            if new_origin_count <= 3:
                return True
    return False


# simulate how many types will be at each machine after swapping 2-2
def twoSwapSim(origin_machine: Machine, target_machine: Machine, origin_job_type1, origin_job_type2, target_job_type1,
               target_job_type2):
    origin_type_hist = origin_machine.types.copy()
    target_type_hist = target_machine.types.copy()

    # simulate removing of the jobs
    origin_type_hist[origin_job_type1 - 1] = origin_type_hist[origin_job_type1 - 1] - 1
    origin_type_hist[origin_job_type2 - 1] = origin_type_hist[origin_job_type2 - 1] - 1
    target_type_hist[target_job_type1 - 1] = target_type_hist[target_job_type1 - 1] - 1
    target_type_hist[target_job_type2 - 1] = target_type_hist[target_job_type2 - 1] - 1

    # simulate adding of the jobs
    origin_type_hist[target_job_type1 - 1] = origin_type_hist[target_job_type1 - 1] + 1
    origin_type_hist[target_job_type2 - 1] = origin_type_hist[target_job_type2 - 1] + 1
    target_type_hist[origin_job_type1 - 1] = target_type_hist[origin_job_type1 - 1] + 1
    target_type_hist[origin_job_type2 - 1] = target_type_hist[origin_job_type2 - 1] + 1

    # calculate the new different types count
    types_in_origin = howManyTypes(origin_type_hist)
    types_in_target = howManyTypes(target_type_hist)

    return types_in_origin, types_in_target


# Check if a certain 2-2 swap is legal
def isLegalTwoSwap(origin_machine: Machine, target_machine: Machine, pair1: list, pair2: list):
    if pair1[0] not in origin_machine.assigned_jobs:
        print("d here")
    first = origin_machine.assigned_jobs[pair1[0]]
    second = origin_machine.assigned_jobs[pair1[1]]
    third = target_machine.assigned_jobs[pair2[0]]
    fourth = target_machine.assigned_jobs[pair2[1]]

    origin_type_count = origin_machine.checkDiffTypes()
    target_type_count = target_machine.checkDiffTypes()

    origin_types = origin_machine.getTypes()
    target_types = target_machine.getTypes()

    common_types = set(origin_types).intersection(target_types)

    new_origin_count, new_target_count = twoSwapSim(origin_machine, target_machine, first.type, second.type, third.type,
                                                    fourth.type)

    if new_target_count > 3 or new_origin_count > 3:  # no can do
        return False
    if new_origin_count <= 3 and new_target_count <= 3:  # we're still fine
        return True


# Check if we should do 2-2 swap
def checkTwoSwapSpan(machine_list, origin_machine: Machine, target_machine: Machine, pair1: list, pair2: list):
    first = (origin_machine.assigned_jobs[pair1[0]])
    second = (origin_machine.assigned_jobs[pair1[1]])
    third = (target_machine.assigned_jobs[pair2[0]])
    fourth = (target_machine.assigned_jobs[pair2[1]])

    cur_span = calculateMakeSpan(machine_list)
    origin_span = origin_machine.span
    target_span = target_machine.span
    local_max_span = max(origin_span, target_span)

    new_local_max_span = max(origin_span - first.length - second.length + third.length + fourth.length,
                             target_span - third.length - fourth.length + first.length + second.length)

    if new_local_max_span < cur_span:  # by swapping the jobs we won't exceed the current makespan
        if new_local_max_span < local_max_span:
            return True
        else:
            return False
    else:
        return False


# Swap 2-2 jobs between 2 machines
def swapTwoJobs(origin_machine: Machine, target_machine: Machine, pair1: list, pair2: list):
    first_move = swapJobs(origin_machine, target_machine, pair1[0], pair2[0])
    second_move = swapJobs(origin_machine, target_machine, pair1[1], pair2[1])

    if first_move and second_move:
        return True
    else:
        return False


# Simulate how many types will be at each machine after circular swapping with 3 machines
def circularSwapSim(machine1: Machine, machine2: Machine, machine3: Machine, job1_type, job2_type, job3_type):
    machine1_type_hist = machine1.types.copy()
    machine2_type_hist = machine2.types.copy()
    machine3_type_hist = machine3.types.copy()

    # simulate removing of the jobs
    machine1_type_hist[job1_type - 1] = machine1_type_hist[job1_type - 1] - 1
    machine2_type_hist[job2_type - 1] = machine2_type_hist[job2_type - 1] - 1
    machine3_type_hist[job3_type - 1] = machine3_type_hist[job3_type - 1] - 1

    # simulate adding of the jobs
    machine1_type_hist[job3_type - 1] = machine1_type_hist[job3_type - 1] + 1
    machine2_type_hist[job1_type - 1] = machine2_type_hist[job1_type - 1] + 1
    machine3_type_hist[job2_type - 1] = machine3_type_hist[job2_type - 1] + 1

    # calculate the new different types count
    types_in_first = howManyTypes(machine1_type_hist)
    types_in_second = howManyTypes(machine2_type_hist)
    types_in_third = howManyTypes(machine3_type_hist)

    return types_in_first, types_in_second, types_in_third


# Checks if a certain circular swap is legal
def isLegalCircularSwap(machine1: Machine, machine2: Machine, machine3: Machine, job1, job2, job3):
    first = machine1.assigned_jobs[job1]
    second = machine2.assigned_jobs[job2]
    third = machine3.assigned_jobs[job3]

    new_machine1_count, new_machine2_count, new_machine3_count = circularSwapSim(machine1, machine2, machine3,
                                                                                 first.type, second.type, third.type)

    if new_machine1_count > 3 or new_machine2_count > 3 or new_machine3_count > 3:  # no can do
        return False
    if new_machine1_count <= 3 and new_machine2_count <= 3 and new_machine3_count <= 3:  # we're still fine
        return True


# Check if we should do a circular swap
def checkCircularSwapSpan(machine_list, machine1: Machine, machine2: Machine, machine3: Machine, job1, job2, job3):
    first = machine1.assigned_jobs[job1]
    second = machine2.assigned_jobs[job2]
    third = machine3.assigned_jobs[job3]

    cur_span = calculateMakeSpan(machine_list)
    machine1_span = machine1.span
    machine2_span = machine2.span
    machine3_span = machine3.span

    local_max_span = max(machine1_span, machine2_span, machine3_span)

    new_local_max_span = max(machine1_span - first.length + third.length,
                             machine2_span - second.length + first.length,
                             machine3_span - third.length + second.length)

    if new_local_max_span < cur_span:  # by swapping the jobs we won't exceed the current makespan
        if new_local_max_span < local_max_span:
            return True
        else:
            return False
    else:
        return False


# do a circular swap between 3 machines
def circularSwap(machine1: Machine, machine2: Machine, machine3: Machine, job1, job2, job3):
    first_move = moveJob(machine1, machine2, job1)
    second_move = moveJob(machine2, machine3, job2)
    third_move = moveJob(machine3, machine1, job3)

    if first_move and second_move and third_move:
        return True
    else:
        return False


# if all done return True, else return False
def isDone(d_list):
    return all(item is False for item in d_list)
