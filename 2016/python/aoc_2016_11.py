from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Iterable, NamedTuple, cast

from lark import Lark, Transformer
from more_itertools import chunked
from pyrsistent import pvector, v
from pyrsistent.typing import PVector

import pytest

from aoc_common import load_puzzle_input


class ItemKind(Enum):
    GENERATOR = auto()
    MICROCHIP = auto()

    def __repr__(self) -> str:
        return self.name.lower()  # pylint: disable=no-member

    def __lt__(self, other: ItemKind) -> bool:
        return self is ItemKind.GENERATOR


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
        return f"Floor {self.number}: {list(self.items)}"

    @property
    def is_valid(self) -> bool:
        """True when there are no generators or each chip has its generator."""
        gen_elements = {i.element for i in self.items if i.kind is ItemKind.GENERATOR}
        chip_elements = {i.element for i in self.items if i.kind is ItemKind.MICROCHIP}
        return not gen_elements or chip_elements <= gen_elements


@pytest.mark.parametrize(
    "floor,expected",
    [
        # Empty floor is valid.
        (Floor(0, v()), True),
        # Floors with only one item are valid.
        (Floor(0, v(Item(element="a", kind=ItemKind.GENERATOR))), True),
        (Floor(0, v(Item(element="a", kind=ItemKind.MICROCHIP))), True),
        # A floor with a matching pair is valid.
        (
            Floor(
                0,
                v(
                    Item(element="a", kind=ItemKind.GENERATOR),
                    Item(element="a", kind=ItemKind.MICROCHIP),
                ),
            ),
            True,
        ),
        # A floor with a differing pair is invalid.
        (
            Floor(
                0,
                v(
                    Item(element="a", kind=ItemKind.GENERATOR),
                    Item(element="b", kind=ItemKind.MICROCHIP),
                ),
            ),
            False,
        ),
        # A floor with a matched pair is valid even
        # if there are other generators present.
        (
            Floor(
                0,
                v(
                    Item(element="a", kind=ItemKind.GENERATOR),
                    Item(element="b", kind=ItemKind.GENERATOR),
                    Item(element="b", kind=ItemKind.MICROCHIP),
                ),
            ),
            True,
        ),
        # A floor with an unmatched chip is invalid if there
        # are (matched or unmatched) generators present.
        (
            Floor(
                0,
                v(
                    Item(element="a", kind=ItemKind.GENERATOR),
                    Item(element="a", kind=ItemKind.MICROCHIP),
                    Item(element="b", kind=ItemKind.MICROCHIP),
                ),
            ),
            False,
        ),
        (
            Floor(
                0,
                v(
                    Item(element="a", kind=ItemKind.GENERATOR),
                    Item(element="b", kind=ItemKind.MICROCHIP),
                    Item(element="c", kind=ItemKind.MICROCHIP),
                ),
            ),
            False,
        ),
        # Floors with only one kind of item are valid.
        (
            Floor(
                0,
                v(
                    Item(element="a", kind=ItemKind.MICROCHIP),
                    Item(element="b", kind=ItemKind.MICROCHIP),
                    Item(element="c", kind=ItemKind.MICROCHIP),
                ),
            ),
            True,
        ),
        (
            Floor(
                0,
                v(
                    Item(element="a", kind=ItemKind.GENERATOR),
                    Item(element="b", kind=ItemKind.GENERATOR),
                    Item(element="c", kind=ItemKind.GENERATOR),
                ),
            ),
            True,
        ),
    ],
)
def test_floor_validity(floor: Floor, expected: bool) -> None:
    assert floor.is_valid == expected


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


with open("aoc_2016_11.lark") as grammar_file:
    grammar = grammar_file.read()

_parse = Lark(grammar).parse
_transform = _T().transform


def parse(line: str) -> Floor:
    return _transform(_parse(line))


class LocationPair(NamedTuple):
    generator: int
    microchip: int


@dataclass(frozen=True)
class MinimumState:
    elevator_floor: int
    pairs: PVector[LocationPair]

    @classmethod
    def from_iterable(
        cls, elevator_floor: int, iterable: Iterable[LocationPair]
    ) -> MinimumState:
        return cls(elevator_floor, pvector(sorted(iterable)))


@dataclass(frozen=True)
class State:
    elevator_floor: int
    floors: PVector[Floor]

    def _group(self) -> Iterable[LocationPair]:
        nested = [
            [(floor.number, item) for item in floor.items] for floor in self.floors
        ]
        flat = [pair for floor in nested for pair in floor]
        s = sorted(flat, key=lambda pair: (pair[1].element, pair[1].kind))
        for generator, chip in chunked(s, 2):
            gen_floor, _ = generator
            chip_floor, _ = chip
            yield LocationPair(gen_floor, chip_floor)

    @property
    def is_valid(self) -> bool:
        ...

    def to_minimum_state(self) -> MinimumState:
        return MinimumState.from_iterable(self.elevator_floor, self._group())


if __name__ == "__main__":
    lines = load_puzzle_input(day=11).splitlines()
    s = State(0, pvector([parse(line) for line in lines]))
    s1 = State(0, pvector([parse(line) for line in lines]))
    s2 = State(1, pvector([parse(line) for line in lines]))
    seen = {s.to_minimum_state()}
    print(seen)
    seen.add(s1.to_minimum_state())
    print(seen)
    seen.add(s2.to_minimum_state())
    print(seen)
