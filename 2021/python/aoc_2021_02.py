"""--- Day 2: Dive! ---"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Literal, TypeGuard, TypeAlias, NoReturn


def assert_never(value: NoReturn) -> NoReturn:
    assert False, f"Unhandled value: {value} ({type(value).__name__})"


Direction: TypeAlias = Literal["up", "down", "forward"]


@dataclass(frozen=True)
class Command:
    direction: Direction
    amount: int

    @staticmethod
    def _validate_direction(command: str) -> TypeGuard[Direction]:
        return command in ["up", "down", "forward"]

    @classmethod
    def from_line(cls, line: str) -> Command:
        direction, amount_string = line.split(" ", maxsplit=1)
        amount = int(amount_string)
        assert cls._validate_direction(direction)
        return cls(direction, amount)


@dataclass(frozen=True)
class Position:
    horizontal: int = 0
    depth: int = 0

    def move_by(self, command: Command) -> Position:
        direction = command.direction
        amount = command.amount

        if direction == "forward":
            return replace(self, horizontal=self.horizontal + amount)
        if direction == "up":
            return replace(self, depth=self.depth - amount)
        if direction == "down":
            return replace(self, depth=self.depth + amount)
        assert_never(direction)


@dataclass(frozen=True)
class AimedPosition(Position):
    aim: int = 0

    def move_by(self, command: Command) -> AimedPosition:
        direction = command.direction
        amount = command.amount

        if direction == "forward":
            return replace(
                self,
                horizontal=self.horizontal + amount,
                depth=self.depth + (self.aim * amount),
            )
        if direction == "up":
            return replace(self, aim=self.aim - amount)
        if direction == "down":
            return replace(self, aim=self.aim + amount)
        assert_never(direction)


def find_final_position(start: Position, commands: list[Command]) -> Position:
    current = start
    for command in commands:
        current = current.move_by(command)
    return current


def main(puzzle_input_text: str) -> tuple[int, int]:
    commands = [Command.from_line(line) for line in puzzle_input_text.splitlines()]

    p1_position = find_final_position(Position(), commands)
    p1_result = p1_position.horizontal * p1_position.depth

    p2_position = find_final_position(AimedPosition(), commands)
    p2_result = p2_position.horizontal * p2_position.depth

    return p1_result, p2_result


if __name__ == "__main__":
    puzzle_input_file = Path(__file__).parent.parent.joinpath("input", "2021-02.txt")
    results = main(puzzle_input_file.read_text())
    print(results)
