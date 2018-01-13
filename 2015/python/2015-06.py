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
