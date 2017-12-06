#!/usr/bin/env python3

import re


def generate_replacements(molecule: str, replacements: list):
    """Return set of permutations for the given molecule

    replacements should be a list of (str, str) tuples, with
    the first item being the string to be replaced and
    the second the replacement string.
    """
    return set()


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


def main():
    pass


if __name__ == '__main__':
    main()
