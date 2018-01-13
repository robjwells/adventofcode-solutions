#!/usr/local/bin/python3


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


def test_LightGrid_setup():
    """LightGrid correctly initialises 1,000 * 1,000 grid of lights

    All lights should start 'off', with the test being that the sum of
    the entire matrix should be 0, with 0 representing an unlit light.
    """
    grid = LightGrid().matrix
    assert len(grid) == 1000  # 1,000 rows
    for row in grid:
        assert len(row) == 1000  # 1,000 columns in each row
    assert sum(sum(row) for row in grid) == 0


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
        assert sum(sum(row) for row in grid.matrix) == total_on


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
        assert sum(sum(row) for row in grid.matrix) == 1000 * 1000 - total_off


if __name__ == '__main__':
    with open('../input/2015-06.txt') as f:
        puzzle_input = [line.rsplit(maxsplit=3)
                        for line in f.read().splitlines()]

    lights = LightGrid()

    for instruction, start, _, end in puzzle_input:
        start_x, start_y = [int(part) for part in start.split(',')]
        end_x, end_y = [int(part) for part in end.split(',')]

        if instruction == 'turn on':
            # func = lambda state: True         # Part one
            func = lambda state: state + 1      # Part two
        elif instruction == 'turn off':
            # func = lambda state: False        # Part one
            func = lambda state: state - 1 if state else 0   # Part two
        elif instruction == 'toggle':
            # func = lambda state: not state    # Part one
            func = lambda state: state + 2      # Part two

        for col in range(start_x, end_x + 1):
            row_part = slice(start_y, end_y + 1)
            lights[col][row_part] = map(func, lights[col][row_part])

    print(sum(sum(col) for col in lights))
