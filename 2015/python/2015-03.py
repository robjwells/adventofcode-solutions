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


if __name__ == '__main__':
    puzzle_input = pathlib.Path('../input/2015-03.txt').read_text().rstrip()
    main(puzzle_input)
