#!/usr/local/bin/python3


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


