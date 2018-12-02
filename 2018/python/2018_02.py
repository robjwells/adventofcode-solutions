"""Advent of Code 2018 Day 2: Inventory Management System"""

import aoc_common
import pytest

DAY = 2


def test_solve_part_one():
    """solve_part_one produces correct results on known input"""
    puzzle_input = '\n'.join([
        'abcdef', 'bababc', 'abbcde', 'abcccd',
        'aabcdd', 'abcdee', 'ababab',
    ])
    expected = 12
    assert solve_part_one(puzzle_input) == expected


def solve_part_one(puzzle_input):
    pass


if __name__ == '__main__':
    puzzle_input = aoc_common.load_puzzle_input(DAY)
