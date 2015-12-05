#!/usr/local/bin/python3

from collections import namedtuple

with open('day3_input.txt') as f:
    instructions = f.read().rstrip()

Point = namedtuple('Point', ['x', 'y'])
location = Point(0, 0)
visited = {location}


def new_loc(current_loc, instruction):
    if instruction == '^':
        xy = current_loc.x, current_loc.y + 1
    elif instruction == 'v':
        xy = current_loc.x, current_loc.y - 1
    elif instruction == '>':
        xy = current_loc.x + 1, current_loc.y
    elif instruction == '<':
        xy = current_loc.x - 1, current_loc.y
    return Point(*xy)


for char in instructions:
    location = new_loc(location, char)
    visited.add(location)

print('At least one present:', len(visited))


# Part two

santa_loc = Point(0, 0)
robo_loc = Point(0, 0)
visited = {santa_loc, robo_loc}

for idx, char in enumerate(instructions):
    if idx % 2 == 0:  # Santa
        santa_loc = new_loc(santa_loc, char)
        visited.add(santa_loc)
    else:  # robot
        robo_loc = new_loc(robo_loc, char)
        visited.add(robo_loc)

print('At least one present with santa and robot:', len(visited))
