from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from itertools import accumulate, chain
from typing import Iterable

from aoc_common import load_puzzle_input, report_solution


@dataclass
class Point:
    x: int = 0
    y: int = 0

    @property
    def manhattan_distance_from_origin(self) -> int:
        return abs(self.x) + abs(self.y)

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __mul__(self, steps: int) -> Point:
        return Point(self.x * steps, self.y * steps)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"

    def __hash__(self) -> int:
        return (self.x, self.y).__hash__()


class Instruction(Enum):
    TURN_LEFT = auto()
    TURN_RIGHT = auto()
    STEP_FORWARD = auto()

    @classmethod
    def parse(cls, s: str) -> Iterable[Instruction]:
        if s[0] == "L":
            yield cls.TURN_LEFT
        elif s[0] == "R":
            yield cls.TURN_RIGHT
        else:
            raise ValueError("Invalue turn direction, must be L or R.")

        for _ in range(int(s[1:])):
            yield cls.STEP_FORWARD


class Direction(Enum):
    NORTH = Point(0, 1)
    EAST = Point(1, 0)
    SOUTH = Point(0, -1)
    WEST = Point(-1, 0)

    def turn(self, turn: Instruction) -> Direction:
        if turn is Instruction.STEP_FORWARD:
            raise ValueError("'turn' must be TURN_LEFT or TURN_RIGHT.")

        cw = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        acw = cw[::-1]

        if turn is Instruction.TURN_LEFT:
            return dict(zip(acw, acw[1:] + [acw[0]]))[self]
        if turn is Instruction.TURN_RIGHT:
            return dict(zip(cw, cw[1:] + [cw[0]]))[self]

        raise Exception("Unreachable.")


@dataclass
class State:
    position: Point = Point()
    heading: Direction = Direction.NORTH
    last_action: Instruction | None = None

    def perform_instruction(self, instruction: Instruction) -> State:
        if instruction is Instruction.STEP_FORWARD:
            position = self.position + self.heading.value
            heading = self.heading
        else:
            position = self.position
            heading = self.heading.turn(instruction)

        return State(position, heading, instruction)


def parse_instructions(strings: list[str]) -> list[Instruction]:
    return list(chain.from_iterable(Instruction.parse(s) for s in strings))


def follow_all_instructions(instructions: list[Instruction]) -> Iterable[Point]:
    return (
        state.position
        for state in accumulate(
            instructions, lambda state, i: state.perform_instruction(i), initial=State()
        )
        if state.last_action is Instruction.STEP_FORWARD
    )


def find_first_repeat_location(
    all_positions: Iterable[Point], seen: frozenset[Point] = frozenset()
) -> Point:
    if not all_positions:
        raise ValueError("No repeated position found.")

    first, *rest = all_positions
    return first if first in seen else find_first_repeat_location(rest, seen | {first})


if __name__ == "__main__":
    instructions = parse_instructions(load_puzzle_input(1).split(", "))
    all_positions = list(follow_all_instructions(instructions))
    end_position = all_positions[-1]
    first_repeat = find_first_repeat_location(all_positions)
    report_solution(
        puzzle_title="Day 1: No Time for a Taxicab",
        part_one_solution=end_position.manhattan_distance_from_origin,
        part_two_solution=first_repeat.manhattan_distance_from_origin,
    )
