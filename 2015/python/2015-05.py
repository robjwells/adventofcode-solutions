#!/usr/bin/env python3
"""Advent of Code 2015, Day 5: Doesn't He Have Intern-Elves For This?"""

import re

import pytest


def is_nice(candidate):
    """Check if candidate string passes nice rules

    Returns True if a string is nice, and False otherwise.

    A 'nice' string has the following properties:
      *  It contains at least three vowels [aeiou]
      *  It contains one letter that appears twice in a row
      *  It does not contain the strings [ab, cd, pq, xy]

    Nice strings must have all of these properties.
    """
    vowels = set('aeiou')
    enough_vowels = len([c for c in candidate if c in vowels]) >= 3

    has_double_char = any(a == b for a, b in zip(candidate, candidate[1:]))

    bad_strings = ['ab', 'cd', 'pq', 'xy']
    no_bad_strings = not [bad for bad in bad_strings if bad in candidate]

    return enough_vowels and has_double_char and no_bad_strings


@pytest.mark.parametrize('nice_string', [
    'ugknbfddgicrmopn',
    'aaa',
    ])
def test_nice_strings(nice_string):
    """is_nice validates 'nice' strings matching certain rules

    A 'nice' string has the following properties:
      *  It contains at least three vowels [aeiou]
      *  It contains one letter that appears twice in a row
      *  It does not contain the strings [ab, cd, pq, xy]

    Nice strings must have all of these properties.
    """
    assert is_nice(nice_string)


@pytest.mark.parametrize('naughty_string', [
    'jchzalrnumimnmhp',  # no double letter
    'haegwjzuvuyypxyu',  # contains 'xy'
    'dvszwmarrgswjxmb',  # only one vowel
    ])
def test_naughty_strings(naughty_string):
    """is_nice rejects strings that are known to be invalid"""
    # Explicit `is not None` check because `not (None)` returns True
    assert is_nice(naughty_string) is not None
    assert not is_nice(naughty_string)


def is_new_nice(candidate):
    """Check if candidate string passes new nice rules

    Returns True if a string is nice, and False otherwise.

    New nice strings have both of the following properties:
      *  Contain a pair of letters that repeats without overlapping
      *  Contains one letter that repeats after exactly one letter
    """
    has_repeated_pair = re.search(r'(.{2}).*\1', candidate) is not None
    has_repeat_one_apart = re.search(r'(.).\1', candidate) is not None
    return has_repeated_pair and has_repeat_one_apart


@pytest.mark.parametrize('nice_string', [
    'qjhvhtzxzqqjkmpb',
    'xxyxx',
    ])
def test_new_nice(nice_string):
    """is_new_nice validates according to second set of rules

    New nice strings match the following rules:
      *  Contain a pair of letters that repeats without overlapping
      *  Contains one letter that repeats after exactly one letter
    """
    assert is_new_nice(nice_string)


@pytest.mark.parametrize('naughty_string', [
    'uurcxstgmygtbstg',
    'ieodomkazucvgmuy',
    ])
def test_new_nice_naughty_strings(naughty_string):
    """Strings that don't match the new nice rules return False"""
    # Explicit `is not None` check because `not (None)` returns True
    assert is_new_nice(naughty_string) is not None
    assert not is_new_nice(naughty_string)


def main(puzzle_input):
    # Part one
    nice_strings = [s for s in puzzle_input if is_nice(s)]
    print(f'Part one, number of nice strings: {len(nice_strings)}')

    # Part two
    new_nice_strings = [s for s in puzzle_input if is_new_nice(s)]
    print(f'Part two, number of new nice strings: {len(new_nice_strings)}')


if __name__ == '__main__':
    with open('../input/2015-05.txt') as input_file:
        puzzle_input = input_file.read().splitlines()
    main(puzzle_input)
