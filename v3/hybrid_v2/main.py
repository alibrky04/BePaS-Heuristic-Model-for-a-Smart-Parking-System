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
from v3.hybrid_v2.heuristic_models.branch_and_bound import branch_and_bound

from v3.hybrid_v2.heuristic_models.genetic import genetic

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
            random_number_of_jobs = int(createDistribution(cnst.NUMBER_OF_JOBS_PER_ROUND))
            new_jobs = create_jobs(random_number_of_jobs, 5, 20, round_id)
            print(create_section_line("Creating Jobs"), "\n", file=debug_file)
            print(create_job_lines(new_jobs), file=debug_file)
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
            for i, machine in enumerate(machines):
                machine.jobs = best_assignment[i]
                machine.load = sum(job.length for job in machine.jobs)
            tod = calculate_tod(machines)
            print(tod)
            round_results.append(tod)
            profiling_results.append(
                {"exec_time": exec_time, "cpu_exec_time": cpu_exec_time, "memory_usage": memory_usage})

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
    simulation_stat_out(round_results, cnst.NUMBER_OF_JOBS_PER_ROUND, simulation_file,profiling_results)

print(create_section_line("Simulation Ended"), "\n", file=debug_file)
