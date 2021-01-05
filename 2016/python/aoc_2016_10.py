from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import Callable, Iterable, NamedTuple, Optional, Tuple

import pytest
from lark import Lark, Transformer
from pyrsistent import m, v
from pyrsistent.typing import PMap, PVector

from aoc_common import load_puzzle_input, report_solution

grammar = """
?start: init | exchange

init: "value " INT " goes to " NAME
exchange: NAME " gives low to " NAME " and high to " NAME

NAME: ("bot"|"output") " " INT

%import common.INT
"""


@dataclass(frozen=True)
class Instruction:
    ...


@dataclass(frozen=True)
class Initialise(Instruction):
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

    def init(self, args: Tuple[int, str]) -> Initialise:
        return Initialise(value=args[0], receiver=args[1])

    def exchange(self, args: Tuple[str, str, str]) -> Exchange:
        return Exchange(source=args[0], gets_low=args[1], gets_high=args[2])


_parse = Lark(grammar).parse
_transform = _T().transform


def parse(line: str) -> Instruction:
    return _transform(_parse(line))


@pytest.mark.parametrize(
    "line,expected",
    [
        ("value 5 goes to bot 2", Initialise(5, "bot 2")),
        (
            "bot 2 gives low to bot 1 and high to bot 0",
            Exchange("bot 2", "bot 1", "bot 0"),
        ),
        ("value 3 goes to bot 1", Initialise(3, "bot 1")),
        (
            "bot 1 gives low to output 1 and high to bot 0",
            Exchange("bot 1", "output 1", "bot 0"),
        ),
        (
            "bot 0 gives low to output 2 and high to output 0",
            Exchange("bot 0", "output 2", "output 0"),
        ),
        ("value 2 goes to bot 2", Initialise(2, "bot 2")),
    ],
)
def test_parse(line: str, expected: Instruction) -> None:
    assert parse(line) == expected


class ExchangeResult(NamedTuple):
    giver: Bot
    receiver: Bot


Selector = Callable[[Iterable[int]], int]


@dataclass(frozen=True)
class Bot:
    name: str
    chips: PVector[int] = v()

    def receive(self, chip: int) -> Bot:
        return Bot(self.name, self.chips.append(chip))

    def _without_chip(self, chip: int) -> Bot:
        return Bot(self.name, self.chips.remove(chip))

    @staticmethod
    def _give(giver: Bot, receiver: Bot, selector: Selector) -> ExchangeResult:
        chip = selector(giver.chips)
        g = giver._without_chip(chip)
        r = receiver.receive(chip)
        return ExchangeResult(giver=g, receiver=r)

    def give_low(self, other: Bot) -> ExchangeResult:
        """Return the states of (self, other) after transferring the low-value chip."""
        return self._give(self, other, min)

    def give_high(self, other: Bot) -> ExchangeResult:
        """Return the states of (self, other) after transferring the high-value chip."""
        return self._give(self, other, max)


@dataclass(frozen=True)
class State:
    current: PMap[str, Bot] = m()
    giver_history: PVector[Bot] = v()
    failed_instructions: PVector[Instruction] = v()

    def _initialise(self, instruction: Initialise) -> State:
        name = instruction.receiver
        value = instruction.value

        bot = self.current.get(name, Bot(name))
        new_current = self.current.set(name, bot.receive(value))
        return State(new_current, self.giver_history, self.failed_instructions)

    def _exchange(self, instruction: Exchange) -> State:
        giver = self.current[instruction.source]

        low_name = instruction.gets_low
        high_name = instruction.gets_high

        low_receiver = self.current.get(low_name, Bot(low_name))
        high_receiver = self.current.get(high_name, Bot(high_name))

        new_history = self.giver_history.append(giver)

        giver, low_receiver = giver.give_low(low_receiver)
        giver, high_receiver = giver.give_high(high_receiver)
        changes = {a.name: a for a in [giver, low_receiver, high_receiver]}
        new_current = self.current.update(changes)

        return State(new_current, new_history, self.failed_instructions)

    def _with_failed_instruction(self, instruction: Instruction) -> State:
        return State(
            self.current,
            self.giver_history,
            self.failed_instructions.append(instruction),
        )

    def process(self, instruction: Instruction) -> State:
        if isinstance(instruction, Initialise):
            return self._initialise(instruction)
        if isinstance(instruction, Exchange):
            try:
                return self._exchange(instruction)
            except (KeyError, ValueError):
                return self._with_failed_instruction(instruction)
        raise ValueError(f"Unknown instruction {instruction}.")

    @classmethod
    def process_all(
        cls, instructions: Iterable[Instruction], state: Optional[State] = None
    ) -> State:
        if state is None:
            state = cls()

        final_state = reduce(lambda s, i: s.process(i), instructions, state)
        if final_state.failed_instructions:
            return cls.process_all(
                final_state.failed_instructions,
                cls(final_state.current, final_state.giver_history, v()),
            )
        else:
            return final_state

    def find_bot_that_handled_chip_values(self, v1: int, v2: int) -> Bot:
        try:
            return next(s for s in self.giver_history if set(s.chips) == {v1, v2})
        except StopIteration:
            raise ValueError(f"No bot in giving history with chips {v1} and {v2}.")


def test_state() -> None:
    instructions = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""
    parsed = [parse(line) for line in instructions.splitlines()]
    state = State.process_all(parsed)
    bot_with_chips_2_and_5 = state.find_bot_that_handled_chip_values(5, 2)
    assert bot_with_chips_2_and_5.name == "bot 2"


if __name__ == "__main__":
    instructions = [parse(line) for line in load_puzzle_input(day=10).splitlines()]
    final_state = State.process_all(instructions)

    bot_we_want = final_state.find_bot_that_handled_chip_values(61, 17)

    output_product = (
        final_state.current["output 0"].chips[0]
        * final_state.current["output 1"].chips[0]
        * final_state.current["output 2"].chips[0]
    )

    report_solution(
        puzzle_title="Day 10: Balance Bots",
        part_one_solution=bot_we_want.name,
        part_two_solution=output_product,
    )
