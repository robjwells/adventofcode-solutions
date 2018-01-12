#!/usr/bin/env python3
"""Advent of Code 2015, Day 1: Not Quite Lisp"""


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


def test_final_floor():
    """final_floor calculates correct final floor from instructions"""
    test_cases = [
        ['(())', 0],
        ['()()', 0],
        ['(((', 3],
        ['(()(()(', 3],
        ['))(((((', 3],
        ['())', -1],
        ['))(', -1],
        [')))', -3],
        [')())())', -3],
        ]
    for instructions, expected in test_cases:
        assert final_floor(instructions) == expected


def test_first_basement_level():
    """first_basement_char returns position of first sub-zero instruction"""
    test_cases = [
        [')', 1],
        ['()())', 5]
        ]
    for instructions, expected in test_cases:
        assert first_basement_char(instructions) == expected


if __name__ == '__main__':
    with open('../input/2015-01.txt') as input_file:
        puzzle_input = input_file.read().rstrip()
    main(puzzle_input)
