import time
import numpy as np
from tqdm import tqdm
from evolutionary import load_word_list, mutate, mutate_swap, calculate_fitness_sum_match, calculate_fitness_weighted_match, run
from Brute_force_algorithm5 import brute_force_random_guesses, brute_force_memory

folder = "./5-mutation_fitness/"
N = 100
experiments = 11  # number of algorithms you're comparing
random_generator = np.random.default_rng(0)

times = np.zeros((experiments, N))
generations = np.zeros((experiments, N))
individuals = np.zeros((experiments, N))

# define all constants
word_list = load_word_list('./5-letter-words.txt')
print("word list loaded")
pop_size = 10
mutation_rate = 1/5
num_generations = 5000  # should be set high to ensure it can reach an answer almost always


for i in tqdm(range(N)):
    target_word = random_generator.choice(word_list)

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, mutate_fun=mutate)
    end = time.time()
    times[0, i] = end - start
    generations[0, i] = generation
    individuals[0, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, mutate_fun=mutate_swap)
    end = time.time()
    times[1, i] = end - start
    generations[1, i] = generation
    individuals[1, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, mutate_fun=mutate_swap, exclude_self=True)
    end = time.time()
    times[2, i] = end - start
    generations[2, i] = generation
    individuals[2, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, fitness_fun=calculate_fitness_sum_match, mutate_fun=mutate)
    end = time.time()
    times[3, i] = end - start
    generations[3, i] = generation
    individuals[3, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, fitness_fun=calculate_fitness_sum_match, mutate_fun=mutate_swap)
    end = time.time()
    times[4, i] = end - start
    generations[4, i] = generation
    individuals[4, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, fitness_fun=calculate_fitness_sum_match, mutate_fun=mutate_swap, exclude_self=True)
    end = time.time()
    times[5, i] = end - start
    generations[5, i] = generation
    individuals[5, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, fitness_fun=calculate_fitness_weighted_match, mutate_fun=mutate)
    end = time.time()
    times[6, i] = end - start
    generations[6, i] = generation
    individuals[6, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, fitness_fun=calculate_fitness_weighted_match, mutate_fun=mutate_swap)
    end = time.time()
    times[7, i] = end - start
    generations[7, i] = generation
    individuals[7, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, fitness_fun=calculate_fitness_weighted_match, mutate_fun=mutate_swap, exclude_self=True)
    end = time.time()
    times[8, i] = end - start
    generations[8, i] = generation
    individuals[8, i] = pop_size * generation

    start = time.time()
    iterations, word = brute_force_memory(word_list, target_word)
    end = time.time()
    times[-2, i] = end - start
    generations[-2, i] = iterations
    individuals[-2, i] = iterations

    start = time.time()
    iterations, word = brute_force_random_guesses(word_list, target_word, num_generations*pop_size, random_generator)
    end = time.time()
    times[-1, i] = end - start
    generations[-1, i] = iterations
    individuals[-1, i] = iterations

np.save(folder+"times.npy", times)
np.save(folder+"generations.npy", generations)
np.save(folder+"individuals.npy", individuals)
