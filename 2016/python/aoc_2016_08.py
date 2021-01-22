from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from typing import Iterable

import pytest
from lark import Lark, Transformer

from aoc_common import load_puzzle_input, report_solution

_grammar = """
    ?start: turn_on | rotate_row | rotate_column

    turn_on: "rect " INT "x" INT
    rotate_row: "rotate row y=" INT " by " INT
    rotate_column: "rotate column x=" INT " by " INT

    %import common.INT
"""


class Instruction:
    ...


@dataclass(frozen=True)
class TurnOn(Instruction):
    width: int
    height: int


@dataclass(frozen=True)
class Rotate(Instruction):
    index: int
    amount: int


@dataclass(frozen=True)
class RotateRow(Rotate):
    ...


@dataclass(frozen=True)
class RotateColumn(Rotate):
    ...


class _Transformer(Transformer[Instruction]):
    INT = int

    @staticmethod
    def turn_on(args: tuple[int, int]) -> TurnOn:
        return TurnOn(*args)

    @staticmethod
    def rotate_row(args: tuple[int, int]) -> RotateRow:
        return RotateRow(*args)

    @staticmethod
    def rotate_column(args: tuple[int, int]) -> RotateColumn:
        return RotateColumn(*args)


_parse = Lark(_grammar, parser="lalr").parse
_transform = _Transformer().transform


def parse(string: str) -> Instruction:
    return _transform(_parse(string))


@pytest.mark.parametrize(
    "string,expected",
    [
        ("rect 3x2", TurnOn(3, 2)),
        ("rotate column x=1 by 1", RotateColumn(1, 1)),
        ("rotate row y=0 by 4", RotateRow(0, 4)),
    ],
)
def test_parser(string: str, expected: Instruction) -> None:
    assert parse(string) == expected


Row = list[str]
Grid = list[Row]


@dataclass(frozen=True, init=False)
class Screen:
    width: int
    height: int

    _grid: Grid
    _OFF = "."
    _ON = "█"

    def __init__(
        self, width: int = 50, height: int = 6, grid: Grid | None = None
    ) -> None:
        object.__setattr__(self, "width", width)
        object.__setattr__(self, "height", height)
        if grid is None:
            grid = [[self._OFF] * width for _ in range(height)]
        object.__setattr__(self, "_grid", grid)

    def _copy_grid(self) -> Grid:
        return deepcopy(self._grid)

    def turn_on(self, width: int, height: int) -> Screen:
        g = self._copy_grid()
        for row in g[:height]:
            row[:width] = [self._ON] * width
        return Screen(self.width, self.height, grid=g)

    @staticmethod
    def _rotate_list(row: Row, amount: int) -> Row:
        return row[-amount:] + row[:-amount]

    def rotate_row(self, row_index: int, amount: int) -> Screen:
        g = self._copy_grid()
        g[row_index] = self._rotate_list(g[row_index], amount)
        return Screen(self.width, self.height, grid=g)

    @staticmethod
    def _transpose(matrix: Grid) -> Grid:
        return list(map(list, zip(*matrix)))

    def rotate_column(self, column_index: int, amount: int) -> Screen:
        g = self._copy_grid()
        g = self._transpose(g)
        g[column_index] = self._rotate_list(g[column_index], amount)
        g = self._transpose(g)
        return Screen(self.width, self.height, grid=g)

    def process(self, instruction: Instruction) -> Screen:
        if isinstance(instruction, TurnOn):
            return self.turn_on(instruction.width, instruction.height)
        if isinstance(instruction, RotateRow):
            return self.rotate_row(instruction.index, instruction.amount)
        if isinstance(instruction, RotateColumn):
            return self.rotate_column(instruction.index, instruction.amount)
        raise ValueError("Unknown instruction.")

    @classmethod
    def process_all(cls, instructions: Iterable[Instruction]) -> Screen:
        return reduce(lambda s, i: s.process(i), instructions, cls())

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self._grid)

    @property
    def lit_pixels(self) -> int:
        return sum(row.count(self._ON) for row in self._grid)


def test_screen() -> None:
    screen = Screen(width=7, height=3)

    screen = screen.process(TurnOn(3, 2))
    assert (
        str(screen)
        == """\
███....
███....
......."""
    )

    screen = screen.process(RotateColumn(1, 1))
    assert (
        str(screen)
        == """\
█.█....
███....
.█....."""
    )

    screen = screen.process(RotateRow(0, 4))
    assert (
        str(screen)
        == """\
....█.█
███....
.█....."""
    )

    screen = screen.process(RotateColumn(1, 1))
    assert (
        str(screen)
        == """\
.█..█.█
█.█....
.█....."""
    )


if __name__ == "__main__":
    instructions = map(parse, load_puzzle_input(day=8).splitlines())
    final_screen = Screen.process_all(instructions)
    report_solution(
        puzzle_title="Day 8: Two-Factor Authentication",
        part_one_solution=final_screen.lit_pixels,
        part_two_solution="\n" + str(final_screen),
    )
