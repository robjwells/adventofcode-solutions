#!/usr/local/bin/python3


import pytest


class LightGrid:
    """A grid of lights that can be toggled on and off

    The grid can be an arbitrary size, but by default is 1,000 lights wide
    and 1,000 lights tall.

    The grid is initialised with all lights turned off, which is represented
    by using False (equivalent to 0).

    Light ranges can be turned on, off, or toggled.
    """
    def __init__(self, rows=1000, columns=1000):
        self.matrix = [[False for _ in range(columns)]
                       for _ in range(rows)]

    @staticmethod
    def _col_slice_for_coords(start_coord, end_coord):
        """Return a slice for the column (y) part of the coordinates range

        The two coordinates designate a rectangular section of a matrix
        and are inclusive. The column slice is the same for each row.

        For example, given coordinates
            (0, 0) and (1, 1)
        return
            slice(0, 2)

        Or coordinates
            (499, 499) and (500, 500)
        return
            slice(499, 501)
        """
        return slice(start_coord[1], end_coord[1] + 1)

    def _manipulate(self, transformer, start_coord, end_coord):
        """Apply transformer to the range between start_coord and end_coord

        transformer is a function that takes one argument — the current
        state of the light in question — and returns the new state.
        """
        column_slice = self._col_slice_for_coords(start_coord, end_coord)
        for row in self.matrix[start_coord[0]:end_coord[0] + 1]:
            row[column_slice] = map(transformer, row[column_slice])

    def turn_on(self, start_coord, end_coord):
        """Turn on an inclusive rectangular range of lights"""
        self._manipulate(lambda state: True, start_coord, end_coord)

    def turn_off(self, start_coord, end_coord):
        """Turn off an inclusive rectangular range of lights"""
        self._manipulate(lambda state: False, start_coord, end_coord)

    def toggle(self, start_coord, end_coord):
        """Toggle the state of an inclusive range of lights"""
        self._manipulate(lambda state: not state, start_coord, end_coord)

    def apply_instruction(self, mode, start_coord, end_coord):
        """Switch on string instruction to change lights

        Valid arguments for mode are: 'turn on', 'turn off', 'toggle'
        """
        try:
            method = getattr(self, mode.replace(' ', '_'))
            method(start_coord, end_coord)
        except AttributeError:
            raise ValueError(f'"{mode}" is not a valid grid method')

    def count_lights_on(self):
        """Total number of lights that are enabled"""
        return sum(sum(row) for row in self.matrix)


class DimmerGrid(LightGrid):
    """A grid of lights with adjustable brightness"""
    def turn_on(self, start_coord, end_coord):
        """Increase brightness of lights in rectangular range by 1"""
        self._manipulate(lambda state: state + 1, start_coord, end_coord)

    def turn_off(self, start_coord, end_coord):
        """Decrease brightness of lights in rectangular range by 1 until 0"""
        self._manipulate(lambda state: state - 1 if state else 0,
                         start_coord, end_coord)

    def toggle(self, start_coord, end_coord):
        """Increase brightness of lights in rectangular range by 2"""
        self._manipulate(lambda state: state + 2, start_coord, end_coord)

    def total_brightness(self):
        """Total brightness of all the lights

        Internally this uses the inherited count_lights_on method
        because the approach of summing the lists in the matrix
        works as well for ints as it does for bools.
        """
        return self.count_lights_on()


def test_LightGrid_setup():
    """LightGrid correctly initialises 1,000 * 1,000 grid of lights

    All lights should start 'off', with the test being that the sum of
    the entire matrix should be 0, with 0 representing an unlit light.
    """
    grid = LightGrid()
    assert len(grid.matrix) == 1000  # 1,000 rows
    for row in grid.matrix:
        assert len(row) == 1000  # 1,000 columns in each row
    assert grid.count_lights_on() == 0


def test_LightGrid_turn_on():
    """LightGrid can turn on light ranges"""
    ranges = [
        ((0, 0), (999, 999)),
        ((0, 0), (999, 0)),
        ((499, 499), (500, 500))
        ]
    for start_coord, end_coord in ranges:
        grid = LightGrid()
        grid.turn_on(start_coord, end_coord)
        assert grid.matrix[start_coord[0]][start_coord[1]] == 1
        assert grid.matrix[end_coord[0]][end_coord[1]] == 1

        # Calculate how many lights should be on and compare
        # against a sum of the light grid
        row_range = range(start_coord[0], end_coord[0] + 1)
        col_range = range(start_coord[1], end_coord[1] + 1)
        total_on = len(row_range) * len(col_range)
        assert grid.count_lights_on() == total_on


def test_LightGrid_turn_off():
    """LightGrid can turn off light ranges"""
    ranges = [
        ((0, 0), (999, 999)),
        ((0, 0), (999, 0)),
        ((499, 499), (500, 500))
        ]
    for start_coord, end_coord in ranges:
        grid = LightGrid()
        # First turn on all the lights
        grid.turn_on((0, 0), (999, 999))

        grid.turn_off(start_coord, end_coord)
        assert grid.matrix[start_coord[0]][start_coord[1]] == 0
        assert grid.matrix[end_coord[0]][end_coord[1]] == 0

        # Calculate how many lights should be turned off and
        # compare against a sum of the light grid
        row_range = range(start_coord[0], end_coord[0] + 1)
        col_range = range(start_coord[1], end_coord[1] + 1)
        total_off = len(row_range) * len(col_range)
        assert grid.count_lights_on() == 1000 * 1000 - total_off


def test_LightGrid_toggle():
    """LightGrid can toggle light ranges"""
    ranges_and_expected = [
        ((0, 0), (999, 999), 1_000_000),
        ((0, 0), (999, 0), 1_000_000 - 1_000),
        ((499, 499), (500, 500), 1_000_000 - 1_000 - 4)
        ]
    grid = LightGrid()
    for start_coord, end_coord, expected_lights in ranges_and_expected:
        grid.toggle(start_coord, end_coord)
        assert grid.count_lights_on() == expected_lights


def test_DimmerGrid_turn_on():
    """DimmerGrid.turn_on increases light brightness by 1"""
    grid = DimmerGrid()
    expected = [1, 2]
    for _, brightness in zip(range(2), expected):
        grid.turn_on((0, 0), (0, 0))
        assert grid.matrix[0][0] == brightness


def test_DimmerGrid_turn_off():
    """DimmerGrid.turn_off decreases brightness by 1 to minimum of 0"""
    grid = DimmerGrid()
    coords = [(0, 0), (0, 0)]

    # Turn the brightness up on light (0, 0) to 2 to start
    grid.turn_on(*coords)
    grid.turn_on(*coords)
    assert grid.matrix[0][0] == 2

    # Start turning down to hit floor of 0
    expected = [1, 0, 0]
    for _, brightness in zip(range(3), expected):
        grid.turn_off(*coords)
        assert grid.matrix[0][0] == brightness


def test_DimmerGrid_toggle():
    """DimmerGrid.toggle increases brightness by 2"""
    grid = DimmerGrid()
    expected = [2, 4]
    for _, brightness in zip(range(2), expected):
        grid.toggle((0, 0), (0, 0))
        assert grid.matrix[0][0] == brightness


@pytest.mark.parametrize('method,coords,brightness', [
    ('turn on', [(0, 0), (0, 0)], 1),
    ('toggle', [(0, 0), (999, 999)], 2000000),
])
def test_DimmerGrid_total_brightness(method, coords, brightness):
    """DimmerGrid correctly reports total brightness"""
    grid = DimmerGrid()
    grid.apply_instruction(method, *coords)
    assert grid.total_brightness() == brightness


def parse_instruction(input_line):
    """Parse a line of puzzle input into an action and two coordinates"""

    def parse_coord_str(coordinate_string):
        """Parse a coordinate string into a tuple of ints"""
        return tuple(int(n) for n in coordinate_string.split(','))

    action, start_coord_str, _, end_coord_str = input_line.rsplit(maxsplit=3)
    return (action,
            parse_coord_str(start_coord_str),
            parse_coord_str(end_coord_str))


def test_parse_instruction():
    """parse_instruction correctly interprets a single line of puzzle input"""
    puzzle_input_lines = [
        'turn on 0,0 through 999,999',
        'toggle 0,0 through 999,0',
        'turn off 499,499 through 500,500']
    expected = [
        ('turn on', (0, 0), (999, 999)),
        ('toggle', (0, 0), (999, 0)),
        ('turn off', (499, 499), (500, 500))]
    for input_line, expected_result in zip(puzzle_input_lines, expected):
        assert parse_instruction(input_line) == expected_result


def main(puzzle_input):
    lights = LightGrid()
    for line in puzzle_input:
        lights.apply_instruction(*parse_instruction(line))
    print('Part one, total lights lit:', lights.count_lights_on())


if __name__ == '__main__':
    with open('../input/2015-06.txt') as f:
        puzzle_input = f.read().splitlines()
    main(puzzle_input)
