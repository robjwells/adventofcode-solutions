"""Advent of Code 2018 Day 1: Chronal Calibration"""

import pytest


PART_ONE_CASES = [
    ('+1\n+1\n+1', 3),
    ('+1\n+1\n-2', 0),
    ('-1\n-2\n-3', -6),
]


@pytest.mark.parametrize('puzzle_input,expected', PART_ONE_CASES)
def test_solve(puzzle_input, expected):
    assert solve(puzzle_input) == expected


@pytest.mark.parametrize('puzzle_input,parsed', zip(
    (case_input for case_input, expected in PART_ONE_CASES),
    ([1, 1, 1], [1, 1, -2], [-1, -2, -3])
))
def test_parse(puzzle_input, parsed):
    assert parse(puzzle_input) == parsed


def parse(puzzle_input):
    """Parses puzzle input into a list of ints"""
    return [int(n) for n in puzzle_input.splitlines()]


def solve(puzzle_input):
    """Return the sum of the frequency changes listed in input"""
    frequency_changes = parse(puzzle_input)
    return sum(frequency_changes)
