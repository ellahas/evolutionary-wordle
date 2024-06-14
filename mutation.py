from evolutionary import load_word_list, generate_population, select_parents
from evolutionary import crossover, mutate, calculate_fitness_exact_match
import numpy as np


def change_mutation_rate(generation, strategy, num_generations, N,
                         population, target_word, kappa=1, beta=1):
    """
    Adjust the mutation rate based on the specified strategy.

    Input:
        generation (int): The current generation.
        strategy (str): The strategy to use for adjusting the mutation rate ("deterministic", "num_correct", or "Wang-Tang").
        num_generations (int): Total number of generations.
        N (int): Population size.
        population (list of str): The current population of words.
        target_word (str): The word we are trying to evolve towards.
        kappa (float): Parameter for the "Wang-Tang" strategy (default is 1).
        beta (float): Parameter for the "Wang-Tang" strategy (default is 1).

    Output:
        mutation_rate (float): The adjusted mutation rate.
    """                     
    if strategy == "deterministic":
        mutation_rate = 1/N * (1 + ((generation * (N - 1)) / num_generations))
    if strategy == "num_correct":
        fitnesses = [calculate_fitness_exact_match(target_word, x)[0] for x in population]
        max_fit = max(fitnesses)
        mutation_rate = 1/(N-max_fit)
    if strategy == "Wang-Tang":
        fitnesses = [calculate_fitness_exact_match(target_word, x)[0] for x in population]
        max_fit = np.max(fitnesses) + 1
        min_fit = np.min(fitnesses) + 1
        avg_fit = np.mean(fitnesses) + 1
        mutation_rate = 1/N * (1 + beta * (avg_fit**kappa / ((max_fit - min_fit)**kappa + avg_fit**kappa)))
    return mutation_rate


def run(word_list, target_word, population_size, mutation_rate,
        num_generations, rng, adaptive_strategy="none"):
    population = generate_population(word_list, population_size, rng)
    N = len(population[0])
    for generation in range(num_generations):
        if adaptive_strategy != "none":
            mutation_rate = change_mutation_rate(generation, adaptive_strategy,
                                                 num_generations, N, population, target_word)
        parents = select_parents(population, 2, rng)
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = parents
            child1, child2 = crossover(parent1, parent2, rng)
            child1 = mutate(child1, mutation_rate, target_word, rng)
            child2 = mutate(child2, mutation_rate, target_word, rng)
            offspring.extend([child1, child2])
        population = offspring
        if target_word in population:
            break
    return generation, population
