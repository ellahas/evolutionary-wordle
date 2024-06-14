import string
import numpy as np
from collections import Counter

filepath = './3-letter-words.txt'
TARGET_WORD = "PIC"
MUTATION_RATE = 0.2
WEIGHTS = [5,1]
#TODO incorporate the feedback given by right letter but wrong position

# Load word list from file
def load_word_list(file_path):
    """
    Load a list of words from a specified file.

    Input:
        file_path (str): The path to the file containing the word list.

    Output:
        words (list of str): List of words loaded from the file, converted to uppercase.
    """
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    words = [w.upper() for w in words]
    return words

## Select random words to generate initial population
def generate_population(word_list, population_size, rng):
    """
    Generate an initial population by randomly selecting words from the word list.

    Input:
        word_list (list of str): List of words to choose from.
        population_size (int): Number of words in the initial population.
        rng (numpy.random.Generator): Random number generator.

    Output:
        population (numpy.ndarray): Array of randomly selected words.
    """
    return rng.choice(word_list, population_size)

# Fitness function based on correct letters regardless of position
def calculate_fitness_exact_match(target_word=TARGET_WORD, guess=""):
    """
    Calculate fitness based on the number of identical characters regardless of position.

    Input:
        target_word (str): The word we are trying to evolve towards.
        guess (str): The current word being evaluated.

    Output:
        num_matching_chars (int): Number of characters that match the target word regardless of positions.
    """
    num_matching_chars = sum(1 for expected, actual in zip(target_word, guess) if expected == actual)
    correct_positions = [i for i, (expected, actual) in enumerate(zip(target_word, guess)) if expected == actual]
    return num_matching_chars, correct_positions



# Second fitness function that sums the number of matches (both position and value)
def calculate_fitness_sum_match(target_word=TARGET_WORD, guess=""):
    """
    Calculate fitness based on the sum of matching characters and their positions.

    Input:
        target_word (str): The word we are trying to evolve towards.
        guess (str): The current word being evaluated.

    Output:
        fitness_score (int): Sum of matching characters and their positions.
        placeholder (int): Placeholder value (always 0).
    """
    num_matching_chars = sum(1 for expected, actual in zip(target_word, guess) if expected == actual)
    correct_positions = [i for i, (expected, actual) in enumerate(zip(target_word, guess)) if expected == actual]
    return num_matching_chars+len(correct_positions), 0


#calculate fitness based on weights for yellow and green matches 
def calculate_fitness_weighted_match(target_word, guess, weights = WEIGHTS):
    """
    Calculate fitness based on weighted matches (exact and partial).

    Input:
        target_word (str): The word we are trying to evolve towards.
        guess (str): The current word being evaluated.
        weights (list of int): Weights for exact matches (green) and partial matches (yellow).

    Output:
        fitness_score (int): Weighted fitness score based on matches.
        placeholder (int): Placeholder value (always 0).
    """
    green_weight = weights[0]  # Weight for letters in the correct position
    yellow_weight = weights[1]  # Weight for correct letters in the wrong position
    
    num_matching_chars = 0
    num_yellow_chars = 0
    target_word_list = list(target_word)
    guess_list = list(guess)
    
    # Calculate green matches
    for i, (expected, actual) in enumerate(zip(target_word, guess)):
        if expected == actual:
            num_matching_chars += 1
            target_word_list[i] = None
            guess_list[i] = None
            
    num_matching_chars*=green_weight
    
    # Calculate yellow matches
    for i, actual in enumerate(guess_list):
        if actual and actual in target_word_list:
            num_yellow_chars += 1
            target_word_list[target_word_list.index(actual)] = None
            
    num_yellow_chars*=yellow_weight
    
    fitness_score = num_matching_chars + num_yellow_chars
    return fitness_score, 0


# Select parents based on fitness
def select_parents(population, num_parents, rng, strategy="proportional", fitness_fun=calculate_fitness_exact_match):
    """
    Select parents from the population based on their fitness scores.

    Input:
        population (list of str): The current population of words.
        num_parents (int): Number of parents to select.
        rng (numpy.random.Generator): Random number generator.
        strategy (str): Selection strategy (default is "proportional").
        fitness_fun (function): Fitness function to evaluate individuals.

    Output:
        parents (list of str): List of selected parents.
    """
    parents = []
    if strategy == "proportional":
        fitness_scores = [fitness_fun(target_word = TARGET_WORD, guess = individual)[0] for individual in population]
        if np.sum(fitness_scores) == 0:  # if all words in a population have a fitness of 0, all have equal chance
            prob_scores = np.ones(len(fitness_scores)) / len(fitness_scores)
        else:
            prob_scores = fitness_scores / np.sum(fitness_scores)
        parent_ids = rng.choice(range(len(population)), size=num_parents, p=prob_scores)
        for i in range(num_parents):
            parents.append(population[parent_ids[i]])
    return parents

# Perform crossover between two parents to generate offspring
def crossover(parent1, parent2, rng):
    """
    Perform crossover between two parents to generate two offspring.

    Input:
        parent1 (str): The first parent word.
        parent2 (str): The second parent word.
        rng (numpy.random.Generator): Random number generator.

    Output:
        child1 (str): The first offspring word.
        child2 (str): The second offspring word.
    """
    crossover_point = rng.integers(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Mutate a word by changing letters that are incorrect
def mutate(individual, mutation_rate, target_word, rng, exclude_self=False):
    """
    Mutate a word by changing its letters with a given mutation rate.

    Input:
        individual (str): The word to be mutated.
        mutation_rate (float): Probability of mutating each character.
        target_word (str): The target word we are trying to evolve towards.
        rng (numpy.random.Generator): Random number generator.
        exclude_self (bool): Whether to exclude the original character from the mutation options.

    Output:
        mutated_individual (str): The mutated word.
    """
    mutated_individual = ''
    for i, char in enumerate(individual):
        if char != target_word[i] and rng.random() < mutation_rate:
            new_chars = list(string.ascii_uppercase)
            if exclude_self:
                new_chars.remove(char)
            mutated_individual += rng.choice(new_chars)
        else:
            mutated_individual += char
    return mutated_individual

# Mutate a word by swapping letters or changing to a random letter
def mutate_swap(individual, mutation_rate, target_word, rng, exclude_self=False):
    """
    Mutate a word by swapping its letters or changing them to random letters with a given mutation rate.

    Input:
        individual (str): The word to be mutated.
        mutation_rate (float): Probability of mutating each character.
        target_word (str): The target word we are trying to evolve towards.
        rng (numpy.random.Generator): Random number generator.
        exclude_self (bool): Whether to exclude the original character from the mutation options.

    Output:
        mutated_individual (str): The mutated word.
    """
    mutated_individual = ''
    # how often a mutation is a letter from the word instead of the alphabet is proportional to how many of the letters in the word are in the target word (green or yellow).
    swap_mutation_rate = len(list(set(individual) & set(target_word))) / len(individual)
    for i, char in enumerate(individual):
        if char != target_word[i] and rng.random() < mutation_rate:
            new_chars = []
            if rng.random() < swap_mutation_rate:
                new_chars = list(individual)
            else:
                new_chars = list(string.ascii_uppercase)
            if exclude_self:
                new_chars.remove(char)
            mutated_individual += rng.choice(new_chars)
        else:
            mutated_individual += char
    return mutated_individual

def run(word_list, target_word, population_size, mutation_rate, num_generations, random_generator, mutate_fun=mutate, fitness_fun=calculate_fitness_exact_match, exclude_self=False):
    """
    Run the genetic algorithm to evolve a population of words towards the target word.

    Input:
        word_list (list of str): List of words to choose from.
        target_word (str): The word we are trying to evolve towards.
        population_size (int): Number of words in the population.
        mutation_rate (float): Probability of mutating each character.
        num_generations (int): Number of generations to run the algorithm.
        random_generator (numpy.random.Generator): Random number generator.
        mutate_fun (function): Mutation function to use.
        fitness_fun (function): Fitness function to evaluate individuals.
        exclude_self (bool): Whether to exclude the original character from the mutation options.

    Output:
        generation (int): The generation at which the target word was found.
        population (list of str): The final population of words.
    """
    population = generate_population(word_list, population_size, random_generator)
    for generation in range(num_generations):
        parents = select_parents(population, 2, random_generator, fitness_fun=fitness_fun)
        offspring = []
        while len(offspring) < population_size:
            parent1, parent2 = parents
            child1, child2 = crossover(parent1, parent2, random_generator)
            child1 = mutate_fun(child1, mutation_rate, target_word, random_generator, exclude_self)
            child2 = mutate_fun(child2, mutation_rate, target_word, random_generator, exclude_self)
            offspring.extend([child1, child2])
        population = offspring
        if target_word in population:
            break
    return generation, population
