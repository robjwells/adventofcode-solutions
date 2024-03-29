#!/usr/bin/env python3
"""Advent of Code 2015, Day 9: All in a Single Night"""

from collections import defaultdict, deque, namedtuple

import aoc
import pytest


def parse_input(text):
    """Parse a list of destinations and weights

    Returns a list of tuples (source, dest, weight).

    Edges in this graph are undirected.

    The input contains multiple rows appearing like so:
        A to B = W
    Where A and B are strings and W is the weight to travel
    between them in a graph.
    """

    def parse_line(line):
        """Parse a single line of the input"""
        parts = line.split()
        return (parts[0], parts[2], int(parts[4]))

    return [parse_line(line) for line in text.splitlines()]


Edge = namedtuple("Edge", ("src", "dst", "weight"))


class Graph:
    """Undirected weighted graph"""

    def __init__(self):
        self.connections = defaultdict(list)

    def __str__(self):
        output = ""
        for l in self.connections.values():
            output += "\n".join(str(e) for e in l)
            output += "\n\n"
        return output.rstrip()

    def add_edge(self, src: str, dst: str, weight: int):
        """Add an edge to the graph and corresponding nodes if new"""
        self.connections[src].append(Edge(src, dst, weight))
        self.connections[dst].append(Edge(dst, src, weight))

    def weight(self, src: str, dst: str):
        """Return the weight between two nodes if edge exists"""
        for e in self.connections[src]:
            if e.dst == dst:
                return e.weight

    def edges(self, node: str):
        """Return all edges for node"""
        return self.connections[node]


def create_graph(parsed_lines):
    """Create a graph from lines parsed from the input file"""
    graph = Graph()
    for src, dst, weight in parsed_lines:
        graph.add_edge(src, dst, weight)
    return graph


def breadth_first_search(graph: Graph, start: str):
    """Yield paths in graph from node start that visit all nodes once

    Args:
        graph (Graph): The graph to be traversed
        start (str): The starting node for paths

    Yields:
        list: A list of strings representing nodes in graph, of
            a length equal to the number of nodes in graph
    """
    total_nodes = len(graph.connections)
    queue = deque([[start]])

    while queue:
        temp_path = queue.pop()

        if len(temp_path) != total_nodes:
            # Not visited all nodes, so append new paths to queue that include
            # unvisited nodes, considering nodes that are reachable from
            # the last node in the path.
            for edge in graph.edges(temp_path[-1]):
                if edge.dst not in temp_path:
                    queue.append(temp_path + [edge.dst])
        else:
            yield temp_path


def total_weight(graph, path):
    """Sum the weights of the edges between nodes in path

    Args:
        graph (Graph): A graph containing nodes and edges between them
        path (list of str): A list of strings representing nodes in graph

    Returns:
        int: The total weight of all the implied edges in path
    """
    pairs = zip(path, path[1:])
    weight = sum(graph.weight(*p) for p in pairs)
    return weight


def search_all(graph):
    """Find every Hamiltonian path in graph and its weight

    A Hamiltonian path is a route traversing graph that visits each
    node exactly once.

    Args:
        graph (Graph): A graph containing nodes and edges between them

    Returns:
        list of ([str], int) tuples: Hamiltonian paths with their weights
    """
    paths = []
    for start_node in graph.connections:
        for path in breadth_first_search(graph, start_node):
            paths.append((path, total_weight(graph, path)))
    return paths


def search_all_min(graph):
    """Find the shortest Hamiltonian path in graph."""
    return min(search_all(graph), key=lambda t: t[1])


def search_all_max(graph):
    """Find the longest Hamiltonian path in graph."""
    return max(search_all(graph), key=lambda t: t[1])


TEST_PARSED_INSTRUCTIONS = [
    ("London", "Dublin", 464),
    ("London", "Belfast", 518),
    ("Dublin", "Belfast", 141),
]


def test_parse():
    """Test parsing of a list of destinations and weights"""
    puzzle_input = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""
    result = parse_input(puzzle_input)
    assert result == TEST_PARSED_INSTRUCTIONS


@pytest.fixture
def sample_graph():
    """Return a graph of the sample instructions"""
    return create_graph(TEST_PARSED_INSTRUCTIONS)


def test_shortest(sample_graph):
    """search_all_min returns the known shortest distance"""
    assert search_all_min(sample_graph)[1] == 605


def test_longest(sample_graph):
    """search_all_max returns the known longest distance"""
    assert search_all_max(sample_graph)[1] == 982


@pytest.fixture
def real_input_graph():
    """Return a graph created from the real puzzle input"""
    puzzle_input = aoc.load_puzzle_input(2015, 9)

    instructions = parse_input(puzzle_input)
    return create_graph(instructions)


def test_longest_gives_expected_result_with_real_input(real_input_graph):
    """search_all_max returns known good result when given real day's input

    This is mostly to check that refactoring doesn't change the
    'real' output from that which has already been accepted by
    the Advent of Code website.
    """
    assert search_all_max(real_input_graph)[1] == 804


def test_shortest_gives_expected_result_with_real_input(real_input_graph):
    """search_all_min returns known good result when given real day's input

    This is mostly to check that refactoring doesn't change the
    'real' output from that which has already been accepted by
    the Advent of Code website.
    """
    assert search_all_min(real_input_graph)[1] == 207


def main(puzzle_input):
    instructions = parse_input(puzzle_input)
    graph = create_graph(instructions)

    print("Shortest:", search_all_min(graph))
    print("Longest:", search_all_max(graph))


if __name__ == "__main__":
    puzzle_input = aoc.load_puzzle_input(2015, 9)
    main(puzzle_input)
