#!/usr/bin/env python3
"""Advent of Code 2015, Day 19: Medicine for Rudolph"""

import pathlib
import re

input_file = pathlib.Path('../input/2015-19.txt')


def parse_input(text: str) -> (list, str):
    """Return a list of replacement pairs and the molecule string"""
    replacement_block, molecule = text.rstrip().split('\n\n')
    replacement_pairs = [tuple(line.split(' => '))
                         for line in replacement_block.splitlines()]
    return replacement_pairs, molecule


def generate_replacements(molecule: str, replacements: list) -> set:
    """Return set of permutations for the given molecule

    replacements should be a list of (str, str) tuples, with
    the first item being the string to be replaced and
    the second the replacement string.
    """
    generated = set()

    # This is quadratic!
    for find_str, replace_str in replacements:
        for match in re.finditer(find_str, molecule):
            substring_start, substring_end = match.span()
            new_molecule = (molecule[:substring_start] +
                            replace_str +
                            molecule[substring_end:])
            generated.add(new_molecule)

    return generated


def reverse_reps(replacements):
    """Map from replacement to source and reverse each string also

    The string reverse is needed because the steps_to_molecule
    reverses the molecule string itself.
    """
    return {b[::-1]: a[::-1] for a, b in replacements}


def steps_to_molecule(molecule: str, replacements: list):
    """Return the minimum number of replacements needed to make molecule

    This is based off askalski’s solution on Reddit:
    https://www.reddit.com/r/adventofcode/comments/
        3xflz8/day_19_solutions/cy4etju

    This solution processes the molecule in reverse, matches the (reversed)
    replacement elements with their source element and retraces the steps
    back to the original element (which is e).

    The reversal is necessary to avoid backtracking to match sequences
    that end in Ar.
    """
    reps = reverse_reps(replacements)
    # Reverse the molecule so we can consume *Ar sequences
    # without the regex engine backtracking
    molecule = molecule[::-1]
    count = 0

    # e is the original molecule we're trying to reach
    while molecule != 'e':
        # Replace one molecule at a time, using the reps dictionary
        # to find the replacement string
        molecule = re.sub(
            '|'.join(reps.keys()),
            lambda m: reps[m.group()],
            molecule,
            count=1
            )
        count += 1

    return count


def test_replacements():
    test_molecule = 'HOH'
    test_replacements = [
        ('H', 'HO'),
        ('H', 'OH'),
        ('O', 'HH'),
        ]
    result = generate_replacements(molecule=test_molecule,
                                   replacements=test_replacements)
    expected = {'HOOH', 'HOHO', 'OHOH', 'HHHH'}
    assert result == expected


def count(molecule, replacements):
    """This uses a modified version of askalski’s formula to count the steps

    Note that in the following expression we don’t have an exact copy
    of askalski’s formula, which is:

        t - p - 2 * c - 1

    This is because in the above function we’re left over with a
    single token (which doesn’t get reduced by the pattern) matching,
    which correlates with having 'e' left over if you do the step
    by step reduction.

    Having that left over, it doesn’t get added to our totals and
    so we don’t have to subtract 1 from the rest of the calculation
    for the total number of steps.

    (At least, I’m pretty sure that’s how this works :)

    I’ve adapted this solution from one in F# by Yan Cui:
    http://theburningmonk.com/2015/12/advent-of-code-f-day-19/
    """
    # Create a set of all the 'source' elements, with the strings reversed
    reps = {a[::-1] for a, b in replacements}

    def loop(molecule, tokens=0, parens=0, commas=0):
        # Minimum length of the molecule list is 1.
        if len(molecule) == 1:
            return (tokens, parens, commas)

        first, second, *rest = molecule

        if first in ('(', ')'):
            return loop(molecule[1:], tokens + 1, parens + 1, commas)
        elif first == ',':
            return loop(molecule[1:], tokens + 1, parens, commas + 1)
        elif first in reps:
            return loop(molecule[1:], tokens + 1, parens, commas)
        elif first + second in reps:
            return loop(rest, tokens + 1, parens, commas)

    # This looks so gross in Python
    molecule = molecule.replace(
        'Rn', '(').replace(
        'Ar', ')').replace(
        'Y', ',')
    molecule = molecule[::-1]

    tokens, parens, commas = loop(molecule)
    return tokens - parens - 2 * commas


def main():
    replacement_pairs, molecule = parse_input(input_file.read_text())
    generated_molecules = generate_replacements(
        molecule=molecule,
        replacements=replacement_pairs)
    num_generated = len(generated_molecules)
    print(f'Part one, number of molecules generated: {num_generated}')

    min_steps_to_molecule = steps_to_molecule(molecule, replacement_pairs)
    print(f'Part two, minimum steps to molecule: {min_steps_to_molecule}'
          ' (iter)')

    min_steps_by_count = count(molecule, replacement_pairs)
    print(f'Part two, minimum steps to molecule: {min_steps_by_count}'
          ' (count)')


if __name__ == '__main__':
    main()
