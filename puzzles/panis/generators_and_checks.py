import itertools
def generate_keys(key_length, max_key_number,string_between_keys):
    # generate all possible numbers for each key position
    possible_numbers = [str(i) for i in range(1, max_key_number+1)]
    
    # generate all possible key combinations
    key_combinations = itertools.product(possible_numbers, repeat=key_length)
    
    # format each key combination as a string with dots between each number
    formatted_keys = [string_between_keys.join(key) for key in key_combinations]
    
    return formatted_keys

def generate_alphabet(strings):
    all_combinations = itertools.permutations(strings, len(strings))
    return all_combinations

def is_english(text, word_list):
    # with open('english_words.txt') as f:
    #     word_list = set(word.strip().lower() for word in f)
    words = text.lower().split()
    num_english_words = sum(1 for word in words if word in word_list)
    return num_english_words >= len(words) * 0.5

def read_wordlist():
    with open('english_words.txt') as f:
        word_list = set(word.strip().lower() for word in f)
    return word_list
