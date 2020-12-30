from __future__ import annotations

from aoc_common import load_puzzle_input, report_solution
from dataclasses import dataclass
from enum import auto, Enum
from functools import reduce
from typing import Iterator, List, Optional, Set, Tuple

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


class Direction(Enum):
    NORTH = Point(0, 1)
    EAST = Point(1, 0)
    SOUTH = Point(0, -1)
    WEST = Point(-1, 0)

    def turn(self, turn: Turn) -> Direction:
        if turn is Turn.LEFT:
            if self is self.NORTH:
                return self.WEST
            if self is self.WEST:
                return self.SOUTH
            if self is self.SOUTH:
                return self.EAST
            if self is self.EAST:
                return self.NORTH
        if turn is Turn.RIGHT:
            if self is self.NORTH:
                return self.EAST
            if self is self.EAST:
                return self.SOUTH
            if self is self.SOUTH:
                return self.WEST
            if self is self.WEST:
                return self.NORTH
        raise Exception("Unreachable.")


class Turn(Enum):
    LEFT = auto()
    RIGHT = auto()

    @classmethod
    def parse(cls, s: str) -> Turn:
        if s == "L":
            return cls.LEFT
        if s == "R":
            return cls.RIGHT
        raise ValueError("Invalue turn direction, must be L or R.")


@dataclass
class Instruction:
    turn: Turn
    steps: int

    def __iter__(self):
        yield from (self.turn, self.steps)


@dataclass
class State:
    position: Point = Point()
    heading: Direction = Direction.NORTH

    def move(self, instruction: Instruction) -> State:
        new_heading = self.heading.turn(instruction.turn)
        delta: Point = new_heading.value * instruction.steps
        new_position = self.position + delta
        return State(position=new_position, heading=new_heading)


class EarlyHaltingState:
    position: Point = Point()
    heading: Direction = Direction.NORTH
    visited: Set[Point] = set()

    def move(self, instruction: Instruction) -> Tuple[Optional[EarlyHaltingState], Optional[Point]]:
        self.heading = self.heading.turn(instruction.turn)
        for _ in range(instruction.steps):
            self.position = self.position + self.heading.value
            if self.position in self.visited:
                return (None, self.position)
            self.visited.add(self.position)
        return (self, None)


def parse_instructions(strings: List[str]) -> List[Instruction]:
    return [
        Instruction(Turn.parse(string[0]), int(string[1:]))
        for string in strings
    ]


def follow_all_instructions(instructions: List[Instruction]) -> Point:
    return reduce(
        lambda state, i: state.move(i),
        instructions,
        State()
    ).position


def find_first_repeat_location(instructions: List[Instruction]) -> Point:
    state = EarlyHaltingState()
    for i in instructions:
        state, repeat_location = state.move(i)
        if repeat_location is not None:
            return repeat_location
    raise Exception("Unreachable.")


if __name__ == "__main__":
    instructions = parse_instructions(load_puzzle_input(1).split(", "))
    end_position = follow_all_instructions(instructions)
    first_repeat = find_first_repeat_location(instructions)
    report_solution(
        puzzle_title="Day 1: No Time for a Taxicab",
        part_one_solution=end_position.manhattan_distance_from_origin,
        part_two_solution=first_repeat.manhattan_distance_from_origin
    )
