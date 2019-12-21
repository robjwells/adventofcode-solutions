"""Day 15: Oxygen System"""
from __future__ import annotations

from collections import deque
from enum import Enum
from typing import Deque, Dict, List, Tuple

import aoc_common
from intcode import IntCode, parse_program

DAY = 15

Position = Tuple[int, int]


class Tile(Enum):
    Wall = 0
    Blank = 1
    Target = 2
    Origin = -1


class MoveResult(Enum):
    HitWall = 0
    Moved = 1
    FoundTarget = 2


class Direction(Enum):
    North = 1
    South = 2
    West = 3
    East = 4

    @staticmethod
    def new_position(position: Position, direction: Direction) -> Position:
        x, y = position
        if direction is Direction.North:
            new_pos = (x, y + 1)
        elif direction is Direction.South:
            new_pos = (x, y - 1)
        elif direction is Direction.West:
            new_pos = (x - 1, y)
        elif direction is Direction.East:
            new_pos = (x + 1, y)
        return new_pos


class Droid:
    computer: IntCode
    position: Position

    def __init__(self, computer: IntCode, position: Position = (0, 0)):
        self.computer = computer
        self.position = position

    def move(self, direction: Direction) -> MoveResult:
        self.computer.pass_input(direction.value)
        self.position = Direction.new_position(self.position, direction)
        while not self.computer.has_output():
            self.computer.step()
        return MoveResult(self.computer.read_output())

    def clone(self):
        return Droid(computer=self.computer.clone(), position=self.position)


def main(program: List[int]) -> None:
    visited: Dict[Position, Tile] = {}
    queue: Deque[Droid] = deque()

    origin = Droid(IntCode(program))
    queue.append(origin)
    visited[origin.position] = Tile.Origin

    while queue:
        current = queue.pop()
        for direction in Direction:
            new = current.clone()
            result = new.move(direction)
            if new.position in visited:
                continue
            if result is MoveResult.Moved:
                visited[new.position] = Tile.Blank
            elif result is MoveResult.HitWall:
                visited[new.position] = Tile.Wall
            elif result is MoveResult.FoundTarget:
                visited[new.position] = Tile.Target

            if result in (MoveResult.Moved, MoveResult.FoundTarget):
                queue.append(new)


if __name__ == "__main__":
    main(parse_program(aoc_common.load_puzzle_input(DAY)))
