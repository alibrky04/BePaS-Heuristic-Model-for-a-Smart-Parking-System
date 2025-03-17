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
from v3.hybrid_v2.helpers.machine_helpers import calculate_tod, calculate_tod_alien,calculate_tod_branch_and_bound, create_machines_alien, removeJobs
from v3.hybrid_v2.helpers.profiling import profile_function
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

    print(create_section_line("INITIALIZING SIMULATION"), file=debug_file)
    print(create_section_line("PARAMETERS"), "\n", file=debug_file)
    print(format_parameters(), file=debug_file)

    print(create_section_line("WELCOME To SIMULATION"), file=out_file)
    print(create_section_line("PARAMETERS"), "\n", file=out_file)
    print(format_parameters(), file=out_file)
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
        profiling_results = {'local_search': [], 'branch_and_bound': [], 'genetic': []}
        make_span_results = {'local_search': [], 'branch_and_bound': [], 'genetic': [], 'final': []}
        tod_span_results = {'local_search': [], 'branch_and_bound': [], 'genetic': [], 'final': []}

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
            _, local_search_exec_time, local_search_cpu_exec_time, local_search_memory_usage = profile_function(
                localSearch, simulation_machines_alien, cnst.NUMBER_OF_MACHINES, new_jobs_alien, random_number_of_jobs,
                cnst.LOCAL_SEARCH_TIME_LIMIT)
            profiling_results["local_search"].append(
                {"exec_time": local_search_exec_time, "cpu_exec_time": local_search_cpu_exec_time,
                 "memory_usage": local_search_memory_usage})
            local_search_makespan = calculateMakeSpan(simulation_machines_alien)
            local_search_tod = calculate_tod_alien(simulation_machines_alien)

            assignment = turn_locals_solution_into_assigment(machines_native, simulation_machines_alien,
                                                             new_jobs_native)
            current_best = [float(local_search_makespan)]
            # This is the output of B&B
            best_assignment = [*assignment]
            start_time = time.time()

            _, branch_and_bound_exec_time, branch_and_bound_cpu_exec_time, branch_and_bound_memory_usage = profile_function(
                branch_and_bound, new_jobs_native,
                machines_native, 0, current_best,
                best_assignment,
                cnst.NUMBER_OF_MACHINES,
                start_time,
                cnst.BRANCH_BOUND_MODEL_TIME_LIMIT)

            transformed_chromosome = turn_assignment_into_chromosome(random_number_of_jobs, new_jobs_native,
                                                                     best_assignment)
            profiling_results["branch_and_bound"].append(
                {"exec_time": branch_and_bound_exec_time, "cpu_exec_time": branch_and_bound_cpu_exec_time,
                 "memory_usage": branch_and_bound_memory_usage})
            # makespan for branch bound

            branch_bound_makespan = int(current_best[0])
            branch_and_bound_tod = calculate_tod_branch_and_bound(machines_native, best_assignment)

            genetic_solution, genetic_exec_time, genetic_cpu_time, genetic_memory_usage = (profile_function
                                                                                           (genetic_hybrid,
                                                                                            new_jobs_native,
                                                                                            machines_native,
                                                                                            cnst.NUMBER_OF_MACHINES,
                                                                                            cnst.GENETIC_MODEL_TIME_LIMIT,
                                                                                            transformed_chromosome,
                                                                                            pop_size=cnst.NUMBER_OF_CHROMOSOMES,
                                                                                            mutation_rate=0.05))
            best_solution, genetic_makespan = genetic_solution
            profiling_results["genetic"].append(
                {"exec_time": genetic_exec_time, "cpu_exec_time": genetic_cpu_time,
                 "memory_usage": genetic_memory_usage})

            best_chromosome, best_makespan = best_solution[0], best_solution[1]



            # Update according to genetic chromosomes since final result is coming from genetic algorithm
            for i, job in enumerate(new_jobs_native):
                machines_native[best_chromosome[i]].add_job(job)

            data_machine = turn_chromosome_into_machines(machines_alien, round_id, new_jobs_native, new_jobs_alien,
                                                         best_chromosome)
            if round_id == 0:
                machine_adapter.machines_alien = copy.deepcopy(data_machine)
            else:
                for j in range(cnst.NUMBER_OF_MACHINES):
                    machine_adapter.machines_alien[j].span = data_machine[j].span
                    recent_round_assignments = {**data_machine[j].assigned_jobs}
                    previous_assignments = machine_adapter.machines_alien[j].assigned_jobs
                    machine_adapter.machines_alien[j].assigned_jobs = {**previous_assignments,
                                                                       **recent_round_assignments}
                    machine_adapter.machines_alien[j].types = data_machine[j].types.copy()
                    machine_adapter.machines_alien[j].types_sums = data_machine[j].types_sums.copy()

            tod = calculate_tod(machines_native)

            make_span_results["local_search"].append(local_search_makespan)
            make_span_results["branch_and_bound"].append(branch_bound_makespan)
            make_span_results["genetic"].append(genetic_makespan)
            make_span_results["final"].append(genetic_makespan)

            tod_span_results["local_search"].append(local_search_tod)
            tod_span_results["branch_and_bound"].append(branch_and_bound_tod)
            tod_span_results["genetic"].append(tod)
            tod_span_results["final"].append(tod)

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

            print(f"TOD in round {round_id}: {tod}", "\n", file=debug_file)
        print(f"{f'TOD in Simulation {simulation + 1} Round {round_id}:':<32}{tod}", file=out_file)

        profiling_data.append(profiling_results)
        print(f"Simulation results: {', '.join(map(str, round_results))}", file=out_file)
        simulation_stat_out(round_results, cnst.NUMBER_OF_JOBS_PER_ROUND, simulation_file, profiling_results, make_span_results,tod_span_results)

print(create_section_line("Simulation Ended"), "\n", file=debug_file)
