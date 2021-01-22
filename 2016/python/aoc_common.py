"""aoc_common

Common utility functions for Advent of Code solutions
"""
from __future__ import annotations

import pathlib
from itertools import islice, repeat
from typing import Iterable, TypeVar


def load_puzzle_input(day: int) -> str:
    """Return the puzzle input for the day’s puzzle"""
    input_directory = pathlib.Path(__file__).parent.with_name("input")
    year = input_directory.parent.name
    input_filename = f"{year}-{day:02}.txt"
    return input_directory.joinpath(input_filename).read_text()


def report_solution(
    *,
    puzzle_title: str,
    part_one_solution: int | str,
    part_two_solution: int | str | None = None,
) -> None:
    print(puzzle_title)
    print("=" * len(puzzle_title))
    print(f"Part one solution:    {part_one_solution}")
    if part_two_solution is not None:
        print(f"Part two solution:    {part_two_solution}")


def split_number_by_places(number: int) -> list[int]:
    places = []
    while number:
        places.append(number % 10)
        number //= 10
    return list(reversed(places))


class Sentinel:
    pass


T = TypeVar("T")


def chunked(
    iterable: Iterable[T], count: int, *, fill: T | Sentinel = Sentinel()
) -> Iterable[list[T]]:
    """Yield count-long chunks from iterable.

    If the length of the iterable is not a multiple of count,
    the final chunk will be short, unless `fill` is provided
    as a keyword argument, in which case the final chunk will
    be filled with the given value.
    """
    iterator = iter(iterable)
    while True:
        chunk = list(islice(iterator, count))
        if not chunk:
            return
        if len(chunk) < count and not isinstance(fill, Sentinel):
            chunk += repeat(fill, count - len(chunk))
        yield chunk
