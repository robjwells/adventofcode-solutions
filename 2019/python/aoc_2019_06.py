"""Day 6: Universal Orbit Map"""
import math
from collections import defaultdict, deque
from copy import deepcopy
from typing import DefaultDict, Iterator, List, NamedTuple, Tuple

import aoc

DAY = 6

OrbitGraph = DefaultDict[str, List[str]]


def parse_input(input_text: str) -> OrbitGraph:
    orbits: OrbitGraph = defaultdict(list)
    pairs = [line.split(")") for line in input_text.splitlines()]
    for orbited, orbited_by in pairs:
        orbits[orbited].append(orbited_by)
    return orbits


def orbit_depths(orbit_graph: OrbitGraph) -> Iterator[int]:
    """Yields node depths in a breadth-first traversal of the orbit graph."""
    queue = deque([(0, "COM")])
    while queue:
        depth, body = queue.popleft()
        yield depth
        queue.extend(
            [(depth + 1, orbiting_body) for orbiting_body in orbit_graph[body]]
        )


def find_shortest_path(
    directed_orbit_graph: OrbitGraph, source: str = "YOU", dest: str = "SAN"
) -> Tuple[int, List[str]]:
    orbits = directed_to_undirected_graph(directed_orbit_graph)

    class BFSEntry(NamedTuple):
        depth: int
        current_node: str
        path_from_source: List[str]

    start = orbits[source][0]  # Body orbited by source
    queue = deque([BFSEntry(0, start, [])])

    min_distance = math.inf
    shortest_path: List[str] = []
    while queue:
        depth, current_node, path = queue.popleft()
        if depth >= min_distance:
            # Cut off search branch if distance is already too long.
            continue

        # Filter already-visited nodes from next steps to avoid cycles.
        unvisited_neighbours = [n for n in orbits[current_node] if n not in path]

        current_path = path + [current_node]
        if dest in unvisited_neighbours:
            # The earlier check ensures the current distance is known to be
            # shorter than the previous-shortest, so we can just assign the
            # current distance and path without testing again.
            min_distance = depth
            shortest_path = current_path
        else:
            queue.extend(
                [
                    BFSEntry(depth + 1, neighbour, current_path)
                    for neighbour in unvisited_neighbours
                ]
            )

    if min_distance is math.inf:
        raise ValueError(f"Node {dest} not present in orbit graph.")

    # Turn off mypy checking for the return value because the use of math.inf
    # (which is a float) earlier causes it to complain about the return type
    # really being a Union[float, int], where for any valid input graph the
    # dest node will be found and min_distance will be an int.
    return min_distance, shortest_path  # type: ignore


def directed_to_undirected_graph(directed: OrbitGraph) -> OrbitGraph:
    """Create undirected graph from the given directed graph."""
    # Make an undirected graph so that we can traverse orbits in
    # either direction. The original orbit graph is strictly
    # orbited_body -> orbiting body, ie a directed acyclic graph.
    undirected = deepcopy(directed)
    for orbited_body, orbiting_bodies in directed.items():
        for orbiting in orbiting_bodies:
            undirected[orbiting].append(orbited_body)
    return undirected


def main(orbit_graph: OrbitGraph) -> Tuple[int, int]:
    part_one_solution = sum(orbit_depths(orbit_graph))
    part_two_solution, shortest_path = find_shortest_path(orbit_graph)
    return (part_one_solution, part_two_solution)


def test_orbit_depths() -> None:
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
    orbit_graph = parse_input(orbits)
    assert sum(orbit_depths(orbit_graph)) == 42


def test_find_shortest_path() -> None:
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
K)L
K)YOU
I)SAN"""
    orbit_graph = parse_input(orbits)
    distance, path = find_shortest_path(orbit_graph)
    assert distance == 4
    assert path == ["K", "J", "E", "D", "I"]


if __name__ == "__main__":
    parsed = parse_input(aoc.load_puzzle_input(2019, DAY))
    part_one_solution, part_two_solution = main(parsed)
    print(
        aoc.format_solution(
            title=__doc__,
            part_one=part_one_solution,
            part_two=part_two_solution,
        )
    )
