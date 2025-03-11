import os
import time
from enum import Enum

from v3.hybrid_v2 import Constants as cnst
from v3.hybrid_v2.formatters import create_section_line, format_parameters, create_machine_lines, create_job_lines, \
    create_machine_state_line, create_machine_state_histogram_line
from v2.genetic.helpers.job_helpers import createDistribution, create_jobs
from v3.hybrid_v2.helpers.machine_helpers import create_machines, calculate_tod
from v3.hybrid_v2.helpers.profiling import profile_function
from v3.hybrid_v2.helpers.simulation_stat_out import simulation_stat_out
from v3.hybrid_v2.helpers.transformers import turn_assignment_into_chromosome
from v3.hybrid_v2.heuristic_models.branch_and_bound import branch_and_bound

from v3.hybrid_v2.heuristic_models.genetic import genetic, genetic_hybrid

if __name__ == "__main__":
    # open file for debug output
    debug_file = open(os.path.join(os.path.dirname(__file__), "output/debug_out.txt"), "w")
    out_file = open(os.path.join(os.path.dirname(__file__), "output/output.txt"), "w")
    simulation_file = open(os.path.join(os.path.dirname(__file__), cnst.SIM_OUTPUT_FILE), "r+")
    print(create_section_line("INITIALIZING SIMULATION"), file=debug_file)
    print(create_section_line("PARAMETERS"), "\n", file=debug_file)
    print(format_parameters(), file=debug_file)

    print(create_section_line("WELCOME To SIMULATION"), file=out_file)
    print(create_section_line("PARAMETERS"), "\n", file=out_file)
    print(format_parameters(), file=out_file)
    simulation_data = []
    profiling_data = []
    for simulation in range(1):
        print(create_section_line(f"Simulation {simulation + 1}"), "\n", file=debug_file)
        print(create_section_line(f"Simulation {simulation + 1}"), "\n", file=out_file)
        print(create_section_line("Creating Machines"), "\n", file=debug_file)
        machines = create_machines(cnst.NUMBER_OF_MACHINES)
        print(create_machine_lines(machines), file=debug_file)
        print(create_section_line("-"), file=debug_file)
        round_results = []
        profiling_results = []
        for round_id in range(1, 3):
            print(create_section_line(f"Round {round_id}"), "\n", file=debug_file)
            # For rounds after the first, update existing jobs.

            # General algoritmh for updating the decays
            if round_id > 1:
                for machine in machines:
                    machine.update_jobs(cnst.DECAY_PER_ROUND)

            random_number_of_jobs = int(createDistribution(cnst.NUMBER_OF_JOBS_PER_ROUND))
            new_jobs = create_jobs(random_number_of_jobs, 1, 6, round_id)
            print(create_section_line("Creating Jobs"), "\n", file=debug_file)
            print(create_job_lines(new_jobs), file=debug_file)
            current_best = [float('inf')]

            # This is the output of B&B
            best_assignment = [[] for _ in range(cnst.NUMBER_OF_MACHINES)]
            start_time = time.time()
            first_solution_found = [False]

            branch_and_bound(new_jobs, machines, 0, current_best, best_assignment, cnst.NUMBER_OF_MACHINES,
                             start_time, cnst.BRANCH_BOUND_MODEL_TIME_LIMIT, first_solution_found)
            transformed_chromosome = turn_assignment_into_chromosome(random_number_of_jobs, new_jobs, best_assignment)

            best_solution = genetic_hybrid(new_jobs, machines,
                                           cnst.NUMBER_OF_MACHINES,
                                           cnst.GENETIC_MODEL_TIME_LIMIT,
                                           transformed_chromosome,
                                           pop_size=cnst.NUMBER_OF_CHROMOSOMES,
                                           mutation_rate=0.05)
            best_chromosome, best_makespan = best_solution[0], best_solution[1]

            print(f"best {best_assignment}")
            print(f"transformed {transformed_chromosome}")
            print(f"best chromosome {best_chromosome}")

            for i, job in enumerate(new_jobs):
                print(f"i = {i} : {job} Best assignment: {best_chromosome[i]}")
                machines[best_chromosome[i]].add_job(job)

            print(machines)

            tod = calculate_tod(machines)
            print(f"tod:{tod}")
            round_results.append(tod)

        print(create_section_line("Machine states after assignment"), "\n", file=debug_file)
        print(create_section_line("Machine States"), "\n", file=debug_file)
        print(create_machine_state_line(machines), file=debug_file)
        print(create_section_line("Machine Histograms"), "\n", file=debug_file)
        print(create_machine_state_histogram_line(machines), file=debug_file)

        print(f"TOD in round {round_id}: {tod}", "\n", file=debug_file)
        print(f"{f'TOD in Simulation {simulation + 1} Round {round_id}:':<32}{tod}", file=out_file)

    simulation_data.append(round_results)
    profiling_data.append(profiling_results)
    print(f"Simulation results: {', '.join(map(str, round_results))}", file=out_file)
    simulation_stat_out(round_results, cnst.NUMBER_OF_JOBS_PER_ROUND, simulation_file, profiling_results)

print(create_section_line("Simulation Ended"), "\n", file=debug_file)
