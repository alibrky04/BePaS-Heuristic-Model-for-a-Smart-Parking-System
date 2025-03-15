import copy
import os
import time

from v3.hybrid_v2 import Constants as cnst
from v3.hybrid_v2.adapters.JobAdapter import JobAdapter
from v3.hybrid_v2.adapters.MachineAdapter import MachineAdapter
from v3.hybrid_v2.formatters import create_section_line, format_parameters, create_machine_lines, create_job_lines, \
    create_machine_state_line, create_machine_state_histogram_line
from v3.hybrid_v2.helpers.job_helpers import createDistribution
from v3.hybrid_v2.helpers.local_search.helper import calculateMakeSpan
from v3.hybrid_v2.helpers.local_search.initialAssing import initialAssign
from v3.hybrid_v2.helpers.local_search.lpt_algorithm import legalLpt
from v3.hybrid_v2.helpers.machine_helpers import calculate_tod, create_machines_alien, removeJobs
from v3.hybrid_v2.helpers.simulation_stat_out import simulation_stat_out
from v3.hybrid_v2.helpers.transformers import turn_assignment_into_chromosome, turn_locals_solution_into_assigment, \
    turn_chromosome_into_machines
from v3.hybrid_v2.heuristic_models.branch_and_bound import branch_and_bound
from v3.hybrid_v2.heuristic_models.genetic import genetic_hybrid
from v3.hybrid_v2.heuristic_models.local_search.local_search_algorithm import localSearch
from v3.local_search.io_utils.printMachineStatOut import printMachineStatOut

if __name__ == "__main__":
    # open file for debug output
    debug_file = open(os.path.join(os.path.dirname(__file__), "output/debug_out.txt"), "w")
    out_file = open(os.path.join(os.path.dirname(__file__), "output/output.txt"), "w")
    simulation_file = open(os.path.join(os.path.dirname(__file__), cnst.SIM_OUTPUT_FILE), "r+")

    # TODO REMOVE THESE UNNECESSARY files
    out_aline_file = open(os.path.join(os.path.dirname(__file__), "output/output_alien.txt"), "w")
    out_debug_file_alien = open(os.path.join(os.path.dirname(__file__), "output/debug_out_alien.txt"), "w")
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

        machine_adapter = MachineAdapter(cnst.NUMBER_OF_MACHINES)
        machines_native = machine_adapter.get_machines_native()
        machines_alien = machine_adapter.get_machines_alien()


        print(create_machine_lines(machines_native), file=debug_file)
        print(create_section_line("-"), file=debug_file)

        round_results = []
        profiling_results = []

        for round_id in range(1, cnst.NUMBER_OF_ROUNDS + 1):
            print(create_section_line(f"Round {round_id}"), "\n", file=debug_file)
            random_number_of_jobs = int(createDistribution(cnst.NUMBER_OF_JOBS_PER_ROUND))
            job_adapter = JobAdapter(random_number_of_jobs, 1, 6, round_id)
            new_jobs_native = job_adapter.get_jobs_native()
            new_jobs_alien = job_adapter.get_jobs_alien()
            simulation_machines_alien = create_machines_alien(cnst.NUMBER_OF_MACHINES, machines_alien, round_id)
            print(create_section_line("Creating Jobs"), "\n", file=debug_file)
            print(create_job_lines(new_jobs_native), file=debug_file)
            printMachineStatOut.out_stat_counter = 0
            if cnst.NUMBER_OF_JOBS_PER_ROUND > 500:
                simulation_machines_alien = legalLpt(new_jobs_native, simulation_machines_alien)
            else:
                initialAssign(new_jobs_alien, simulation_machines_alien)
            localSearch(simulation_machines_alien, cnst.NUMBER_OF_MACHINES, new_jobs_alien, random_number_of_jobs,
                        out_aline_file, out_debug_file_alien, cnst.LOCAL_SEARCH_TIME_LIMIT)
            local_search_makespan = calculateMakeSpan(simulation_machines_alien)


            assignment = turn_locals_solution_into_assigment(machines_native, simulation_machines_alien,
                                                             new_jobs_native)

            current_best = [float(local_search_makespan)]
            # This is the output of B&B
            best_assignment = [*assignment]
            print(f"BEST ASSIGNMENT {best_assignment}")
            start_time = time.time()

            branch_and_bound(new_jobs_native, machines_native, 0, current_best, best_assignment,
                             cnst.NUMBER_OF_MACHINES,
                             start_time, cnst.BRANCH_BOUND_MODEL_TIME_LIMIT)
            transformed_chromosome = turn_assignment_into_chromosome(random_number_of_jobs, new_jobs_native,
                                                                     best_assignment)

            print("_______BRANCH AND BOUND_________")
            print(f"best assignment {best_assignment}")
            print(f"machines native after branch and bound {machines_native}")
            print(f"machines native max makespan after tod {current_best[0]}")
            print("_______BRANCH AND BOUND_________")

            best_solution, genetic_makespan = genetic_hybrid(new_jobs_native, machines_native,
                                           cnst.NUMBER_OF_MACHINES,
                                           cnst.GENETIC_MODEL_TIME_LIMIT,
                                           transformed_chromosome,
                                           pop_size=cnst.NUMBER_OF_CHROMOSOMES,
                                           mutation_rate=0.05)
            best_chromosome, best_makespan = best_solution[0], best_solution[1]

            print(f"transformed {transformed_chromosome}")
            print(f"best chromosome {best_chromosome}")

            # Update according to genetic chromosomes since final result is coming from genetic algorithm
            for i, job in enumerate(new_jobs_native):
                # print(f"i = {i} : {job} Best assignment: {best_chromosome[i]}")
                machines_native[best_chromosome[i]].add_job(job)

            data_machine = turn_chromosome_into_machines(machines_alien, round_id, new_jobs_native, new_jobs_alien,
                                                         best_chromosome)
            if round_id == 0:
                machine_adapter.machines_alien = copy.deepcopy(data_machine)
            else:
                for j in range(cnst.NUMBER_OF_MACHINES):
                    machine_adapter.machines_alien[j].span = data_machine[j].span
                    #
                    # machine_adapter.machines_alien[j].assigned_jobs = {job.number: job for job in
                    #                                                    data_machine[j].assigned_jobs.values()}
                    recent_round_assignments = {**data_machine[j].assigned_jobs}
                    print(f'recent round assignments {recent_round_assignments}')
                    previous_assignments = machine_adapter.machines_alien[j].assigned_jobs
                    machine_adapter.machines_alien[j].assigned_jobs = {**previous_assignments,
                                                                       **recent_round_assignments}
                    machine_adapter.machines_alien[j].types = data_machine[j].types.copy()
                    machine_adapter.machines_alien[j].types_sums = data_machine[j].types_sums.copy()

            print("machine alien after SYNCH :============\n")
            for machine_alien in machines_alien:
                print(f"{machine_alien} \n")

            print(f"Machines after update: {machines_native}")
            tod = calculate_tod(machines_native)
            print(f"tod:{tod}")
            round_results.append(tod)

            print(create_section_line("Machine states after assignment"), "\n", file=debug_file)
            print(create_section_line("Machine States"), "\n", file=debug_file)
            print(create_machine_state_line(machines_native), file=debug_file)
            print(create_section_line("Machine Histograms"), "\n", file=debug_file)
            print(create_machine_state_histogram_line(machines_native), file=debug_file)

            if round_id:
                for machine in machines_native:
                    machine.update_jobs(cnst.DECAY_PER_ROUND)
            removeJobs(machine_adapter.machines_alien)

            print("machine alien after REMOVING DECAYS :============\n")
            for machine_alien in machines_alien:
                print(f"{machine_alien} \n")

        print(f"TOD in round {round_id}: {tod}", "\n", file=debug_file)
        print(f"{f'TOD in Simulation {simulation + 1} Round {round_id}:':<32}{tod}", file=out_file)

    simulation_data.append(round_results)
    profiling_data.append(profiling_results)
    print(f"Simulation results: {', '.join(map(str, round_results))}", file=out_file)
    simulation_stat_out(round_results, cnst.NUMBER_OF_JOBS_PER_ROUND, simulation_file, profiling_results)

print(create_section_line("Simulation Ended"), "\n", file=debug_file)
