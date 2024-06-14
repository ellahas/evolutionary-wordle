# Natural Computing Project: Evolutionary Algorithms for WORDLE


This project explores different ways to employ mutation and fitness functions to find a target word.

## Usage

### File contents

The core functionality can be found in ```evolutionary.py```. Here you find functions to load word lists, generate an initial population, calculate different types of fitness scores, perform crossover and different kinds of mutation.
It also includes an implementation of ```run```, which takes care of the evolutionary loop. It takes a mutation and fitness function as input, so different functions can be compared.

The fitness functions are:

- ```calculate_fitness_exact_match```, based only on the number of fully correct (green) letters,
- ```calculate_fitness_sum_match```, based on the number of fully correct (green) and correct but in the wrong place (yellow) letters,
- ```calculate_fitness_weighted_match```, like the previous one but green letters are weighted more than yellow letters.

The mutation strategies are:

- ```mutate```, which swaps each character which is mutated for any letter in the alphabet,
- ```mutate_swap```, which swaps some characters for any letter in the alphabet and others with a letter from the word itself.

Both mutation functions have a keyword ```exclude_self``` which regulates whether a mutation is allowed to swap a letter for the same letter. This may be particularly important in the case of ```mutate_swap``` where the number of choices for a letter within the word is much lower than in the whole alphabet, and so the odds of swapping for oneself are much higher.

In ```mutation.py```, a function to adaptively change the mutation rate is implemented. There are three different adaptive strategies included:

- ```"deterministic"```, a deterministic function (Bandaru et al., 2011),
- ```"num_correct"```, a function based on the number of correct letters in the best guess of the population,
- ```"Wang-Tang"```, a strategy based on the distribution of fitness scores in the population (Wang & Tang, 2011).

Also a ```run``` function is included that loops through the generations using adaptive mutation rates, if a keyword is passed.

Brute force algorithms to compare against are implemented in ```Brute_force_algorithm5.py```.

A timed test of different algorithms is implemented in ```test.py``` and ```test_mutation_adaptation.py```. Boxplots with the results are plotted with ```plot_comparisons.py``` and ```plot_comparisons_mutation_adapt.py```.

Two word lists are included, one of 3-letter words (adapted from []()), and one of 5-letter words (from [here](https://github.com/charlesreid1/five-letter-words/blob/master/sgb-words.txt)).

### Example use

The code is used by calling one of the ```run``` functions according to your needs.

If you want to give a different or custom fitness function and/or mutation strategy, use ```run``` from ```evolutionary.py```:

``` python
import numpy as np
from evolutionary import load_word_list, mutate_swap, calculate_fitness_weighted, run

filepath = "path/to/word/list"
word_list = load_word_list(file_path=filepath)
random_generator = np.random.default_rng(10)
TARGET_WORD = random_generator.choice(word_list)
print(TARGET_WORD)
generation, population = run(word_list, TARGET_WORD, population_size=10, mutation_rate=1/5, num_generations=500, random_generator=random_generator, mutate_fun=mutate_swap, fitness_fun=calculate_fitness_weighted)
print("generation:", generation)
print("final population:", population)

output:
DIPPY
generation: 39
final population: ['DIPPI', 'DIPPD', 'DIPPD', 'DIPPD', 'DIPPD', 'DIPPI', 'DIPPB', 'DIPPD', 'DIPPY', 'DIPPD']
```

Alternatively, the ```run``` function from ```mutation.py``` can be used to run different mutation adaptation approaches with the "basic" fitness and mutation functions. Example:

``` python
import numpy as np
from evolutionary import load_word_list
from mutation import run

word_list = load_word_list(file_path=filepath)
random_generator = np.random.default_rng(10)
TARGET_WORD = random_generator.choice(word_list)
print(TARGET_WORD)
generation, population = run(word_list, TARGET_WORD, population_size=10, mutation_rate=1/5, num_generations=500, rng=random_generator, adaptive_strategy="Wang-Tang")
print("generation:", generation)
print("final population:", population)

output:
DIPPY
generation: 45
final population: ['DIBPY', 'DIEPY', 'DIHPY', 'DISPY', 'DIBPY', 'DIEPY', 'DIZPY', 'DIPPY', 'DIEPY', 'DIQPY']
```

An example use in which different settings are timed can be found in ```test.py```.

## Authors
This project is coded by Anushree Ganesh, Ella Has, and Richard Schwartzkopf.

## References

Bandaru, S., Tulshyan, R., & Deb, K. (2011, June). Modified SBX and adaptive mutation for real world single objective optimization. In _2011 IEEE Congress of Evolutionary Computation (CEC)_ (pp. 1335-1342). IEEE.

Wang, L., & Tang, D. B. (2011). An improved adaptive genetic algorithm based on hormone modulation mechanism for job-shop scheduling problem. _Expert Systems with Applications._