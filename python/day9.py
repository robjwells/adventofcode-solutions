#!/usr/local/bin/python3

from collections import defaultdict, deque, namedtuple
import pathlib
import sys

input_file = pathlib.Path(__file__).parent.parent.joinpath('day9_input.txt')


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
    for src, dst, weight in lines:
        graph.add_edge(src, dst, weight)
    return graph


def breadth_first_search(graph: Graph, start: str):
    """Search the graph for the shortest path that vistis all nodes

    Returns the shortest path (a list of strings) and the weight (int)
    """
    def total_weight(path):
        pairs = zip(path, path[1:])
        weight = sum(graph.weight(*p) for p in pairs)
        return weight

    queue = deque([[start]])
    all_nodes = graph.connections.keys()

    shortest_path = None
    lowest_weight = sys.maxsize

    while queue:
        temp_path = queue.pop()
        if total_weight(temp_path) >= lowest_weight:
            continue
        if all_nodes - set(temp_path):
            # Not visited all nodes yet
            for edge in graph.edges(temp_path[0]):
                if edge.dst not in temp_path:
                    new_path = temp_path + [edge.dst]
                    queue.append(new_path)
        else:
            # Visited all nodes
            temp_weight = total_weight(temp_path)
            if temp_weight < lowest_weight:
                lowest_weight = temp_weight
                shortest_path = temp_path

    return shortest_path, lowest_weight


if __name__ == '__main__':
    with open(input_file) as f:
        lines = parse_input(f.read())
    graph = create_graph(lines)
    start_node = list(graph.connections.keys())[0]
    path, weight = breadth_first_search(graph, start_node)

    print(f'Shortest path is:\n{path}')
    print(f'Weight is {weight}')
