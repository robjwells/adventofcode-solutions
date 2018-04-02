#!/usr/bin/env python3

import pytest


def circ_pairs(sequence):
    """Zip consequtive elements in sequence and wrap round at the end

    For example:

    [4, 5, 1] -> [(4, 5), (5, 1), (1, 4)]
    """
    return zip(sequence, sequence[1:] + [sequence[0]])


def int_to_sequence(integer):
    """Return a list of each digit in integer

    For example:

    1111 -> [1, 1, 1, 1]
    451  -> [4, 5, 1]
    """
    return [int(n) for n in str(integer)]


def matching_pairs(sequence):
    """Filter sequence so only pairs that are equal are returned

    For example
    [(1, 2), (2, 3), (3, 1) (1, 1)] -> [(1, 1)]
    [(4, 5), (5, 1), (1, 4)] -> []
    """
    return filter(lambda t: t[0] == t[1], sequence)


def sum_matching_digits(pairs):
    """Sum the digits that match the second item of the pair

    Note that matching digits are single counted, not double.

    For example:
    [(1, 1)]         -> 1
    [(1, 1), (2, 2)] -> 3
    """
    return sum(a for a, b in pairs)


def sum_matching_neighbours(circular_number):
    """Sums all digits that match the next digit in the sequence"""
    seq = int_to_sequence(circular_number)
    pairs = circ_pairs(seq)
    matching = matching_pairs(pairs)
    return sum_matching_digits(matching)


def main(puzzle_input):
    print('Part one:', sum_matching_neighbours(puzzle_input))


@pytest.mark.parametrize('circ_number,total', [
    (1122, 3),
    (1111, 4),
    (1234, 0),
    (91212129, 9),
    ])
def test_next(circ_number, total):
    assert sum_matching_neighbours(circ_number) == total


if __name__ == '__main__':
    with open('../input/2017-01.txt') as f:
        puzzle_input = int(f.read())
    main(puzzle_input)
