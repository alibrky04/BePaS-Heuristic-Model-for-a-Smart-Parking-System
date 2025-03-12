from v3.local_search.heuristic_model.calculateMakeSpan import calculateMakeSpan
from v3.local_search.heuristic_model.job_management import *
from v3.local_search.io_utils.printMachineStatOut import printMachineStatOut
from v3.local_search.models.Machine import Machine


def isDone(d_list):
    return all(item is False for item in d_list)


def oneJobRoutine(machine_list, number_of_machines, job_list, number_of_jobs, output_file, debug_file):
    done = False
    while not done:
        prev_makespan = calculateMakeSpan(machine_list)

        done_list = [False] * number_of_machines  # for checking if at least one job has moved in the last machine iteration
        for index, machine in enumerate(machine_list):
            for job_number, job in machine.assigned_jobs.copy().items():
                for i in range(1, number_of_machines):
                    if isLegalMove(machine_list[(machine.number + i) % number_of_machines], job.type):
                        move_or_not_to_move = checkMoveSpan(machine_list, job_list, machine,
                                                            machine_list[(machine.number + i) % number_of_machines],
                                                            job_number)
                        if move_or_not_to_move is True:
                            moved = moveJob(machine, machine_list[(machine.number + i) % number_of_machines],
                                            job_number)
                            if moved is True:
                                if done_list[machine.number] is False:
                                    done_list[machine.number] = True
                            break

            if number_of_jobs <= 500:
                printMachineStatOut(machine_list, output_file, "Moving one job")
            if prev_makespan > calculateMakeSpan(machine_list):
                print("makespan: ", calculateMakeSpan(machine_list), file=debug_file)
                prev_makespan = calculateMakeSpan(machine_list)

            if isDone(done_list):
                done = True
                break


def colorChangeRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file):
    done = False

    check_count = 0

    # check changing of whole color
    while not done:
        prev_makespan = calculateMakeSpan(machine_list)

        done_list = [
                        False] * number_of_machines  # for checking if at least one job has moved in the last machine iteration
        for index, machine in enumerate(machine_list):
            color_list = machine.getTypes()

            for color in color_list:
                for i in range(1, number_of_machines):
                    if isLegalMove(machine_list[(machine.number + i) % number_of_machines], color):
                        move_or_not_to_move = checkColorChangeSpan(machine_list, machine,
                                                                   machine_list[
                                                                       (machine.number + i) % number_of_machines],
                                                                   color)
                        if move_or_not_to_move is True:
                            moved = moveColor(machine, machine_list[(machine.number + i) % number_of_machines], color)
                            if moved is True:
                                if done_list[machine.number] is False:
                                    done_list[machine.number] = True
                            break

            if number_of_jobs <= 500:
                pass
                # printMachineStatOut(machine_list, output_file, "Color Change")
            if prev_makespan > calculateMakeSpan(machine_list):
                print("makespan: ", calculateMakeSpan(machine_list), file=debug_file)
                prev_makespan = calculateMakeSpan(machine_list)

            if isDone(done_list) or check_count == 100:
                done = True
                break
        check_count += 1


def oneByOneSwapRoutine(machine_list, number_of_machines, job_list, number_of_jobs, output_file, debug_file):
    done = False
    while not done:
        prev_makespan = calculateMakeSpan(machine_list)
        no_swap_count = len(job_list)
        done_list = [
                        False] * number_of_machines  # for checking if at least one job has moved in the last machine iteration
        for index, machine in enumerate(machine_list):  # origin machine
            for job_number, job in machine.assigned_jobs.copy().items():  # origin job
                move_at_least_once = False
                break_flag = False
                for i in range(1, number_of_machines):
                    target_machine = machine_list[(machine.number + i) % number_of_machines]
                    for target_job_number, target_job in target_machine.assigned_jobs.copy().items():
                        moved = False
                        if isLegalSwap(machine, target_machine, job.type,
                                       target_job.type):  # check if origin machine can accept target job and if target machine can accept origin job
                            move_or_not_to_move = checkSwapSpan(machine_list, job_list, machine,
                                                                target_machine,
                                                                job_number, target_job_number)

                            if move_or_not_to_move is True:
                                moved = swapJobs(machine, target_machine, job_number, target_job_number)
                                move_at_least_once = True
                                if moved is True:
                                    break_flag = True
                                    break
                    if break_flag is True:
                        break

                if move_at_least_once is False:
                    no_swap_count = no_swap_count - 1

            if number_of_jobs <= 500:
                pass
                # printMachineStatOut(machine_list, output_file, "Swapping jobs 1 by 1 with 2 machine")

            if prev_makespan > calculateMakeSpan(machine_list):
                print("makespan: ", calculateMakeSpan(machine_list), file=debug_file)
                prev_makespan = calculateMakeSpan(machine_list)

        if no_swap_count == 0:
            done = True
            break


# simply returns a list of all unique pairs from the numbers in the source list
def uniquePairs(source):
    result = []
    for p1 in range(len(source)):
        for p2 in range(p1 + 1, len(source)):
            result.append([source[p1], source[p2]])
    return result


def twoRoutineHelper(machine_list, number_of_machines, debug_file, machine: Machine):
    origin_pairs = uniquePairs(list((machine.assigned_jobs.copy().keys())))

    for pair1 in origin_pairs:

        for i in range(1, number_of_machines):
            target_machine = machine_list[(machine.number + i) % number_of_machines]

            target_pairs = uniquePairs(list(target_machine.assigned_jobs.copy().keys()))

            for pair2 in target_pairs:

                if isLegalTwoSwap(machine, target_machine, pair1,
                                  pair2):  # check if origin machine can accept target job and if target machine can accept origin job
                    move_or_not_to_move = checkTwoSwapSpan(machine_list, machine, target_machine, pair1, pair2)

                    if move_or_not_to_move is True:
                        print("swapping jobs numbers ", pair1[0], pair1[1], "from machine number ", machine.number,
                              "with jobs numbers ", pair2[0], pair2[1], "from machine number ", target_machine.number,
                              file=debug_file)
                        moved = swapTwoJobs(machine, target_machine, pair1, pair2)
                        if moved is True:
                            return True

    return False


def twoByTwoSwapRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file):
    done = False
    machine_one_counter = 0

    while not done:

        prev_makespan = calculateMakeSpan(machine_list)

        # iterate over the machine - 1st machine is passed only if all the jobs in this machine cant be swapped
        for index, machine in enumerate(machine_list):  # 1st machine
            if machine.number == 0:
                machine_one_counter += 1

            # generate all unique jobs pairs in the machine
            swapped = True
            # print("im in machine", machine.number, "final makespan= ", calculateMakeSpan(machine_list))

            while swapped is True:
                swapped = twoRoutineHelper(machine_list, number_of_machines, debug_file, machine)

            if number_of_jobs <= 500:
                pass
                # printMachineStatOut(machine_list,output_file,"Swapping jobs 2 by 2 with 2 machine")
            if prev_makespan > calculateMakeSpan(machine_list):
                print("makespan: ", calculateMakeSpan(machine_list), file=debug_file)
                prev_makespan = calculateMakeSpan(machine_list)
        if machine_one_counter == 2:
            return


def circularSwapHelper(machine_list, number_of_machines):
    # iterate over the machine - 1st machine is passed only if all the jobs in this machine cant be swapped
    for i in range(len(machine_list)):  # 1st machine
        for job1 in machine_list[i].assigned_jobs.keys():
            for j in range((i + 1 % number_of_machines), len(machine_list)):  # machine 2
                for job2 in machine_list[j].assigned_jobs.keys():
                    for k in range((j + 1) % number_of_machines, len(machine_list)):  # machine 3
                        for job3 in machine_list[k].assigned_jobs.keys():

                            if isLegalCircularSwap(machine_list[i], machine_list[j], machine_list[k],
                                                   job1, job2, job3):  # check if the circular swap can be legal
                                move_or_not_to_move = checkCircularSwapSpan(machine_list, machine_list[i],
                                                                            machine_list[j],
                                                                            machine_list[k], job1, job2, job3)

                                if move_or_not_to_move is True:
                                    moved = circularSwap(machine_list[i], machine_list[j], machine_list[k],
                                                         job1, job2, job3)
                                    if moved is True:
                                        return True
    return False


def circularSwapRoutine(machine_list, number_of_machines, number_of_jobs, output_file, debug_file):
    done = False
    no_swap_count = 0

    while not done:
        prev_makespan = calculateMakeSpan(machine_list)

        swapped = True

        while swapped is True:
            swapped = circularSwapHelper(machine_list, number_of_machines)
            if swapped is False:
                no_swap_count += 1

        if number_of_jobs <= 500:
            pass
            # printMachineStatOut(machine_list,output_file,"Circular swap between 3 machines")
        if prev_makespan > calculateMakeSpan(machine_list):
            print("makespan: ", calculateMakeSpan(machine_list), file=debug_file)
            calculateMakeSpan(machine_list)
        if no_swap_count == 2:
            return
