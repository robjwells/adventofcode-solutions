from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import Any, Generic, NamedTuple, Optional, cast

from aoc_common import T, load_puzzle_input, report_solution


class Location(NamedTuple):
    row: int
    column: int


class Direction(tuple[int, int], Enum):
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
class Grid2D(Generic[T]):
    grid: list[list[T]]
    width: int
    height: int
    cursor_index: Location

    def __init__(
        self, width: int, height: int, start_index: Location, grid: list[list[T]]
    ) -> None:
        self.grid = grid
        self.width = width
        self.height = height
        self.cursor_index = start_index

    @property
    def cursor_item(self) -> T:
        row, column = self.cursor_index
        return self.grid[row][column]

    def __str__(self) -> str:
        return f"Cursor at: {self.cursor_index} ({self.cursor_item})\t{self.grid}"

    def _new_location_is_valid(self, new_row: int, new_col: int) -> bool:
        return 0 <= new_row < self.width and 0 <= new_col < self.height

    def move(self, direction: Direction) -> Grid2D[T]:
        drow, dcol = cast(tuple[int, int], direction.value)
        nrow, ncol = self.cursor_index.row + drow, self.cursor_index.column + dcol
        if self._new_location_is_valid(nrow, ncol):
            return type(self)(self.width, self.height, Location(nrow, ncol), self.grid)
        return self


class SquareKeypad(Grid2D[int]):
    def __init__(
        self,
        width: int = 3,
        height: int = 3,
        start_index: Location = Location(1, 1),
        grid: list[list[int]] | None = None,
    ) -> None:
        if grid is None:
            grid = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        super().__init__(width, height, start_index, grid)


class DiamondKeypad(Grid2D[Optional[str]]):
    # fmt:off
    _DIAMOND_GRID: list[list[str | None]] = [
        [None, None, "1", None, None],
         [None, "2", "3", "4", None, None],
          ["5", "6", "7", "8", "9"],
         [None, "A", "B", "C", None],
        [None, None, "D", None, None],
    ]
    # fmt:on

    def __init__(
        self,
        width: int = 5,
        height: int = 5,
        start_index: Location = Location(2, 0),
        grid: list[list[str | None]] | None = None,
    ) -> None:
        if grid is None:
            grid = self._DIAMOND_GRID
        super().__init__(width, height, start_index, grid)

    def _new_location_is_valid(self, new_row: int, new_col: int) -> bool:
        return (
            super()._new_location_is_valid(new_row, new_col)
            and self.grid[new_row][new_col] is not None
        )


def parse_instructions(string: str) -> list[list[Direction]]:
    return [[Direction.parse(c) for c in line] for line in string.splitlines()]


def follow_all_instructions(
    instructions: list[list[Direction]], grid: Grid2D[T]
) -> list[Grid2D[T]]:
    return [reduce(lambda grid, d: grid.move(d), group, grid) for group in instructions]


def find_grid_code(instructions: list[list[Direction]], grid: Grid2D[Any]) -> str:
    return "".join(
        [str(grid.cursor_item) for grid in follow_all_instructions(instructions, grid)]
    )


if __name__ == "__main__":
    instructions = parse_instructions(load_puzzle_input(day=2))
    report_solution(
        puzzle_title="Day 2: Bathroom Security",
        part_one_solution=find_grid_code(instructions, SquareKeypad()),
        part_two_solution=find_grid_code(instructions, DiamondKeypad()),
    )
