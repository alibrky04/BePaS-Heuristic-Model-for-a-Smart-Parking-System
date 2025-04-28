import os
import time

from v3.genetic.formatters import *
from v3.genetic import Constants as cnst
from v3.genetic.helpers.job_helpers import createDistribution, create_jobs
from v3.genetic.helpers.machine_helpers import create_machines, calculate_tod
from v3.genetic.helpers.profiling import profile_function
from v3.genetic.helpers.simulation_stat_out import simulation_stat_out
from v3.genetic.heuristic_model.genetic import genetic

if __name__ == '__main__':
    import random
    import numpy as np

    random.seed(42)
    np.random.seed(42)

    # Initialize parameters
    cnst.SIMULATION_DISTRIBUTION = cnst.SIMULATION_DISTRIBUTION
    cnst.BATCH_TIME = cnst.BATCH_TIME
    cnst.NUMBER_OF_ROUNDS = cnst.NUMBER_OF_ROUNDS
    cnst.DECAY_PER_ROUND = cnst.DECAY_PER_ROUND
    cnst.SIM_OUTPUT_FILE = cnst.SIM_OUTPUT_FILE

    # open file for debug output
    debug_file = open(os.path.join(os.path.dirname(__file__), "output/debug_out.txt"), "w")

    # open file for regular output
    out_file = open(os.path.join(os.path.dirname(__file__), "output/output.txt"), "w")

    # add json file later
    simulation_file = open(cnst.SIM_OUTPUT_FILE, "r+")

    print(create_section_line("INITIALIZING SIMULATION"), file=debug_file)
    print(create_section_line("PARAMETERS"), "\n", file=debug_file)
    print(format_parameters(), file=debug_file)

    print(create_section_line("WELCOME To SIMULATION"), file=out_file)
    print(create_section_line("PARAMETERS"), "\n", file=out_file)
    print(format_parameters(), file=out_file)
    simulation_data = []
    profiling_data = []
    for simulation in range(cnst.NUMBER_OF_SIMULATIONS):
        print(create_section_line(f"Simulation {simulation + 1}"), "\n", file=debug_file)
        print(create_section_line(f"Simulation {simulation + 1}"), "\n", file=out_file)
        print(create_section_line("Creating Machines"), "\n", file=debug_file)

        machines = create_machines(cnst.NUMBER_OF_MACHINES)
        print(create_machine_lines(machines), file=debug_file)

        print(create_section_line("-"), file=debug_file)

        round_results = []
        profiling_results = []
        makespan_data = []
        for round_id in range(1, cnst.NUMBER_OF_ROUNDS + 1):
            print(create_section_line(f"Round {round_id}"), "\n", file=debug_file)
            # For rounds after the first, update existing jobs.
            if round_id > 1:
                for machine in machines:
                    machine.update_jobs(cnst.DECAY_PER_ROUND)

            # Generate a random number of new jobs for this round.
            random_number_of_jobs = int(createDistribution(cnst.NUMBER_OF_JOBS_PER_ROUND))
            new_jobs = create_jobs(20, cnst.MINIMUM_JOB_LENGTH, cnst.MAXIMUM_JOB_LENGTH, round_id)
            print(f"Number of jobs in round {round_id}: {20}")
            print(create_section_line("Creating Jobs"), "\n", file=debug_file)
            print(create_job_lines(new_jobs), file=debug_file)

            # Sort new jobs by descending length (LPT heuristic) for consistency.
            new_jobs.sort(key=lambda job: job.length, reverse=True)
            best_solution, exec_time, cpu_exec_time, memory_usage = profile_function(genetic, new_jobs, machines,
                                                                                     cnst.NUMBER_OF_MACHINES,
                                                                                     cnst.MODEL_TIME_LIMIT,
                                                                                     pop_size=cnst.NUMBER_OF_CHROMOSOMES,
                                                                                     mutation_rate=0.05)
            best_chromosome, best_makespan = best_solution[0], best_solution[1]

            # Update machines with the best assignment:
            # (Since the genetic solver simulated assignment, now we permanently add each new job to its assigned machine.)
            print(best_chromosome)
            print(new_jobs)
            for i, job in enumerate(new_jobs):
                print(f"i = {i} : {job} Best assignment: {best_chromosome[i]}")
                machines[best_chromosome[i]].add_job(job)

            print(machines)


            # Calculate a measure (TOD) from the machines after assignment.
            tod = calculate_tod(machines)
            round_results.append(tod)
            makespan_data.append(best_makespan)
            profiling_results.append(
                {"exec_time": exec_time, "cpu_exec_time": cpu_exec_time, "memory_usage": memory_usage})

            print(create_section_line("Machine states after assignment"), "\n", file=debug_file)
            print(create_section_line("Machine States"), "\n", file=debug_file)
            print(create_machine_state_line(machines), file=debug_file)
            print(create_section_line("Machine Histograms"), "\n", file=debug_file)
            print(create_machine_state_histogram_line(machines), file=debug_file)

            print(f"TOD in round {round_id}: {tod}", "\n", file=debug_file)
            print(f"{f'TOD in Simulation Round {round_id}:':<32}{tod}", file=out_file)

        simulation_data.append(round_results)
        profiling_data.append(profiling_results)
        print(f"Simulation results: {', '.join(map(str, round_results))}", file=out_file)
        simulation_stat_out(round_results, random_number_of_jobs, simulation_file, profiling_results,makespan_data)

    print(create_section_line("Simulation Ended"), "\n", file=debug_file)
