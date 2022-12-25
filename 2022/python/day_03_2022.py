from __future__ import annotations

from util import read_input

import pytest
from more_itertools import chunked


def calculate_priority(item: str) -> int:
    assert len(item) == 1, "Only handles single characters."
    assert item.isalpha(), "Item must be a letter."
    if item.isupper():
        return ord(item) - 38
    if item.islower():
        return ord(item) - 96
    raise ValueError(f"Should be unreachable but got: {item!r}")


def common_in_compartments(line: str) -> str:
    half = len(line) // 2
    common = set(line[:half]) & set(line[half:])
    return common.pop()


def solve_part_one(puzzle_input: str) -> int:
    common = [common_in_compartments(line) for line in puzzle_input.splitlines()]
    priorities = [calculate_priority(item) for item in common]
    return sum(priorities)


def solve_part_two(puzzle_input: str) -> int:
    lines = puzzle_input.splitlines()
    groups = [set(a) & set(b) & set(c) for a, b, c in chunked(lines, 3, strict=True)]
    priorities = [calculate_priority(s.pop()) for s in groups]
    return sum(priorities)


def main() -> None:
    puzzle_input = read_input(3)

    part_one = solve_part_one(puzzle_input)
    print(f"Part one: {part_one:,}")

    part_two = solve_part_two(puzzle_input)
    print(f"Part two: {part_two:,}")


if __name__ == "__main__":
    main()


SAMPLE_INPUT = """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


@pytest.mark.parametrize(
    ["item", "priority"],
    [
        ("p", 16),
        ("L", 38),
        ("P", 42),
        ("v", 22),
        ("t", 20),
        ("s", 19),
    ],
)
def test_priority(item: str, priority: int) -> None:
    assert calculate_priority(item) == priority


def test_sample_input_part_one() -> None:
    assert solve_part_one(SAMPLE_INPUT) == 157


def test_sample_input_part_two() -> None:
    assert solve_part_two(SAMPLE_INPUT) == 70
