"""aoc_common

Common utility functions for Advent of Code solutions
"""

import pathlib


def load_puzzle_input(day):
    """Return the puzzle input for the day’s puzzle"""
    input_directory = pathlib.Path(__file__).parent.with_name('input')
    year = input_directory.parent.name
    input_filename = f'{year}-{day:02}.txt'
    return input_directory.joinpath(input_filename).read_text()
