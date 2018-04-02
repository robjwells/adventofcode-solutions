#!/usr/bin/env python3
"""Advent of Code 2015, Day 3: Perfectly Spherical Houses in a Vacuum"""

import pytest


def move_location(current_location, direction):
    """Return a new (x, y) tuple after moving one unit in direction

    current_location should be tuple of ints (x, y)

    Direction is one of:
        ^   north
        v   south
        >   east
        <   west
    """
    direction_table = {
        '^': (0, 1),
        'v': (0, -1),
        '>': (1, 0),
        '<': (-1, 0)}
    cur_x, cur_y = current_location
    diff_x, diff_y = direction_table[direction]
    return (cur_x + diff_x, cur_y + diff_y)


def houses_visited(instructions, number_of_santas=1):
    """Return the number of distinct houses visited by following instructions

    instructions is a string containing the characters `^ v > <` which move
    the current location one unit north, south, east and west respectively.

    number_of_santas determines how many people the decisions will be shared
    among. The default (1) means that one starting location is changed at each
    step, where 2 would have one location changed for each odd-indexed
    instruction and the other for each even-numbered instruction.

    The simulation may visit the same location twice but only unique locations
    are counted for the return value.
    """
    # Initialise visited set with origin location
    origin = (0, 0)
    visited = {origin}
    for santa in range(number_of_santas):
        location = origin
        # Use the santa number and the total number of santas to divide
        # up the instructions between each of them
        for direction in instructions[santa::number_of_santas]:
            location = move_location(location, direction)
            visited.add(location)
    return len(visited)


@pytest.mark.parametrize('instruction,expected_location', [
    ('^', (0, 1)),
    ('v', (0, -1)),
    ('>', (1, 0)),
    ('<', (-1, 0)),
    ])
def test_move_location(instruction, expected_location):
    """move_location correctly moves in any of the cardinal directions"""
    origin = (0, 0)
    new_location = move_location(current_location=origin,
                                 direction=instruction)
    assert new_location == expected_location


@pytest.mark.parametrize('instructions,total_houses', [
    ('>', 2),
    ('^>v<', 4),
    ('^v^v^v^v^v', 2),
    ])
def test_houses_visited(instructions, total_houses):
    """houses_visited gives expected number of houses with one santa agent"""
    assert houses_visited(instructions) == total_houses


@pytest.mark.parametrize('instructions,total_houses', [
    ('^v', 3),
    ('^>v<', 3),
    ('^v^v^v^v^v', 11),
    ])
def test_houses_visited_by_two_santas(instructions, total_houses):
    """houses_visited gives expected number of houses with two santa agents"""
    assert houses_visited(instructions, number_of_santas=2) == total_houses


def main(puzzle_input):
    # Part one, houses visited by Santa himself
    one_santa = houses_visited(puzzle_input)
    print(f'Part one, single santa: {one_santa}')

    # Part two
    two_santas = houses_visited(puzzle_input, number_of_santas=2)
    print(f'Part two, two santas: {two_santas}')


if __name__ == '__main__':
    with open('../input/2015-03.txt') as input_file:
        puzzle_input = input_file.read().rstrip()
    main(puzzle_input)
