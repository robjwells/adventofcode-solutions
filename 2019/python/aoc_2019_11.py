"""Day 11: Space Police"""
from __future__ import annotations
from enum import Enum
from typing import DefaultDict, List, Tuple, NamedTuple
from collections import defaultdict
from itertools import groupby

import aoc_common
from intcode import IntCode, parse_program, HaltExecution

DAY = 11


class Point(NamedTuple):
    x: int
    y: int


class Colour(Enum):
    BLACK = 0
    WHITE = 1


class Turn(Enum):
    LEFT = 0
    RIGHT = 1


class Direction(Enum):
    UP = Point(0, 1)
    DOWN = Point(0, -1)
    LEFT = Point(-1, 0)
    RIGHT = Point(1, 0)

    def turn(self, turn_direction: Turn) -> Direction:
        turns = {
            (Turn.LEFT, Direction.UP): Direction.LEFT,
            (Turn.LEFT, Direction.LEFT): Direction.DOWN,
            (Turn.LEFT, Direction.DOWN): Direction.RIGHT,
            (Turn.LEFT, Direction.RIGHT): Direction.UP,
            (Turn.RIGHT, Direction.UP): Direction.RIGHT,
            (Turn.RIGHT, Direction.LEFT): Direction.UP,
            (Turn.RIGHT, Direction.DOWN): Direction.LEFT,
            (Turn.RIGHT, Direction.RIGHT): Direction.DOWN,
        }
        return turns[turn_direction, self]


Grid = DefaultDict[Point, Colour]


def new_grid(default_colour: Colour = Colour.BLACK) -> Grid:
    return defaultdict(lambda: default_colour)


def new_grid_with_white_starting_square() -> Grid:
    grid = new_grid()
    grid[Point(0, 0)] = Colour.WHITE
    return grid


class HullPaintingRobot:
    position: Point = Point(0, 0)
    direction = Direction
    grid: Grid
    computer: IntCode

    def __init__(
        self, grid: Grid, computer: IntCode, direction: Direction = Direction.UP
    ):
        self.direction = direction
        self.grid = grid
        self.computer = computer

    def step(self):
        if self.computer.has_halted():
            return

        # Pass colour of current position as integer
        self.computer.pass_input(self.grid[self.position].value)
        while len(self.computer.output_queue) < 2:
            self.computer.step()

        colour = Colour(self.computer.read_output())
        self.grid[self.position] = colour

        turn = Turn(self.computer.read_output())
        self.direction = self.direction.turn(turn)
        self.position = self.move(self.position, self.direction)

    def run_until_halt(self):
        try:
            while True:
                self.step()
        except HaltExecution:
            pass

    @staticmethod
    def move(position: Point, direction: Direction):
        return Point(position.x + direction.value.x, position.y + direction.value.y)


def main(program):
    robot = HullPaintingRobot(grid=new_grid(), computer=IntCode(program))
    robot.run_until_halt()
    print(len(robot.grid))  # 1967

    second_robot = HullPaintingRobot(
        grid=new_grid_with_white_starting_square(), computer=IntCode(program)
    )
    second_robot.run_until_halt()
    grid = second_robot.grid
    white_panels = [point for point, colour in grid.items() if colour is Colour.WHITE]
    white_panels = sorted(white_panels, key=lambda p: (-p.x, p.y))
    min_x, max_x = white_panels[-1].x, white_panels[0].x
    min_y = min(p.y for p in white_panels)
    max_y = max(p.y for p in white_panels)

    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            if grid[Point(x, y)] is Colour.WHITE:
                print("█", end="")
            else:
                print(" ", end="")
        print()
    # KBUEGZBK


if __name__ == "__main__":
    program = parse_program(aoc_common.load_puzzle_input(DAY))
    main(program)
