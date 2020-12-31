from __future__ import annotations

from typing import List, Tuple

from aoc_common import load_puzzle_input, report_solution


def parse_horizontal(string: str) -> List[Tuple[int, int, int]]:
    """Parse the instruction lines into sorted triples of side lengths."""
    sorted_sides = [
        sorted(int(x) for x in line.split()) for line in string.splitlines()
    ]
    triples = [(sides[0], sides[1], sides[2]) for sides in sorted_sides]
    return triples


def filter_valid_triangles(
    triples: List[Tuple[int, int, int]]
) -> List[Tuple[int, int, int]]:
    return [triple for triple in triples if triple[0] + triple[1] > triple[2]]


if __name__ == "__main__":
    horizontal_triples = parse_horizontal(load_puzzle_input(day=3))
    valid_horizontal = filter_valid_triangles(horizontal_triples)
    report_solution(
        puzzle_title="Day 3: Squares With Three Sides",
        part_one_solution=len(valid_horizontal),
    )
