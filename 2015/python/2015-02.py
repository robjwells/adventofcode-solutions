#!/usr/bin/env python3
"""Advent of Code 2015, Day 2: I Was Told There Would Be No Math"""

import pytest


def parse_input(text):
    """Parse a file containing box dimensions LxWxH

    Returns a list of lists of ints [[L, W, H]].
    """
    return [[int(i) for i in line.split('x')]
            for line in text.splitlines()]


def surface_area(l, w, h):
    """Return the total surface area of a box"""
    return (2 * l * w) + (2 * w * h) + (2 * h * l)


def smallest_side(l, w, h):
    """Return the area of the smallest side of a box"""
    return min([(l * w), (w * h), (h * l)])


def wrapping_paper(dimensions):
    """Return total amount of wrapping paper needed for box of size dimensions

    The total wrapping paper includes enough wrapping paper for each side of
    the box, plus slack equal to the size of the smallest side.
    """
    return surface_area(*dimensions) + smallest_side(*dimensions)


def ribbon(dimensions):
    """Return total ribbon needed for box of size dimensions

    The total ribbon is equal to twice the lengths of the shortest two
    dimensions plus the product of all three dimensions.
    """
    s1, s2, s3 = sorted(dimensions)
    return (2 * s1) + (2 * s2) + (s1 * s2 * s3)


def test_parse():
    dimensions = '''\
2x3x4
1x1x10
'''
    assert parse_input(dimensions) == [[2, 3, 4], [1, 1, 10]]


# Dimensions, wrapping total, ribbon total
TEST_BOXES = [([2, 3, 4], 58, 34),
              ([1, 1, 10], 43, 14)]


@pytest.mark.parametrize('dimensions,wrapping_tot,_', TEST_BOXES)
def test_wrapping_paper(dimensions, wrapping_tot, _):
    assert wrapping_paper(dimensions) == wrapping_tot


@pytest.mark.parametrize('dimensions,_,ribbon_tot', TEST_BOXES)
def test_ribbon(dimensions, _, ribbon_tot):
    assert ribbon(dimensions) == ribbon_tot


def main(puzzle_input):
    # Part one
    needed_paper = sum(wrapping_paper(box) for box in puzzle_input)
    print(f'Part one, wrapping paper: {needed_paper:,}')

    # Part two
    needed_ribbon = sum(ribbon(box) for box in puzzle_input)
    print(f'Part two, ribbon: {needed_ribbon:,}')


if __name__ == '__main__':
    with open('../input/2015-02.txt') as input_file:
        puzzle_input = parse_input(input_file.read())
    main(puzzle_input)
