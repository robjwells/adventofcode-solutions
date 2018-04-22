#!/usr/bin/env python3
"""Advent of Code 2015, Day 9: All in a Single Night"""

from collections import defaultdict, deque, namedtuple
import operator


TEST_PARSED_INSTRUCTIONS = [
    ('London', 'Dublin', 464),
    ('London', 'Belfast', 518),
    ('Dublin', 'Belfast', 141)]


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
    assert result == TEST_PARSED_INSTRUCTIONS


Edge = namedtuple('Edge', ('src', 'dst', 'weight'))


class Graph:
    """Undirected weighted graph"""
    def __init__(self):
        self.connections = defaultdict(list)

    def __str__(self):
        output = ''
        for l in self.connections.values():
            output += '\n'.join(
                str(e) for e in l)
            output += '\n\n'
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


def breadth_first_search(graph: Graph, start: str, mode: str):
    """Search the graph for the best path that visits all nodes

    Returns the path that is best according to the mode: either min or
    max.

    The string mode is a bit of a hack, and removes the ability to
    have a generic checking function. But it also allows me to optimise
    the minimisation case by skipping paths that are too long despite
    not visiting all nodes.
    """
    def total_weight(path):
        pairs = zip(path, path[1:])
        weight = sum(graph.weight(*p) for p in pairs)
        return weight

    total_nodes = len(graph.connections)
    total_edges = len([e for l in graph.connections.values() for e in l])
    average_edge_weight = sum([
        edge.weight for edge_list in graph.connections.values()
        for edge in edge_list
        ]) / total_edges

    # FIXME: Switching on strings like this is super-gross.
    #        The design needs improving so that either objective
    #        functions are passed into the search, or the search
    #        function is called by something else which does its
    #        own bookkeeping, or the search is specialised for either.
    if mode == 'min':
        minimise = True
        check_func = operator.__lt__
    else:
        minimise = False
        check_func = operator.__gt__
        best_weight = 0

    queue = deque([[start]])
    all_nodes = graph.connections.keys()
    best_path = None
    best_weight = (total_nodes - 1) * average_edge_weight

    while queue:
        temp_path = queue.pop()
        temp_weight = total_weight(temp_path)
        if minimise and check_func(best_weight, temp_weight):
            # Bail if path is too long already when minimising length
            continue
        elif check_func((len(temp_path) - 1) * average_edge_weight,
                        temp_weight):
            # If the path is below average, move on to the next
            continue
        if all_nodes - set(temp_path):
            # Not visited all nodes yet
            for edge in graph.edges(temp_path[0]):
                if edge.dst not in temp_path:
                    new_path = temp_path + [edge.dst]
                    queue.append(new_path)
        else:
            # Visited all nodes
            if check_func(temp_weight, best_weight):
                best_weight = temp_weight
                best_path = temp_path

    return best_path, best_weight


# FIXME: Duplicated code in the search_all_* functions
def search_all_min(graph):
    results = []
    for start_node in list(graph.connections.keys()):
        results.append(breadth_first_search(graph, start_node, mode='min'))
    return min(results, key=lambda x: x[1])


# FIXME: Duplicated code in the search_all_* functions
def search_all_max(graph):
    results = []
    for start_node in list(graph.connections.keys()):
        results.append(breadth_first_search(graph, start_node, mode='max'))
    return max(results, key=lambda x: x[1])


def test_shortest():
    """search_all_min returns the known shortest distance"""
    graph = create_graph(TEST_PARSED_INSTRUCTIONS)
    assert search_all_min(graph)[1] == 605


def test_longest():
    """search_all_max returns the known longest distance"""
    graph = create_graph(TEST_PARSED_INSTRUCTIONS)
    assert search_all_max(graph)[1] == 982


def main(puzzle_input):
        instructions = parse_input(puzzle_input)
        graph = create_graph(instructions)

        print('Shortest:', search_all_min(graph))
        print('Longest:', search_all_max(graph))


if __name__ == '__main__':
    with open('../input/2015-09.txt') as f:
        puzzle_input = f.read()
