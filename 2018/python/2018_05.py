"""Advent of Code 2018 Day 5: Alchemical Reduction"""

import collections

import aoc

DAY = 5


def swap_case(char):
    if char != char.lower():
        return char.lower()
    else:
        return char.upper()


def solve_part_one(puzzle_input):
    stack = collections.deque()
    for char in puzzle_input:
        if not stack or stack[-1] != swap_case(char):
            stack.append(char)
        else:
            stack.pop()
    return len(stack)


if __name__ == "__main__":
    puzzle_input = aoc.load_puzzle_input(2018, DAY)

    print(__doc__)

    part_one_solution = solve_part_one(puzzle_input)
    print("Part one:", part_one_solution)

    # part_two_solution = solve_part_two(puzzle_input)
    # print('Part two:', part_two_solution)
