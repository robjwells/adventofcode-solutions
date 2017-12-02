#!/usr/bin/env python3


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


def main(puzzle_input):
    seq = int_to_sequence(puzzle_input)
    pairs = circ_pairs(seq)
    matching = matching_pairs(pairs)
    return sum_matching_digits(matching)


def test_full():
    assert main(1122) == 3
    assert main(1111) == 4
    assert main(1234) == 0
    assert main(91212129) == 9


if __name__ == '__main__':
    puzzle_input = 91212129  # This is example input
    print(main(puzzle_input))
