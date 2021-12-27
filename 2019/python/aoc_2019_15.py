"""Day 15: Oxygen System"""
from __future__ import annotations

from collections import deque
from enum import Enum
from pathlib import Path
from typing import Deque, Dict, Iterator, List, Set, Tuple

import png
from PIL import Image

import aoc
from intcode import IntCode, parse_program

DAY = 15

VISUALISE = False

X_RANGE = range(-21, 20)
Y_RANGE = range(-19, 22)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

FRAME = 0

Position = Tuple[int, int]


class Tile(Enum):
    Wall = 0
    Blank = 1
    Target = 2
    Origin = -1
    Oxygen = -2


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

    def clone(self) -> Droid:
        return Droid(computer=self.computer.clone(), position=self.position)


def bfs_distance(
    maze: Dict[Position, Tile], target: Position, start: Position = (0, 0)
) -> int:
    deltas = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    queue: Deque[Tuple[int, Position]] = deque(
        (1, (start[0] + pos[0], start[1] + pos[1]))
        for pos in deltas
        if maze.get(pos, Tile.Wall) is not Tile.Wall
    )
    visited = {start}
    while queue:
        distance, position = queue.popleft()
        visited.add(position)
        if position == target:
            return distance
        x, y = position
        for dx, dy in deltas:
            new_pos = (x + dx, y + dy)
            if new_pos not in visited and maze.get(new_pos, Tile.Wall) is not Tile.Wall:
                queue.append((distance + 1, new_pos))
    return -1


def explore_maze(program: List[int]) -> Dict[Position, Tile]:
    visited: Dict[Position, Tile] = {}
    queue: Deque[Droid] = deque()

    origin = Droid(IntCode(program))
    queue.append(origin)
    visited[origin.position] = Tile.Origin

    while queue:
        buffer = []
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
                    buffer.append(new)
        queue.extend(buffer)
        if VISUALISE:
            render_maze_frame(visited)

    return visited


def oxygen_propagation_times(
    maze: Dict[Position, Tile], system_position: Position
) -> Iterator[int]:
    visited: Set[Position] = set()
    queue: Deque[Tuple[Position, int]] = deque()
    queue.append((system_position, 0))

    while queue:
        buffer = []
        while queue:
            current_position, current_distance = queue.pop()
            maze[current_position] = Tile.Oxygen
            visited.add(current_position)
            yield current_distance

            for direction in Direction:
                new_position = Direction.new_position(current_position, direction)
                if new_position not in visited and maze[new_position] is not Tile.Wall:
                    buffer.append((new_position, current_distance + 1))
        queue.extend(buffer)
        if VISUALISE:
            render_maze_frame(maze)


def main(program: List[int]) -> Tuple[int, int]:
    maze = explore_maze(program)
    system_position = next(p for p, t in maze.items() if t is Tile.Target)
    distance_to_system = bfs_distance(maze, target=system_position)

    oxygen_fill_time = max(oxygen_propagation_times(maze, system_position))

    return distance_to_system, oxygen_fill_time


def render_maze_frame(maze: Dict[Position, Tile]) -> None:
    global FRAME

    image = []
    writer = png.Writer(len(X_RANGE), len(Y_RANGE), greyscale=False)

    for y in Y_RANGE:
        row: List[int] = []
        for x in X_RANGE:
            tile = maze.get((x, y), Tile.Wall)
            if tile is Tile.Blank:
                row.extend(WHITE)
            elif tile is Tile.Wall:
                row.extend(BLACK)
            elif tile is Tile.Origin:
                row.extend(BLUE)
            elif tile is Tile.Target:
                row.extend(RED)
            elif tile is Tile.Oxygen:
                row.extend(GREEN)
            else:
                assert False, "Should be unreachable"
        image.append(row)

    subdir = Path("aoc_2019_15_maze")
    subdir.mkdir(exist_ok=True)
    filename = f"{subdir}/{FRAME:03}.png-s"
    FRAME += 1
    with open(filename, "wb") as png_file:
        writer.write(png_file, image)

    saved = Image.open(filename)
    resized = saved.resize((saved.size[0] * 12, saved.size[1] * 12))
    resized.save(filename[:-2])

    Path(filename).unlink()


if __name__ == "__main__":
    part_one_solution, part_two_solution = main(
        parse_program(aoc.load_puzzle_input(2019, DAY))
    )

    assert (
        part_one_solution == 244
    ), "Part one solution doesn't match known-correct answer."

    assert (
        part_two_solution == 278
    ), "Part one solution doesn't match known-correct answer."

    print(
        aoc.format_solution(
            title=__doc__,
            part_one=part_one_solution,
            part_two=part_two_solution,
        )
    )
