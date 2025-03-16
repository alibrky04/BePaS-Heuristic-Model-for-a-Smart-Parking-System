import random
import time

from v3.hybrid_v2 import Constants as cnst


def genetic_create_chrom(new_jobs, machines, number_of_machines):
    """
    Create one chromosome. Each gene is a machine index assigned to the corresponding new job.
    We simulate an assignment by temporarily adding the job to a machine and then removing it.
    """
    chrom = [None] * len(new_jobs)
    for i, job in enumerate(new_jobs):
        legal = False
        while not legal:
            machine_index = random.randint(0, number_of_machines - 1)
            chrom[i] = machine_index
            machines[machine_index].add_job(job)
            # If the machine state is legal, accept this assignment.
            if machines[machine_index].__repr__():
                legal = True
            else:
                machines[machine_index].remove_job(job)
        # Remove job to restore machine state for further simulation.
        machines[chrom[i]].remove_job(job)
    return chrom


def genetic_evaluate(chrom, new_jobs, machines):
    """
    Simulate adding the new_jobs to machines according to the chromosome assignment,
    then return the makespan (maximum machine load). After evaluation, remove the jobs.
    """
    for i, job in enumerate(new_jobs):
        machines[chrom[i]].add_job(job)
    makespan = max(machine.load for machine in machines)
    for i, job in enumerate(new_jobs):
        machines[chrom[i]].remove_job(job)
    return makespan


def genetic_create_pop(new_jobs, machines, number_of_machines, pop_size):
    pop = []
    for _ in range(pop_size):
        chrom = genetic_create_chrom(new_jobs, machines, number_of_machines)
        eval_val = genetic_evaluate(chrom, new_jobs, machines)
        pop.append([chrom, eval_val])
    return pop


def genetic_selection(pop):
    """
    Select two parents using tournament selection from the top half.
    """
    sorted_pop = sorted(pop, key=lambda x: x[1])
    parent1 = random.choice(sorted_pop[:len(sorted_pop) // 2])[0]
    parent2 = random.choice(sorted_pop[:len(sorted_pop) // 2])[0]
    return parent1, parent2


def genetic_crossover(parent1, parent2):
    """
    One-point crossover between two parents.
    """
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


def genetic_mutate(chrom, mutation_rate, number_of_machines):
    """
    For each gene, with probability mutation_rate, assign a new random machine.
    """
    new_chrom = chrom[:]
    for i in range(len(new_chrom)):
        if random.random() < mutation_rate:
            new_chrom[i] = random.randint(0, number_of_machines - 1)
    return new_chrom


def genetic(new_jobs, machines, number_of_machines, time_limit, pop_size=cnst.NUMBER_OF_CHROMOSOMES,
            mutation_rate=0.05):
    """
    Solve the assignment of new_jobs to machines using a genetic algorithm.
    Returns the best chromosome (assignment) and its makespan.
    """
    start_time = time.time()
    pop = genetic_create_pop(new_jobs, machines, number_of_machines, pop_size)
    best = min(pop, key=lambda x: x[1])
    gen = 0
    while True:
        if time.time() - start_time >= time_limit:
            break
        gen += 1
        new_pop = []
        while len(new_pop) < pop_size:
            parent1, parent2 = genetic_selection(pop)
            child1, child2 = genetic_crossover(parent1, parent2)
            child1 = genetic_mutate(child1, mutation_rate, number_of_machines)
            child2 = genetic_mutate(child2, mutation_rate, number_of_machines)
            eval1 = genetic_evaluate(child1, new_jobs, machines)
            eval2 = genetic_evaluate(child2, new_jobs, machines)
            new_pop.append([child1, eval1])
            new_pop.append([child2, eval2])
        pop = new_pop[:pop_size]
        current_best = min(pop, key=lambda x: x[1])
        if current_best[1] < best[1]:
            best = current_best
    print(f'number of generations: {gen}')
    return best  # returns [chromosome, makespan]


def genetic_hybrid(new_jobs, machines, number_of_machines, time_limit, best_chromosome,
                   pop_size=cnst.NUMBER_OF_CHROMOSOMES,
                   mutation_rate=0.05):
    """
    Solve the assignment of new_jobs to machines using a genetic algorithm.
    Returns the best chromosome (assignment) and its makespan.
    """
    start_time = time.time()
    pop = genetic_create_pop(new_jobs, machines, number_of_machines, pop_size)
    worst = max(pop, key=lambda x: x[1])
    pop.remove(worst)
    pop.append([best_chromosome, genetic_evaluate(best_chromosome, new_jobs, machines)])
    best = min(pop, key=lambda x: x[1])
    gen = 0
    while True:
        if time.time() - start_time >= time_limit:
            break
        gen += 1
        new_pop = []
        while len(new_pop) < pop_size:
            parent1, parent2 = genetic_selection(pop)
            child1, child2 = genetic_crossover(parent1, parent2)
            child1 = genetic_mutate(child1, mutation_rate, number_of_machines)
            child2 = genetic_mutate(child2, mutation_rate, number_of_machines)
            eval1 = genetic_evaluate(child1, new_jobs, machines)
            eval2 = genetic_evaluate(child2, new_jobs, machines)
            new_pop.append([child1, eval1])
            new_pop.append([child2, eval2])
        pop = new_pop[:pop_size]
        current_best = min(pop, key=lambda x: x[1])
        if current_best[1] < best[1]:
            best = current_best
    return best, genetic_evaluate(best_chromosome, new_jobs, machines)
