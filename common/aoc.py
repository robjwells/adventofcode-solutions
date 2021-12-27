"""aoc

Common utility functions for Advent of Code solutions.
"""

from os import environ
from pathlib import Path


AOC_ROOT_KEY = "AOC_ROOT"


def _get_aoc_root_directory() -> Path:
    try:
        root = Path(environ[AOC_ROOT_KEY])
    except KeyError as e:
        raise EnvironmentError(
            "Cannot find your Advent of Code root directory as the "
            f"{AOC_ROOT_KEY} environment variable is unset."
        ) from e
    if not root.exists() and root.is_dir():
        raise FileNotFoundError(f"Given root '{root}' is not an existing directory.")
    return root.resolve(strict=True)


def _construct_input_file_path(year: int, day: int) -> Path:
    assert 2015 <= year <= 2021, f"Year '{year}' is out of range."
    assert 1 <= day <= 25, f"Day '{day}' is out of range."
    root = _get_aoc_root_directory()
    return root / str(year) / "input" / f"{year}-{day:02}.txt"


def load_puzzle_input(year: int, day: int) -> str:
    """Return the puzzle input for the day’s puzzle"""
    return _construct_input_file_path(year, day).read_text()


def format_solution(
    *,
    title: str,
    part_one: int | str,
    part_two: int | str | None = None,
) -> str:
    separator_line = "=" * len(title)
    parts = [
        separator_line,
        title,
        separator_line,
        f"Part one:    {part_one}",
    ]
    if part_two is not None:
        parts.append(f"Part two:    {part_two}")
    return "\n".join(parts)


def split_number_by_places(number: int) -> list[int]:
    places = []
    while number:
        places.append(number % 10)
        number //= 10
    return list(reversed(places))
