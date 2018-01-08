#!/usr/local/bin/python3

from collections import namedtuple
import pathlib


def main(puzzle_input):
    Point = namedtuple('Point', ['x', 'y'])
    location = Point(0, 0)
    visited = {location}

    def new_loc(current_loc, instruction):
        new_loc_table = {
            '^': (current_loc.x, current_loc.y + 1),
            'v': (current_loc.x, current_loc.y - 1),
            '>': (current_loc.x + 1, current_loc.y),
            '<': (current_loc.x - 1, current_loc.y)
            }
        return Point(*new_loc_table[instruction])

    for char in puzzle_input:
        location = new_loc(location, char)
        visited.add(location)

    print('At least one present:', len(visited))

    # Part two
    santa_loc = Point(0, 0)
    robo_loc = Point(0, 0)
    visited = {santa_loc}

    for idx, char in enumerate(puzzle_input):
        if idx % 2 == 0:  # Santa
            santa_loc = new_loc(santa_loc, char)
            visited.add(santa_loc)
        else:  # robot
            robo_loc = new_loc(robo_loc, char)
            visited.add(robo_loc)

    print('At least one present with santa and robot:', len(visited))


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
    visited = {(0, 0)}
    for santa in range(number_of_santas):
        location = (0, 0)
        for direction in instructions[santa::number_of_santas]:
            location = move_location(location, direction)
            visited.add(location)
    return len(visited)


def test_move_location():
    """move_location correctly moves in any of the cardinal directions"""
    origin = (0, 0)
    test_cases = [
        ('^', (0, 1)),
        ('v', (0, -1)),
        ('>', (1, 0)),
        ('<', (-1, 0))]
    for instruction, expected_location in test_cases:
        new_location = move_location(current_location=origin,
                                     direction=instruction)
        assert new_location == expected_location


def test_houses_visited():
    """houses_visited gives expected number of houses with one santa agent"""
    test_cases = [
        ('>', 2),
        ('^>v<', 4),
        ('^v^v^v^v^v', 2)]
    for instructions, total_houses in test_cases:
        assert houses_visited(instructions) == total_houses


def test_houses_visited_by_two_santas():
    """houses_visited gives expected number of houses with two santa agents"""
    test_cases = [
        ('^v', 3),
        ('^>v<', 3),
        ('^v^v^v^v^v', 11)]
    for instructions, total_houses in test_cases:
        assert houses_visited(instructions, number_of_santas=2) == total_houses


if __name__ == '__main__':
    puzzle_input = pathlib.Path('../input/2015-03.txt').read_text().rstrip()
    main(puzzle_input)
