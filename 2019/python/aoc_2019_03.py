"""Day 3: Crossed Wires"""
import aoc_common
import pytest
from typing import Dict, List, Set, Tuple
from typing import NamedTuple

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


class Instruction(NamedTuple):
    direction: str
    distance: int


class Point(NamedTuple):
    x: int
    y: int

    @staticmethod
    def origin():
        return Point(0, 0)


def parse_input(puzzle_input: str) -> List[List[Instruction]]:
    """Split each line in the input into a list of (direction, distance) tuples."""
    return [
        [Instruction(part[0], int(part[1:])) for part in line.split(",")]
        for line in puzzle_input.splitlines()
    ]


def manhattan_distance(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def trace_single_wire_locations(instructions: List[Instruction]) -> Dict[Point, int]:
    """Returns a set of the unique locations traced by the wire instructions."""
    current = Point.origin()
    move_functions = {
        "U": lambda p: Point(current.x, current.y + 1),
        "D": lambda p: Point(current.x, current.y - 1),
        "R": lambda p: Point(current.x + 1, current.y),
        "L": lambda p: Point(current.x - 1, current.y),
    }
    visited: Dict[Point, int] = {}
    step = 0
    for instruction in instructions:
        mover = move_functions[instruction.direction]
        for _ in range(instruction.distance):
            current = mover(current)
            step += 1
            if current not in visited:
                visited[current] = step

    return visited


def find_closest_intersection(intersections: Set[Point]) -> Point:
    return min(
        intersections, key=lambda point: manhattan_distance(point, Point.origin())
    )


def find_closest_intersection_distance(wire_traces: List[Dict[Point, int]]) -> int:
    intersecting = wire_traces[0].keys() & wire_traces[1].keys()
    return manhattan_distance(find_closest_intersection(intersecting), Point.origin())


def trace_wires(instructions: List[List[Instruction]]) -> List[Dict[Point, int]]:
    return [trace_single_wire_locations(wire) for wire in instructions]


def solve_part_one(instructions: List[List[Instruction]]) -> int:
    return find_closest_intersection_distance(trace_wires(instructions))


if __name__ == "__main__":
    puzzle_input = aoc_common.load_puzzle_input(DAY)
    parsed = parse_input(puzzle_input)
    part_one_solution = solve_part_one(parsed)
    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
