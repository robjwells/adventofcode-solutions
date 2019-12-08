"""Day 6: Universal Orbit Map"""
from collections import defaultdict, deque
from typing import Dict, Iterator, List, NamedTuple

import aoc_common

DAY = 6

OrbitGraph = Dict[str, List[str]]


class Orbit(NamedTuple):
    orbited: str
    orbited_by: str


def parse_input(input_text: str) -> List[Orbit]:
    return [Orbit(*line.split(")")) for line in input_text.splitlines()]


def create_orbit_graph(orbits: List[Orbit]) -> OrbitGraph:
    orbit_graph: Dict[str, List[str]] = defaultdict(list)
    for orbited, orbited_by in orbits:
        orbit_graph[orbited].append(orbited_by)
    return orbit_graph


def orbit_depths(orbit_graph: OrbitGraph) -> Iterator[int]:
    queue = deque([(0, "COM")])
    while queue:
        depth, body = queue.popleft()
        yield depth
        queue.extend(
            [(depth + 1, orbiting_body) for orbiting_body in orbit_graph[body]]
        )


def main(orbit_list: List[Orbit]) -> None:
    orbit_graph = create_orbit_graph(orbit_list)
    part_one_solution = sum(orbit_depths(orbit_graph))
    print(part_one_solution)


def test_orbit_depths():
    orbits = """\
COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L"""
    orbit_graph = create_orbit_graph(parse_input(orbits))
    assert sum(orbit_depths(orbit_graph)) == 42


if __name__ == "__main__":
    parsed = parse_input(aoc_common.load_puzzle_input(DAY))
    main(parsed)
