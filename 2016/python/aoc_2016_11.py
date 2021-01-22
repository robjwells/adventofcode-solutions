from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List, Tuple, cast

from lark import Lark, Transformer
from pyrsistent import pvector
from pyrsistent.typing import PVector

from aoc_common import load_puzzle_input

with open("aoc_2016_11.lark") as grammar_file:
    grammar = grammar_file.read()


class ItemKind(Enum):
    GENERATOR = auto()
    MICROCHIP = auto()

    def __repr__(self) -> str:
        return self.name.lower()  # pylint: disable=no-member


@dataclass(frozen=True)
class Item:
    element: str
    kind: ItemKind

    def __repr__(self) -> str:
        return f"<{self.element} {self.kind!r}>"


@dataclass(frozen=True)
class Floor:
    number: int
    items: PVector[Item]

    def __str__(self) -> str:
        return f"{self.number}: {list(self.items)}"


class _T(Transformer[Floor]):
    ELEMENT = str

    @staticmethod
    def nth(args: tuple[str]) -> int:
        idx = ["first", "second", "third", "fourth"].index(args[0])
        return idx

    @staticmethod
    def generator(args: tuple[str]) -> Item:
        return Item(args[0], kind=ItemKind.GENERATOR)

    @staticmethod
    def microchip(args: tuple[str]) -> Item:
        return Item(args[0], kind=ItemKind.MICROCHIP)

    @staticmethod
    def nothing(_args: list[str]) -> None:
        return None

    @staticmethod
    def floor(args: tuple[Any, ...]) -> Floor:
        if args[1] is None:
            args = (args[0],)
        floor = cast(int, args[0])
        items = cast(list[Item], args[1:])
        return Floor(floor, pvector(items))


_parse = Lark(grammar).parse
_transform = _T().transform


def parse(line: str) -> Floor:
    return _transform(_parse(line))


if __name__ == "__main__":
    lines = load_puzzle_input(day=11).splitlines()
    print(*[parse(line) for line in lines], sep="\n\n")
