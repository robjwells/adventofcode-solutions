"""Day 11: Space Police"""
from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import DefaultDict, List, NamedTuple, Tuple

import aoc_common
from intcode import HaltExecution, IntCode, parse_program

DAY = 11


class Point(NamedTuple):
    x: int
    y: int

    @classmethod
    def origin(cls) -> Point:
        return cls(0, 0)


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


def create_black_grid() -> Grid:
    return defaultdict(lambda: Colour.BLACK)


def create_black_grid_with_one_white_panel() -> Grid:
    grid = create_black_grid()
    grid[Point.origin()] = Colour.WHITE
    return grid


class HullPaintingRobot:
    position: Point = Point.origin()
    direction: Direction
    grid: Grid
    computer: IntCode

    def __init__(
        self, grid: Grid, computer: IntCode, direction: Direction = Direction.UP
    ):
        self.direction = direction
        self.grid = grid
        self.computer = computer

    def step(self) -> None:
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

    def run_until_halt(self) -> None:
        try:
            while True:
                self.step()
        except HaltExecution:
            pass

    @staticmethod
    def move(position: Point, direction: Direction) -> Point:
        return Point(position.x + direction.value.x, position.y + direction.value.y)


def paint_hull(program: List[int], grid: Grid) -> Grid:
    robot = HullPaintingRobot(grid=grid, computer=IntCode(program))
    robot.run_until_halt()
    return robot.grid


def visualise_painted_hull(grid: Grid) -> str:
    white_panels = [point for point, colour in grid.items() if colour is Colour.WHITE]
    white_panels = sorted(white_panels, key=lambda p: (-p.x, p.y))
    min_x, max_x = white_panels[-1].x, white_panels[0].x
    min_y = min(p.y for p in white_panels)
    max_y = max(p.y for p in white_panels)

    hull = []
    for y in range(max_y, min_y - 1, -1):
        line = ""
        for x in range(min_x, max_x + 1):
            if grid[Point(x, y)] is Colour.WHITE:
                line += "█"
            else:
                line += " "
        hull.append(line.rstrip() + "\n")
    hull_string = "".join(hull)
    return hull_string


def main(program: List[int]) -> Tuple[int, str]:
    part_one_grid = paint_hull(program, create_black_grid())
    unique_panels_painted = len(part_one_grid)

    part_two_grid = paint_hull(program, create_black_grid_with_one_white_panel())
    registration_id = visualise_painted_hull(part_two_grid)

    return unique_panels_painted, registration_id


if __name__ == "__main__":
    program = parse_program(aoc_common.load_puzzle_input(DAY))
    part_one_solution, part_two_solution = main(program)

    assert (
        part_one_solution == 1967
    ), "Part one solution doesn't match known-correct answer."

    part_two_expected = """\
█  █ ███  █  █ ████  ██  ████ ███  █  █
█ █  █  █ █  █ █    █  █    █ █  █ █ █
██   ███  █  █ ███  █      █  ███  ██
█ █  █  █ █  █ █    █ ██  █   █  █ █ █
█ █  █  █ █  █ █    █  █ █    █  █ █ █
█  █ ███   ██  ████  ███ ████ ███  █  █
"""
    assert (
        part_two_solution == part_two_expected
    ), "Part two solution doesn't match known-correct answer."

    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        # Append newlines to clear "Part two solution:" line
        part_two_solution="\n\n" + part_two_solution,
    )
