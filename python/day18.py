#!/usr/bin/env python3

import pathlib

input_file = pathlib.Path(__file__).parent.parent.joinpath('day18_input.txt')


class Grid:
    """An animated light grid"""
    @staticmethod
    def _parse_input(text):
        return [1 if s == '#' else 0 for s in text.replace('\n', '')]

    def __init__(self, lights_string, width=None, broken_corners=False):
        """Create grid from the puzzle input (lights_string)

        Raises ValueError if width doesn't divide cleanly into total length,
        or if the grid is not a square and the width is not provided.
        """
        parsed = self._parse_input(lights_string)
        self.lights = parsed
        self.total_lights = len(self.lights)

        if width is None:
            width = self.total_lights ** 0.5
            if not width.is_integer():
                raise ValueError(
                    f'Grid is not a square and width was not provided.')
        self.width = int(width)

        if self.total_lights % self.width:
            raise ValueError(
                f'Grid of length {len(lights_string)} and width {width}'
                ' is not rectangular.')

        self.history = []

        self.broken_corners = broken_corners
        if broken_corners:
            self.corner_indices = (
                0, self.width - 1,
                self.total_lights - self.width,
                self.total_lights - 1)
            for idx in self.corner_indices:
                self.lights[idx] = 1

    def _neighbour_indices(self, index):
        """Return index’s neighbours on a rectangular grid

        The 'grid' is virtual so the specified width and
        length of the light list are used to determine if
        positions are on the edge or in the corners, and
        only return indices for neighbours inside the grid.
        """
        w = self.width

        # These aren't always safe, but filtered later
        # along with the upper and lower diagonals.
        positions = [-w, w]
        if index % w != 0:  # Not on the left-hand edge
            positions.extend([-(w + 1), -1, w - 1])
        if (index + 1) % w != 0:  # Not on the right-hand edge
            positions.extend([-(w - 1), 1, w + 1])

        indices = [i for i in (index + p for p in positions)
                   if 0 <= i < self.total_lights]
        return indices

    def neighbours_lit(self, target, light_state):
        """Return the number of neighbours that are turned on

        light_state is a list of lights, so toggles don't affect
        other toggles in the same animation step.
        """
        indices = self._neighbour_indices(target)
        return sum(light_state[idx] for idx in indices)

    def toggle(self, index, light_state):
        """Toggle the light at index based on neighbours

        light_state is a list of lights, so toggles don't affect
        other toggles in the same animation step.

        A light which is on stays on when 2 or 3 neighbours
        are on, and turns off otherwise.

        A light which is off turns on if exactly 3 neighbours
        are on, and stays off otherwise.
        """
        if self.broken_corners and index in self.corner_indices:
            return
        lit = light_state[index]
        neighbour_score = self.neighbours_lit(index, light_state)
        if lit and neighbour_score not in (2, 3):
            self.lights[index] = 0
        elif not lit and neighbour_score == 3:
            self.lights[index] = 1

    def animate(self, to_stage):
        """Animate the grid by performing repeated rounds of toggles

        History is used to store previous animation stages to
        save time in repeated calls.
        """
        if not self.history:
            self.history.append(self.lights[:])
            light_state = self.lights[:]
            furthest_stage = 0
        elif to_stage <= len(self.history) - 1:
            return self.history[to_stage][:]
        else:
            light_state = self.history[-1]
            furthest_stage = len(self.history) - 1

        for stage in range(furthest_stage + 1, to_stage + 1):
            for idx in range(self.total_lights):
                self.toggle(idx, light_state)
            self.history.append(self.lights[:])
            light_state = self.lights[:]
        return light_state


def test_parse():
    assert Grid._parse_input('......\n######') == [0, 0, 0, 0, 0, 0,
                                                   1, 1, 1, 1, 1, 1]


def test_misshaped_grid():
    try:
        Grid(lights_string=('.' * 5), width=2)
    except ValueError:
        assert True
    else:
        assert False


def test_neighbours():
    g = Grid(lights_string=('#' * 36), width=6)
    assert sorted(g._neighbour_indices(0)) == [1, 6, 7]
    assert sorted(g._neighbour_indices(1)) == [0, 2, 6, 7, 8]
    assert sorted(g._neighbour_indices(5)) == [4, 10, 11]
    assert sorted(g._neighbour_indices(6)) == [0, 1, 7, 12, 13]
    assert sorted(g._neighbour_indices(7)) == [0, 1, 2, 6, 8, 12, 13, 14]
    assert sorted(g._neighbour_indices(29)) == [22, 23, 28, 34, 35]
    assert sorted(g._neighbour_indices(35)) == [28, 29, 34]


def test_neighbours_lit():
    lights = '''\
....
.##.
.##.
....'''
    g = Grid(lights_string=lights, width=4)
    light_state = g.lights[:]
    assert g.neighbours_lit(0, light_state) == 1
    assert g.neighbours_lit(4, light_state) == 2
    assert g.neighbours_lit(5, light_state) == 3
    assert g.neighbours_lit(14, light_state) == 2


def test_toggle():
    lights = '''\
....
.###
.##.
....'''
    g = Grid(lights_string=lights, width=4)
    light_state = g.lights[:]
    for index, expected in [(0, 0), (2, 1), (11, 1), (14, 0)]:
        g.toggle(index, light_state)
        assert g.lights[index] == expected


def test_sample():
    lights = '''\
.#.#.#
...##.
#....#
..#...
#.#..#
####..'''
    g = Grid(lights_string=lights)
    assert sum(g.animate(5)) == 4
    bg = Grid(lights_string=lights, broken_corners=True)
    assert sum(bg.animate(5)) == 17


def main():
    grid_text = input_file.read_text()
    grid = Grid(lights_string=grid_text, width=100)
    print(sum(grid.animate(100)))
    broken_grid = Grid(lights_string=grid_text, width=100,
                       broken_corners=True)
    print(sum(broken_grid.animate(100)))


if __name__ == '__main__':
    main()
