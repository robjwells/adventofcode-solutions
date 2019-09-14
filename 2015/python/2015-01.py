#!/usr/bin/env python3
"""Advent of Code 2015, Day 1: Not Quite Lisp"""
from itertools import accumulate

import pytest


def parse_input(instructions):
    """Parse the parentheses into floor-change deltas (1, -1)."""
    instruction_values = {"(": 1, ")": -1}
    return [instruction_values[char] for char in instructions]


def final_floor(deltas):
    """Calculate the final floor for a given set of instructions."""
    return sum(deltas)


def first_basement_char(deltas):
    """Return position of char that puts Santa in the basement

    Positions start from 1.
    """
    return next(
        position
        for (position, floor) in enumerate(accumulate(deltas), start=1)
        if floor == -1
    )


def main(puzzle_input):
    parsed = parse_input(puzzle_input)
    p1_final_floor = final_floor(parsed)
    print(f"Part one, final floor: {p1_final_floor}")
    basement_instruction = first_basement_char(parsed)
    print(f"Part two, first basement instruction: {basement_instruction}")


@pytest.mark.parametrize(
    "instructions,expected",
    [
        ("(())", 0),
        ("()()", 0),
        ("(((", 3),
        ("(()(()(", 3),
        ("))(((((", 3),
        ("())", -1),
        ("))(", -1),
        (")))", -3),
        (")())())", -3),
    ],
)
def test_final_floor(instructions, expected):
    """final_floor calculates correct final floor from instructions"""
    assert final_floor(parse_input(instructions)) == expected


@pytest.mark.parametrize("instructions,expected", [(")", 1), ("()())", 5)])
def test_first_basement_level(instructions, expected):
    """first_basement_char returns position of first sub-zero instruction"""
    assert first_basement_char(parse_input(instructions)) == expected


if __name__ == "__main__":
    with open("../input/2015-01.txt") as input_file:
        puzzle_input = input_file.read().rstrip()
    main(puzzle_input)
