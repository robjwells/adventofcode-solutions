from __future__ import annotations
from copy import deepcopy
from collections import deque
from dataclasses import dataclass
from enum import Enum, auto

from util import read_input

from more_itertools import chunked


@dataclass(frozen=True)
class Step:
    move_quantity: int
    from_stack: int
    to_stack: int


class CraneType(Enum):
    SINGLE = auto()
    MULTIPLE = auto()


class Stacks:
    _stacks: dict[int, deque[str]]

    def __init__(self, stack_strings: dict[str, str]) -> None:
        self._stacks = {int(ns): deque(cs) for ns, cs in stack_strings.items()}

    def __len__(self) -> int:
        return len(self._stacks)

    @property
    def _indices(self) -> range:
        return range(1, len(self) + 1)

    def top_crates(self) -> list[str]:
        return [self._stacks[index][-1] for index in self._indices]

    def perform_step(self, step: Step, mode: CraneType) -> None:
        assert step.from_stack in self._indices
        assert step.to_stack in self._indices
        assert len(self._stacks[step.from_stack]) >= step.move_quantity

        if mode == CraneType.SINGLE:
            for _ in range(step.move_quantity):
                crate = self._stacks[step.from_stack].pop()
                self._stacks[step.to_stack].append(crate)
        elif mode == CraneType.MULTIPLE:
            buffer = deque()
            for _ in range(step.move_quantity):
                crate = self._stacks[step.from_stack].pop()
                buffer.append(crate)
            while buffer:
                self._stacks[step.to_stack].append(buffer.pop())
        else:
            raise ValueError(f"Unknown CraneType: {mode!r}")


def parse(s: str) -> tuple[list[Step], Stacks]:
    stack_section, move_section = s.split("\n\n", 1)

    steps = []
    for line in move_section.splitlines():
        n, f, t = [int(part) for part in line.split() if part.isdigit()]
        steps.append(
            Step(
                move_quantity=n,
                from_stack=f,
                to_stack=t,
            )
        )

    bottom_up = reversed(stack_section.splitlines())
    split = []
    for line in bottom_up:
        chunks = ["".join(chunk) for chunk in chunked(line, 4, strict=False)]
        parts = ["".join(c for c in chunk if c.isalnum()) for chunk in chunks]
        split.append(parts)

    indexes, *crate_lines = split
    stack_strings = {n: "" for n in indexes}
    for line in crate_lines:
        for index, crate in zip(indexes, line):
            if crate:
                stack_strings[index] += crate

    stacks = Stacks(stack_strings)

    return (steps, stacks)


def solve(steps: list[Step], stacks: Stacks, mode: CraneType) -> str:
    for step in steps:
        stacks.perform_step(step, mode)
    return "".join(stacks.top_crates())


def main() -> None:
    puzzle_text = read_input(5)
    steps, initial_stacks = parse(puzzle_text)

    part_one = solve(steps, deepcopy(initial_stacks), CraneType.SINGLE)
    assert part_one == "BSDMQFLSP"
    print(f"Part one: {part_one}")

    part_two = solve(steps, deepcopy(initial_stacks), CraneType.MULTIPLE)
    assert part_two == "PGSQBFLDP"
    print(f"Part two: {part_two}")


if __name__ == "__main__":
    main()


SAMPLE_INPUT = """\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def test_parse() -> None:
    steps, stacks = parse(SAMPLE_INPUT)
    assert len(steps) == 4
    assert steps[0].move_quantity == 1
    assert steps[1].to_stack == 3
    assert steps[2].from_stack == 2

    assert len(stacks) == 3
    assert stacks.top_crates() == ["N", "D", "P"]


def test_sample_input_part_one() -> None:
    assert solve(*parse(SAMPLE_INPUT), CraneType.SINGLE) == "CMZ"


def test_sample_input_part_two() -> None:
    assert solve(*parse(SAMPLE_INPUT), CraneType.MULTIPLE) == "MCD"
