"""Day 3: Crossed Wires"""
from __future__ import annotations
from functools import reduce
from typing import Dict, List, NamedTuple, Set

import pytest

import aoc_common

DAY = 3


@pytest.mark.parametrize(
    "puzzle_input,expected_distance",
    [
        (("R8,U5,L5,D3" "\n" "U7,R6,D4,L4"), 6),
        (
            (
                "R75,D30,R83,U83,L12,D49,R71,U7,L72"
                "\n"
                "U62,R66,U55,R34,D71,R55,D58,R83"
            ),
            159,
        ),
        (
            (
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
                "\n"
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
            ),
            135,
        ),
    ],
)
def test_find_closest_intersection_distance(
    puzzle_input: str, expected_distance: int
) -> None:
    parsed = parse_input(puzzle_input)
    wire_traces = trace_wires(parsed)
    assert find_closest_intersection_distance(wire_traces) == expected_distance


@pytest.mark.parametrize(
    "puzzle_input,expected_delay",
    [
        (("R8,U5,L5,D3" "\n" "U7,R6,D4,L4"), 30),
        (
            (
                "R75,D30,R83,U83,L12,D49,R71,U7,L72"
                "\n"
                "U62,R66,U55,R34,D71,R55,D58,R83"
            ),
            610,
        ),
        (
            (
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
                "\n"
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
            ),
            410,
        ),
    ],
)
def test_find_lowest_intersection_signal_delay(
    puzzle_input: str, expected_delay: int
) -> None:
    parsed = parse_input(puzzle_input)
    wire_traces = trace_wires(parsed)
    assert find_lowest_intersection_signal_delay(wire_traces) == expected_delay


class Instruction(NamedTuple):
    direction: str
    distance: int


class Point(NamedTuple):
    x: int
    y: int

    @staticmethod
    def origin() -> Point:
        return Point(0, 0)


TraceDict = Dict[Point, int]


def parse_input(puzzle_input: str) -> List[List[Instruction]]:
    """Split each line in the input into a list of (direction, distance) tuples."""
    return [
        [Instruction(part[0], int(part[1:])) for part in line.split(",")]
        for line in puzzle_input.splitlines()
    ]


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def trace_single_wire_locations(instructions: List[Instruction]) -> TraceDict:
    """Returns a set of the unique locations traced by the wire instructions."""
    current = Point.origin()
    move_functions = {
        "U": lambda p: Point(p.x, p.y + 1),
        "D": lambda p: Point(p.x, p.y - 1),
        "R": lambda p: Point(p.x + 1, p.y),
        "L": lambda p: Point(p.x - 1, p.y),
    }
    visited: TraceDict = {}
    step = 0
    for instruction in instructions:
        mover = move_functions[instruction.direction]
        for _ in range(instruction.distance):
            current = mover(current)
            step += 1
            if current not in visited:
                visited[current] = step

    return visited


def intersect_dict_keys(dictionaries: List[TraceDict]) -> Set[Point]:
    if not dictionaries:
        return set()
    return reduce(lambda keys, d: keys & d.keys(), dictionaries)  # type: ignore


def find_closest_intersection(intersections: Set[Point]) -> Point:
    return min(
        intersections, key=lambda point: manhattan_distance(point, Point.origin())
    )


def find_closest_intersection_distance(wire_traces: List[TraceDict]) -> int:
    intersecting = intersect_dict_keys(wire_traces)
    return manhattan_distance(find_closest_intersection(intersecting), Point.origin())


def find_lowest_intersection_signal_delay(wire_traces: List[TraceDict]) -> int:
    intersecting_points = intersect_dict_keys(wire_traces)
    return min(
        sum(trace[point] for trace in wire_traces) for point in intersecting_points
    )


def trace_wires(instructions: List[List[Instruction]]) -> List[TraceDict]:
    return [trace_single_wire_locations(wire) for wire in instructions]


if __name__ == "__main__":
    puzzle_input = aoc_common.load_puzzle_input(DAY)
    instructions = parse_input(puzzle_input)
    wire_traces = trace_wires(instructions)
    part_one_solution = find_closest_intersection_distance(wire_traces)
    part_two_solution = find_lowest_intersection_signal_delay(wire_traces)
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution=part_two_solution,
    )
