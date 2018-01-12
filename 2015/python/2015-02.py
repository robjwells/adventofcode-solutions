#!/usr/bin/env python3
"""Advent of Code 2015, Day 2: I Was Told There Would Be No Math"""

import pathlib


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


# Dimensions, wrapping total, ribbon total
TEST_BOXES = [([2, 3, 4], 58, 34),
              ([1, 1, 10], 43, 14)]


def test_wrapping_paper():
    for dimensions, expected, _ in TEST_BOXES:
        assert wrapping_paper(dimensions) == expected


def test_ribbon():
    for dimensions, _, expected in TEST_BOXES:
        assert ribbon(dimensions) == expected


def main(puzzle_input):
    # Part one
    needed_paper = sum(wrapping_paper(box) for box in puzzle_input)
    print(f'Part one, wrapping paper: {needed_paper:,}')

    # Part two
    needed_ribbon = sum(ribbon(box) for box in puzzle_input)
    print(f'Part two, ribbon: {needed_ribbon:,}')


if __name__ == '__main__':
    puzzle_input = parse_input(
        pathlib.Path('../input/2015-02.txt').read_text())
    main(puzzle_input)
