import os
import time

from v2.branch_and_bound.formatters import *
from v2.branch_and_bound import Constants as cnst

from v2.branch_and_bound.helpers.job_helpers import create_jobs, createDistribution
from v2.branch_and_bound.helpers.machine_helpers import calculate_tod, create_machines, calculate_makespan
from v2.branch_and_bound.helpers.profiling import profile_function
from v2.branch_and_bound.helpers.simulation_stat_out import simulation_stat_out

from v2.branch_and_bound.heuristic_model.branch_and_bound import branch_and_bound


# ----- Branch and Bound Assignment -----

def main(distribution="UNIFORM", batch_time=60, sim_output_file="output/json", timeLimit=10):
    import random
    import numpy as np

    random.seed(42)
    np.random.seed(42)

    # Initialize parameters
    cnst.SIMULATION_DISTRIBUTION = distribution
    cnst.BATCH_TIME = batch_time
    cnst.NUMBER_OF_ROUNDS = int((60 / batch_time) * 48)
    cnst.DECAY_PER_ROUND = batch_time
    cnst.SIM_OUTPUT_FILE = sim_output_file
    cnst.MODEL_TIME_LIMIT = timeLimit

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
    makespan_data = []

    for simulation in range(cnst.NUMBER_OF_SIMULATIONS):
        print(create_section_line(f"Simulation {simulation + 1}"), "\n", file=debug_file)
        print(create_section_line(f"Simulation {simulation + 1}"), "\n", file=out_file)
        print(create_section_line("Creating Machines"), "\n", file=debug_file)

        machines = create_machines(cnst.NUMBER_OF_MACHINES)
        print(create_machine_lines(machines), file=debug_file)

        print(create_section_line("-"), file=debug_file)

        round_results = []
        profiling_results = []

        for round_id in range(1, cnst.NUMBER_OF_ROUNDS + 1):
            print(create_section_line(f"Round {round_id}"), "\n", file=debug_file)
            # For rounds after the first, update existing jobs.
            if round_id > 1:
                for machine in machines:
                    machine.update_jobs(cnst.DECAY_PER_ROUND)

            # Generate new jobs randomly.
            random_number_of_jobs = int(createDistribution(cnst.NUMBER_OF_JOBS_PER_ROUND))
            print(f"Number of jobs in round {round_id}: {random_number_of_jobs}")
            new_jobs = create_jobs(random_number_of_jobs, cnst.MINIMUM_JOB_LENGTH, cnst.MAXIMUM_JOB_LENGTH, round_id)
            print(create_section_line("Creating Jobs"), "\n", file=debug_file)
            print(create_job_lines(new_jobs), file=debug_file)

            # Sort new jobs by descending length (LPT heuristic).
            new_jobs.sort(key=lambda job: job.length, reverse=True)

            # Run branch and bound to assign these new jobs.
            current_best = [float('inf')]
            best_assignment = [[] for _ in range(cnst.NUMBER_OF_MACHINES)]
            start_time = time.time()
            first_solution_found = [False]
            best_solution, exec_time, cpu_exec_time, memory_usage = profile_function(branch_and_bound, new_jobs,
                                                                                     machines, 0, current_best,
                                                                                     best_assignment,
                                                                                     cnst.NUMBER_OF_MACHINES,
                                                                                     start_time,
                                                                                     cnst.MODEL_TIME_LIMIT,
                                                                                     first_solution_found)

            # Update machines with the best found assignment.
            for i, machine in enumerate(machines):
                machine.jobs = best_assignment[i]
                machine.load = sum(job.length for job in machine.jobs)

            tod = calculate_tod(machines)
            round_results.append(tod)
            makespan_data.append(calculate_makespan(machines))
            profiling_results.append(
                {"exec_time": exec_time, "cpu_exec_time": cpu_exec_time, "memory_usage": memory_usage})

            print(create_section_line("Machine states after assignment"), "\n", file=debug_file)
            print(create_section_line("Machine States"), "\n", file=debug_file)
            print(create_machine_state_line(machines), file=debug_file)
            print(create_section_line("Machine Histograms"), "\n", file=debug_file)
            print(create_machine_state_histogram_line(machines), file=debug_file)

            print(f"TOD in round {round_id}: {tod}", "\n", file=debug_file)
            print(f"TOD in Simulation {simulation + 1} Round {round_id}:".ljust(32) + f"{tod}", file=out_file)

        simulation_data.append(round_results)
        profiling_data.append(profiling_results)
        print(f"Simulation {simulation + 1} results: {', '.join(map(str, round_results))}", file=out_file)
        simulation_stat_out(round_results, random_number_of_jobs, simulation_file, profiling_results,makespan_data)

    print(create_section_line("Simulation Ended"), "\n", file=debug_file)
