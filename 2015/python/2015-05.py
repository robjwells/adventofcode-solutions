#!/usr/local/bin/python3

import re


def is_nice(candidate):
    """Check if candidate string passes nice rules

    Returns True if a string is nice, and False otherwise.

    A 'nice' string has the following properties:
      *  It contains at least three vowels [aeiou]
      *  It contains one letter that appears twice in a row
      *  It does not contain the strings [ab, cd, pq, xy]

    Nice strings much have all of these properties.
    """
    vowels = set('aeiou')
    enough_vowels = len([c for c in candidate if c in vowels]) >= 3

    has_double_char = any(a == b for a, b in zip(candidate, candidate[1:]))

    bad_strings = ['ab', 'cd', 'pq', 'xy']
    no_bad_strings = not [bad for bad in bad_strings if bad in candidate]

    return enough_vowels and has_double_char and no_bad_strings


def test_nice_strings():
    """is_nice validates 'nice' strings matching certain rules

    A 'nice' string has the following properties:
      *  It contains at least three vowels [aeiou]
      *  It contains one letter that appears twice in a row
      *  It does not contain the strings [ab, cd, pq, xy]

    Nice strings much have all of these properties.
    """
    known_nice_strings = [
        'ugknbfddgicrmopn',
        'aaa']
    assert all(is_nice(s) for s in known_nice_strings)


def test_naughty_strings():
    """is_nice rejects strings that are known to be invalid"""
    known_naughty_strings = [
        'jchzalrnumimnmhp',     # no double letter
        'haegwjzuvuyypxyu',     # contains 'xy'
        'dvszwmarrgswjxmb']     # only one vowel
    for naughty_string in known_naughty_strings:
        # Can't shortcut with all because `not None` returns True
        assert is_nice(naughty_string) is not None
        assert not is_nice(naughty_string)


def main(puzzle_input):
    # Part one
    nice_strings = [w for w in puzzle_input if is_nice(w)]
    print(f'Part one, number of nice strings: {len(nice_strings)}')


if __name__ == '__main__':
    with open('../input/2015-05.txt') as input_file:
        puzzle_input = input_file.read().splitlines()

    main(puzzle_input)

    # Part Two
    def new_nice(string):
        has_repeated_pair = re.search(r'(.{2}).*\1', string) is not None
        has_repeat_one_apart = re.search(r'(.).\1', string) is not None
        return has_repeated_pair and has_repeat_one_apart

    new_nice_strings = list(filter(new_nice, lines))
    print('Number of new nice strings:', len(new_nice_strings))
