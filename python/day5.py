#!/usr/local/bin/python3

import re

with open('../day5_input.txt') as f:
    lines = [l.rstrip() for l in f.readlines()]


def is_nice(string):
    bad_strings = ['ab', 'cd', 'pq', 'xy']
    for bad in bad_strings:
        if string.find(bad) != -1:
            return False

    vowels = set('aeiou')
    enough_vowels = len([c for c in string if c in vowels]) >= 3

    has_double_char = re.search(r'(.)\1', string) is not None

    return enough_vowels and has_double_char


nice_strings = list(filter(is_nice, lines))
print('Number of nice strings:', len(nice_strings))


# Part Two


def new_nice(string):
    has_repeated_pair = re.search(r'(.{2}).*\1', string) is not None
    has_repeat_one_apart = re.search(r'(.).\1', string) is not None
    return has_repeated_pair and has_repeat_one_apart


new_nice_strings = list(filter(new_nice, lines))
print('Number of new nice strings:', len(new_nice_strings))
