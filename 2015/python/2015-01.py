#!/usr/bin/env python3
"""Advent of Code 2015, Day 1: Not Quite Lisp"""

import pytest


def final_floor(instructions):
    """Calculate the final floor for a given set of instructions

    Instructions are a list of parentheses:
        (   Move up a floor
        )   Move down a floor
    """
    instruction_values = {'(': 1, ')': -1}
    result = sum(instruction_values[char] for char in instructions)
    return result


def first_basement_char(instructions):
    """Return position of char that puts Santa in the basement

    Positions start from 1.
    """
    instruction_values = {'(': 1, ')': -1}
    floor = 0
    for position, char in enumerate(instructions, start=1):
        floor += instruction_values[char]
        if floor == -1:
            return position


def main(puzzle_input):
    p1_final_floor = final_floor(puzzle_input)
    print(f'Part one, final floor: {p1_final_floor}')
    basement_instruction = first_basement_char(puzzle_input)
    print(f'Part two, first basement instruction: {basement_instruction}')


@pytest.mark.parametrize('instructions,expected', [
    ('(())', 0),
    ('()()', 0),
    ('(((', 3),
    ('(()(()(', 3),
    ('))(((((', 3),
    ('())', -1),
    ('))(', -1),
    (')))', -3),
    (')())())', -3),
    ])
def test_final_floor(instructions, expected):
    """final_floor calculates correct final floor from instructions"""
    assert final_floor(instructions) == expected


@pytest.mark.parametrize('instructions,expected', [
    (')', 1),
    ('()())', 5),
    ])
def test_first_basement_level(instructions, expected):
    """first_basement_char returns position of first sub-zero instruction"""
    assert first_basement_char(instructions) == expected


if __name__ == '__main__':
    with open('../input/2015-01.txt') as input_file:
        puzzle_input = input_file.read().rstrip()
    main(puzzle_input)
