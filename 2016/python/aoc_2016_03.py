from __future__ import annotations

from more_itertools import chunked
from typing import List, Tuple

from aoc_common import load_puzzle_input, report_solution


def parse_horizontal(string: str) -> List[Tuple[int, int, int]]:
    """Parse the instruction lines into triples of side lengths."""
    sides = [[int(x) for x in line.split()] for line in string.splitlines()]
    return [(s[0], s[1], s[2]) for s in sides]


def filter_valid_triangles(
    triples: List[Tuple[int, int, int]]
) -> List[Tuple[int, int, int]]:
    triples = sort_sides(triples)
    return [triple for triple in triples if triple[0] + triple[1] > triple[2]]


def parse_vertical(string: str) -> List[Tuple[int, int, int]]:
    horizontal_triples = parse_horizontal(string)
    all_vertical = [s[col] for col in range(3) for s in horizontal_triples]
    return [(s[0], s[1], s[2]) for s in chunked(all_vertical, 3)]


def sort_sides(triples: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    return [(t[0], t[1], t[2]) for t in [sorted(sides) for sides in triples]]


if __name__ == "__main__":
    input_string = load_puzzle_input(day=3)
    valid_horizontal = filter_valid_triangles(parse_horizontal(input_string))
    valid_vertical = filter_valid_triangles(parse_vertical(input_string))
    report_solution(
        puzzle_title="Day 3: Squares With Three Sides",
        part_one_solution=len(valid_horizontal),
        part_two_solution=len(valid_vertical),
    )
