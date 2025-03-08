import os
from enum import Enum

from v3.hybrid_v1.Constants import *
from v3.hybrid_v1.formatters import create_section_line, format_parameters, create_machine_lines, create_job_lines, \
    create_machine_state_line, create_machine_state_histogram_line
from v2.genetic.helpers.job_helpers import createDistribution, create_jobs
from v3.hybrid_v1.helpers.configurators import find_combinations_sorted, Algorithm, round_manager
from v3.hybrid_v1.helpers.machine_helpers import create_machines, calculate_tod
from v3.hybrid_v1.helpers.simulation_stat_out import simulation_stat_out
from v3.hybrid_v1.heuristic_models.branch_and_bound import branch_and_bound

from v3.hybrid_v1.heuristic_models.genetic import genetic




if __name__ == "__main__":
    # open file for debug output
    debug_file = open(os.path.join(os.path.dirname(__file__), "output/debug_out.txt"), "w")

    # open file for regular output
    out_file = open(os.path.join(os.path.dirname(__file__), "output/output.txt"), "w")

    # add json file later
    simulation_file = open(os.path.join(os.path.dirname(__file__), SIM_OUTPUT_FILE), "r+")

    solutions = find_combinations_sorted(NUMBER_OF_ROUNDS)

    for i in range(len(solutions)):
        print(solutions[i])

    print(create_section_line("INITIALIZING SIMULATION"), file=debug_file)
    print(create_section_line("PARAMETERS"), "\n", file=debug_file)
    print(format_parameters(), file=debug_file)

    print(create_section_line("WELCOME To SIMULATION"), file=out_file)
    print(create_section_line("PARAMETERS"), "\n", file=out_file)
    print(format_parameters(), file=out_file)
    simulation_data = []
    for simulation in range(len(solutions)):
        print(create_section_line(f"Simulation {simulation + 1}"), "\n", file=debug_file)
        print(create_section_line(f"Simulation {simulation + 1}"), "\n", file=out_file)
        print(create_section_line("Creating Machines"), "\n", file=debug_file)

        machines = create_machines(NUMBER_OF_MACHINES)
        print(create_machine_lines(machines), file=debug_file)

        print(create_section_line("-"), file=debug_file)

        round_results = []

        for round_id in range(1, NUMBER_OF_ROUNDS + 1):
            print("Simulation: ", simulation + 1, " Round: ", round_id, " Algorithm: ", round_manager(solutions[simulation],round_id))
            print(create_section_line(f"Round {round_id}"), "\n", file=debug_file)
            # For rounds after the first, update existing jobs.
            if round_id > 1:
                for machine in machines:
                    machine.update_jobs(DECAY_PER_ROUND)

            # Generate a random number of new jobs for this round.
            random_number_of_jobs = int(createDistribution(NUMBER_OF_JOBS_PER_ROUND))
            new_jobs = create_jobs(random_number_of_jobs, 5, 20, round_id)
            print(create_section_line("Creating Jobs"), "\n", file=debug_file)
            print(create_job_lines(new_jobs), file=debug_file)

            # Sort new jobs by descending length (LPT heuristic) for consistency.
            new_jobs.sort(key=lambda job: job.length, reverse=True)

            # Use the genetic algorithm solver to assign these new jobs.
            round_algorithm = round_manager(solutions[simulation],round_id)
            if round_algorithm == Algorithm.GENETIC:
                best_solution = genetic(new_jobs, machines, NUMBER_OF_MACHINES, pop_size=NUMBER_OF_CHROMOSOMES,
                                        num_gen=NUMBER_OF_GEN, mutation_rate=0.05)
                best_chromosome, best_makespan = best_solution[0], best_solution[1]
                # Update machines with the best assignment:
                # (Since the genetic solver simulated assignment, now we permanently add each new job to its assigned machine.)
                for i, job in enumerate(new_jobs):
                    machines[best_chromosome[i]].add_job(job)
            if round_algorithm == Algorithm.BRANCH_AND_BOUND:
                current_best = [float('inf')]
                best_assignment = [[] for _ in range(NUMBER_OF_MACHINES)]
                branch_and_bound(new_jobs, machines, 0, current_best, best_assignment, NUMBER_OF_MACHINES)

                # Update machines with the best found assignment.
                for i, machine in enumerate(machines):
                    machine.jobs = best_assignment[i]
                    machine.load = sum(job.length for job in machine.jobs)
            if round_algorithm == Algorithm.LOCAL_SEARCH:
                #TODO update locl search algorithm
                pass

            # Calculate a measure (TOD) from the machines after assignment.
            tod = calculate_tod(machines)
            round_results.append(tod)

            print(create_section_line("Machine states after assignment"), "\n", file=debug_file)
            print(create_section_line("Machine States"), "\n", file=debug_file)
            print(create_machine_state_line(machines), file=debug_file)
            print(create_section_line("Machine Histograms"), "\n", file=debug_file)
            print(create_machine_state_histogram_line(machines), file=debug_file)

            print(f"TOD in round {round_id}: {tod}", "\n", file=debug_file)
            print(f"{f'TOD in Simulation {simulation + 1} Round {round_id}:':<32}{tod}", file=out_file)

        simulation_data.append(round_results)
        print(f"Simulation results: {', '.join(map(str, round_results))}", file=out_file)
        simulation_stat_out(round_results, NUMBER_OF_JOBS_PER_ROUND, simulation_file)

    print(create_section_line("Simulation Ended"), "\n", file=debug_file)
