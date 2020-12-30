from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import reduce
from itertools import count
from typing import List, NamedTuple, Tuple, cast

from aoc_common import load_puzzle_input, report_solution


class Location(NamedTuple):
    x: int
    y: int


class Direction(Tuple[int, int], Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

    @classmethod
    def parse(cls, s: str) -> Direction:
        if s == "U":
            return cls.UP
        if s == "R":
            return cls.RIGHT
        if s == "D":
            return cls.DOWN
        if s == "L":
            return cls.LEFT
        raise ValueError("Invalid string for Direction (must be U, R, D or L).")


@dataclass
class Grid2D:
    grid: List[List[int]]
    width: int
    height: int
    cursor_index: Location

    def __init__(
        self, width: int, height: int, start_index: Location, fill_from: int = 1
    ):
        counter = count(start=fill_from)
        self.grid = [[next(counter) for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self.cursor_index = start_index

    @property
    def cursor_digit(self) -> int:
        row, column = self.cursor_index
        return self.grid[row][column]

    def __str__(self) -> str:
        return f"Cursor at: {self.cursor_index} ({self.cursor_digit})\t{self.grid}"

    def _new_location_is_valid(self, new_x: int, new_y: int) -> bool:
        return 0 <= new_x < self.width and 0 <= new_y < self.height

    def move(self, direction: Direction) -> Grid2D:
        dx, dy = cast(Tuple[int, int], direction.value)
        nx, ny = self.cursor_index.x + dx, self.cursor_index.y + dy
        if self._new_location_is_valid(nx, ny):
            return Grid2D(self.width, self.height, Location(nx, ny))
        else:
            return self


def parse_instructions(string: str) -> List[List[Direction]]:
    return [[Direction.parse(c) for c in line] for line in string.splitlines()]


def follow_all_instructions(instructions: List[List[Direction]]) -> List[Grid2D]:
    return [
        reduce(lambda grid, d: grid.move(d), group, Grid2D(3, 3, Location(1, 1)))
        for group in instructions
    ]


def find_square_grid_code(instructions: List[List[Direction]]) -> str:
    return "".join(
        [str(grid.cursor_digit) for grid in follow_all_instructions(instructions)]
    )


if __name__ == "__main__":
    instructions = parse_instructions(load_puzzle_input(day=2))
    square_grid_code = find_square_grid_code(instructions)
    report_solution(
        puzzle_title="Day 2: Bathroom Security", part_one_solution=square_grid_code
    )
