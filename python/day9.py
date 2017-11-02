#!/usr/local/bin/python3

from collections import deque, namedtuple

def parse_input(text):
    """Parse a list of destinations and weights

    Returns a list of tuples (source, dest, weight).

    Edges in this graph and undirected.

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


def test_parse():
    """Test parsing of a list of destinations and weights"""
    puzzle_input = '''\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141'''
    result = parse_input(puzzle_input)
    assert result == [
        ('London', 'Dublin', 464),
        ('London', 'Belfast', 518),
        ('Dublin', 'Belfast', 141)
        ]


Edge = namedtuple('Edge', ('src', 'dst', 'weight'))
# Node = namedtuple('Node', ('value')) # Might just be able to use strings

class Graph:
    """Undirected weighted graph"""
    def __init__(self):
        self.connections = dict()

    def add_edge(self, src: str, dst: str, weight: int):
        """Add an edge to the graph and corresponding nodes if new"""
        self.connections[src][dst] = Edge(src, dst, weight)
        self.connections[dst][src] = Edge(dst, src, weight)

    def weight(self, src: str, dst: str):
        """Return the weight between two nodes if edge exists"""
        return self.connections[src].get(dst).weight

    def edges(self, node: str):
        """Return all edges for node"""
        return self.connections[node].values()
