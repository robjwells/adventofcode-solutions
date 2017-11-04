#!/usr/bin/env python3

import pathlib

input_file = pathlib.Path(__file__).parent.parent.joinpath('day18_input.txt')


class Grid:
    """An animated light grid"""
    @staticmethod
    def _parse_input(text):
        return [1 if s == '#' else 0 for s in text.replace('\n', '')]

    def __init__(self, lights_string, width=100):
        """Lights is a list of numbers, 1 for on, 0 for off"""
        self.lights = self._parse_input(lights_string)
        self.total_lights = len(self.lights)
        self.width = width

    def neighbour_indices(self, index):
        w = self.width

        # These aren't always safe, but filtered later
        # along with the upper and lower diagonals.
        positions = [-w, w]
        if index % 6 != 0:  # Not on the left-hand edge
            positions.extend([-(w + 1), -1, w - 1])
        if (index + 1) % 6 != 0:  # Not on the right-hand edge
            positions.extend([-(w - 1), 1, w + 1])

        indices = [i for i in (index + p for p in positions)
                   if 0 <= i < self.total_lights]
        return indices


def test_parse():
    assert Grid._parse_input('......\n######') == [0, 0, 0, 0, 0, 0,
                                                   1, 1, 1, 1, 1, 1]


def test_neighbours():
    g = Grid(lights_string=('#' * 36), width=6)
    assert sorted(g.neighbour_indices(0)) == [1, 6, 7]
    assert sorted(g.neighbour_indices(1)) == [0, 2, 6, 7, 8]
    assert sorted(g.neighbour_indices(5)) == [4, 10, 11]
    assert sorted(g.neighbour_indices(6)) == [0, 1, 7, 12, 13]
    assert sorted(g.neighbour_indices(7)) == [0, 1, 2, 6, 8, 12, 13, 14]
    assert sorted(g.neighbour_indices(29)) == [22, 23, 28, 34, 35]
    assert sorted(g.neighbour_indices(35)) == [28, 29, 34]
