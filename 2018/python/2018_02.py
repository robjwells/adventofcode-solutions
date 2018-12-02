"""Advent of Code 2018 Day 2: Inventory Management System"""

from collections import Counter

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
    """Return checksum of box ids provided in puzzle input"""
    return checksum(puzzle_input.split('\n'))


def checksum(box_ids):
    """Return integer checksum of box_ids list

    Checksum is defined as the number of ids containing
    exactly two of any letter, multiplied by the number
    of ids that contain exactly three of any letter.
    """
    two_count = boxes_with_n_of_any_letter(box_ids, 2)
    three_count = boxes_with_n_of_any_letter(box_ids, 3)
    return two_count * three_count


def boxes_with_n_of_any_letter(boxes, count):
    """Returns the number of boxes where a letter appears `count` times"""
    return sum(some_element_appers_n_times(box, count) for box in boxes)


def some_element_appers_n_times(iterable, count):
    """Returns whether any element of string appears exactly `count` times"""
    return count in Counter(iterable).values()


if __name__ == '__main__':
    puzzle_input = aoc_common.load_puzzle_input(DAY)

    part_one_solution = solve_part_one(puzzle_input)
    print('Part one:', part_one_solution)
