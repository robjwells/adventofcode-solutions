#!/usr/bin/env python3

import aoc

import pytest


def circ_pairs(sequence, distance=1):
    """Zip elements some distance apart in sequence and wrap around

    For example:

    [4, 5, 1] -> [(4, 5), (5, 1), (1, 4)]
    """
    return zip(sequence, sequence[distance:] + sequence[:distance])


def int_to_sequence(integer):
    """Return a list of each digit in integer

    For example:

    1111 -> [1, 1, 1, 1]
    451  -> [4, 5, 1]
    """
    return [int(n) for n in str(integer)]


def matching_pairs(sequence):
    """Filter sequence so only pairs that are equal are returned

    For example:

    [(1, 2), (2, 3), (3, 1), (1, 1)] -> [(1, 1)]
    [(4, 5), (5, 1), (1, 4)]         -> []
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


def total_nearby_digits_in_sequence(circular_number, digit_distance):
    """Sums all digits that match a digit a specified distance away

    The sequence of digits (the circular_number) is considered to
    be circular, so the comparison wraps around the rear to the
    front of the sequence.
    """
    seq = int_to_sequence(circular_number)
    pairs = circ_pairs(seq, distance=digit_distance)
    matching = matching_pairs(pairs)
    return sum_matching_digits(matching)


def total_matching_neighbours(circular_number):
    """Sums all digits that match the next digit in the sequence"""
    return total_nearby_digits_in_sequence(circular_number, digit_distance=1)


def total_half_distant(circular_number):
    """Sums all digits that match the digit halfway distant in the sequence"""
    return total_nearby_digits_in_sequence(
        circular_number, digit_distance=len(str(circular_number)) // 2
    )


@pytest.mark.parametrize(
    "number,digit_distance,pairs",
    [
        (451, 1, [(4, 5), (5, 1), (1, 4)]),
        (1122, 1, [(1, 1), (1, 2), (2, 2), (2, 1)]),
        (1122, 2, [(1, 2), (1, 2), (2, 1), (2, 1)]),
        (1212, 1, [(1, 2), (2, 1), (1, 2), (2, 1)]),
        (1212, 2, [(1, 1), (2, 2), (1, 1), (2, 2)]),
        (123123, 1, [(1, 2), (2, 3), (3, 1), (1, 2), (2, 3), (3, 1)]),
        (123123, 3, [(1, 1), (2, 2), (3, 3), (1, 1), (2, 2), (3, 3)]),
    ],
)
def test_circ_pairs(number, digit_distance, pairs):
    """circ_pairs pairs digits in number with digit specified distance away"""
    sequence = int_to_sequence(number)
    assert list(circ_pairs(sequence, distance=digit_distance)) == pairs


@pytest.mark.parametrize(
    "circ_number,total",
    [
        (1122, 3),
        (1111, 4),
        (1234, 0),
        (91212129, 9),
    ],
)
def test_next(circ_number, total):
    """Test total_matching_neighbours against known input and output"""
    assert total_matching_neighbours(circ_number) == total


@pytest.mark.parametrize(
    "circ_number,total",
    [
        (1212, 6),
        (1221, 0),
        (123425, 4),
        (123123, 12),
        (12131415, 4),
    ],
)
def test_half_distant(circ_number, total):
    """Test total_half_distant against known input and output"""
    assert total_half_distant(circ_number) == total


def main(puzzle_input):
    print("Part one:", total_matching_neighbours(puzzle_input))
    print("Part two:", total_half_distant(puzzle_input))


if __name__ == "__main__":
    puzzle_input = int(aoc.load_puzzle_input(2017, 1))
    main(puzzle_input)
