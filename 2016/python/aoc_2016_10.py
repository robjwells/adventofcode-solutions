from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import pytest
from lark import Lark, Transformer

from aoc_common import load_puzzle_input, report_solution

grammar = """
?start: init | exchange

init: "value " INT " goes to " NAME
exchange: NAME " gives low to " NAME " and high to " NAME

NAME: ("bot"|"output") " " INT

%import common.INT
%ignore " "
"""


@dataclass(frozen=True)
class Instruction:
    ...


@dataclass(frozen=True)
class Init(Instruction):
    value: int
    receiver: str


@dataclass(frozen=True)
class Exchange(Instruction):
    source: str
    gets_low: str
    gets_high: str


class _T(Transformer[Instruction]):
    INT = int
    NAME = str

    def init(self, args: Tuple[int, str]) -> Init:
        return Init(value=args[0], receiver=args[1])

    def exchange(self, args: Tuple[str, str, str]) -> Exchange:
        return Exchange(source=args[0], gets_low=args[1], gets_high=args[2])


_parse = Lark(grammar, parser="lalr").parse
_transform = _T().transform


def parse(line: str) -> Instruction:
    return _transform(_parse(line))


@pytest.mark.parametrize(
    "line,expected",
    [
        ("value 5 goes to bot 2", Init(5, "bot 2")),
        (
            "bot 2 gives low to bot 1 and high to bot 0",
            Exchange("bot 2", "bot 1", "bot 0"),
        ),
        ("value 3 goes to bot 1", Init(3, "bot 1")),
        (
            "bot 1 gives low to output 1 and high to bot 0",
            Exchange("bot 1", "output 1", "bot 0"),
        ),
        (
            "bot 0 gives low to output 2 and high to output 0",
            Exchange("bot 0", "output 2", "output 0"),
        ),
        ("value 2 goes to bot 2", Init(2, "bot 2")),
    ],
)
def test_parse(line: str, expected: Instruction) -> None:
    assert parse(line) == expected


if __name__ == "__main__":
    instructions = map(parse, load_puzzle_input(day=10).splitlines())
    for i in instructions:
        if isinstance(i, Init):
            print(i)
