"""aoc_common

Common utility functions for Advent of Code solutions
"""

import pathlib
from typing import List, Optional


def load_puzzle_input(day: int) -> str:
    """Return the puzzle input for the day’s puzzle"""
    input_directory = pathlib.Path(__file__).parent.with_name("input")
    year = input_directory.parent.name
    input_filename = f"{year}-{day:02}.txt"
    return input_directory.joinpath(input_filename).read_text()


def report_solution(
    *,
    puzzle_title: str,
    part_one_solution: int,
    part_two_solution: Optional[int] = None,
) -> None:
    print(puzzle_title)
    print("=" * len(puzzle_title))
    print(f"Part one solution:    {part_one_solution}")
    if part_two_solution is not None:
        print(f"Part two solution:    {part_two_solution}")


def split_number_by_places(number: int) -> List[int]:
    places = []
    while number:
        places.append(number % 10)
        number //= 10
    return list(reversed(places))
