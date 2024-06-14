import time
import numpy as np
from tqdm import tqdm
from evolutionary import load_word_list
from Brute_force_algorithm5 import brute_force_random_guesses, brute_force_memory
from mutation import run

folder = "./5-mutation_adaptation/"
N = 100
experiments = 6  # number of algorithms you're comparing
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
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, adaptive_strategy="none")
    end = time.time()
    times[0, i] = end - start
    generations[0, i] = generation
    individuals[0, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, adaptive_strategy="deterministic")
    end = time.time()
    times[1, i] = end - start
    generations[1, i] = generation
    individuals[1, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, adaptive_strategy="num_correct")
    end = time.time()
    times[2, i] = end - start
    generations[2, i] = generation
    individuals[2, i] = pop_size * generation

    start = time.time()
    # run the algorithm until max generations or found result
    generation, population = run(word_list, target_word, pop_size, mutation_rate, num_generations, random_generator, adaptive_strategy="Wang-Tang")
    end = time.time()
    times[3, i] = end - start
    generations[3, i] = generation
    individuals[3, i] = pop_size * generation

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
