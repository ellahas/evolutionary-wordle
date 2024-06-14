def brute_force_memory(word_list, target_word):
    for iteration, word in enumerate(word_list):
        if word == target_word:
            return iteration + 1, word
    return len(word_list), None


def brute_force_random_guesses(word_list, target_word, max_i, rng):
    for i in range(max_i):
        guess = rng.choice(word_list)
        if guess == target_word:
            return i + 1, guess
    return max_i, None