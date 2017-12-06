#!/usr/bin/env python3

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


def steps_to_molecule(molecule: str, replacements: list):
    """Return the minimum number of replacements needed to make molecule"""
    pass


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


def test_steps_to_molecule():
    test_molecule = 'HOH'
    test_replacements = [
        ('e', 'H'),
        ('e', 'O'),
        ('H', 'HO'),
        ('H', 'OH'),
        ('O', 'HH'),
        ]
    expected_steps = 6
    result = steps_to_molecule(molecule=test_molecule,
                               replacements=test_replacements)
    assert result == expected_steps


def main():
    replacement_pairs, molecule = parse_input(input_file.read_text())
    generated_molecules = generate_replacements(
        molecule=molecule,
        replacements=replacement_pairs)
    print(len(generated_molecules))


if __name__ == '__main__':
    main()
