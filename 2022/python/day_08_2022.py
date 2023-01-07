from __future__ import annotations
from enum import Enum

import pytest

from util import read_input

Grid = list[list[int]]


class Direction(Enum):
    value: tuple[int, int]

    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)


def parse(s: str) -> Grid:
    return [[int(c) for c in line] for line in s.splitlines()]


def search(grid: Grid, vg: Grid, outer: range, inner: range, row_major: bool) -> None:
    for row in outer:
        previous_highest = -1
        for col in inner:
            val = grid[row][col] if row_major else grid[col][row]
            if val > previous_highest:
                if row_major:
                    vg[row][col] += 1
                else:
                    vg[col][row] += 1
            previous_highest = max(previous_highest, val)


def solve_part_one(grid: Grid) -> int:
    forward = range(len(grid))
    backward = range(len(grid) - 1, -1, -1)
    visibility = [[0 for _ in forward] for _ in forward]

    search(grid, visibility, forward, forward, True)
    search(grid, visibility, forward, backward, True)
    search(grid, visibility, forward, forward, False)
    search(grid, visibility, forward, backward, False)

    return sum([len([v for v in row if v > 0]) for row in visibility])


def in_bounds(row: int, col: int, grid_size: int) -> bool:
    return 0 <= row < grid_size and 0 <= col < grid_size


def trees_in_view(grid: Grid, row: int, col: int, direction: Direction) -> int:
    row_delta, col_delta = direction.value
    grid_size = len(grid)

    our_tree = grid[row][col]
    visible_trees = 0
    row += row_delta
    col += col_delta

    while in_bounds(row, col, grid_size):
        tree = grid[row][col]
        visible_trees += 1
        if tree >= our_tree:
            break

        row += row_delta
        col += col_delta
    return visible_trees


def solve_part_two(grid: Grid) -> int:
    size = len(grid)
    inner = range(1, size - 1)
    scenic = [[1 for _ in range(size)] for _ in range(size)]
    row_col_pairs = ((row, col) for row in inner for col in inner)

    for row, col in row_col_pairs:
        for direction in Direction:
            n = trees_in_view(grid, row, col, direction)
            scenic[row][col] *= n

    flattened = [score for row in scenic for score in row]
    return max(flattened)


def main() -> None:
    puzzle_input = read_input(8)
    grid = parse(puzzle_input)

    part_one = solve_part_one(grid)
    assert part_one == 1_782
    print(f"Part one: {part_one:,}")

    part_two = solve_part_two(grid)
    assert part_two == 474_606
    print(f"Part two: {part_two:,}")


if __name__ == "__main__":
    main()


SAMPLE_INPUT = """\
30373
25512
65332
33549
35390
"""


def test_solve_part_one_sample_input() -> None:
    assert solve_part_one(parse(SAMPLE_INPUT)) == 21


@pytest.mark.parametrize(
    ["row", "col", "up", "left", "right", "down"],
    [
        (1, 2, 1, 1, 2, 2),
        (3, 2, 2, 2, 2, 1),
    ],
)
def test_trees_in_view(
    row: int, col: int, up: int, left: int, right: int, down: int
) -> None:
    grid = parse(SAMPLE_INPUT)
    assert trees_in_view(grid, row, col, Direction.UP) == up
    assert trees_in_view(grid, row, col, Direction.LEFT) == left
    assert trees_in_view(grid, row, col, Direction.RIGHT) == right
    assert trees_in_view(grid, row, col, Direction.DOWN) == down


def test_solve_part_two_sample_input() -> None:
    assert solve_part_two(parse(SAMPLE_INPUT)) == 8
