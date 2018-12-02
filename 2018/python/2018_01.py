"""Advent of Code 2018 Day 1: Chronal Calibration"""

import itertools

import aoc_common
import pytest

DAY = 1

PART_ONE_CASES = [
    ('+1\n+1\n+1', 3),
    ('+1\n+1\n-2', 0),
    ('-1\n-2\n-3', -6),
]


@pytest.mark.parametrize('puzzle_input,expected', PART_ONE_CASES)
def test_solve_part_one(puzzle_input, expected):
    assert solve_part_one(puzzle_input) == expected


@pytest.mark.parametrize('puzzle_input,expected', [
    ('+1\n-1', 0),
    ('+3\n+3\n+4\n-2\n-4', 10),
    ('-6\n+3\n+8\n+5\n-6', 5),
    ('+7\n+7\n-2\n-7\n-4', 14),
])
def test_solve_part_two(puzzle_input, expected):
    assert solve_part_two(puzzle_input) == expected


@pytest.mark.parametrize('puzzle_input,parsed', zip(
    (case_input for case_input, expected in PART_ONE_CASES),
    ([1, 1, 1], [1, 1, -2], [-1, -2, -3])
))
def test_parse(puzzle_input, parsed):
    assert parse(puzzle_input) == parsed


def test_known_part_one_solution():
    part_one_solution = 400
    puzzle_input = aoc_common.load_puzzle_input(DAY)
    assert solve_part_one(puzzle_input) == part_one_solution


def test_known_part_two_solution():
    part_two_solution = 232
    puzzle_input = aoc_common.load_puzzle_input(DAY)
    assert solve_part_two(puzzle_input) == part_two_solution


def parse(puzzle_input):
    """Parses puzzle input into a list of ints"""
    return [int(n) for n in puzzle_input.splitlines()]


def solve_part_one(puzzle_input):
    """Return the sum of the frequency changes listed in input"""
    frequency_changes = parse(puzzle_input)
    return sum(frequency_changes)


def solve_part_two(puzzle_input):
    """Return the first repeated frequency"""
    frequency_changes = parse(puzzle_input)
    frequency = 0
    seen = {frequency}
    for change in itertools.cycle(frequency_changes):
        frequency += change
        if frequency in seen:
            return frequency
        seen.add(frequency)


if __name__ == '__main__':
    puzzle_input = aoc_common.load_puzzle_input(DAY)

    part_one_solution = solve_part_one(puzzle_input)
    print('Part one:', part_one_solution)

    part_two_solution = solve_part_two(puzzle_input)
    print('Part two:', part_two_solution)
