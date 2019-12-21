"""Day 15: Oxygen System"""
from __future__ import annotations

from collections import deque
from enum import Enum
# from pathlib import Path
from typing import Deque, Dict, List, Tuple

import aoc_common
from intcode import IntCode, parse_program

# import png
# from PIL import Image


DAY = 15

# X_RANGE = range(-21, 20)
# Y_RANGE = range(-19, 22)

# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# BLUE = (0, 0, 255)
# RED = (255, 0, 0)

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


def bfs_distance(maze: Dict[Position, Tile], start: Position = (0, 0)) -> int:
    queue = deque()
    deltas = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    queue.extend(
        [
            (1, pos)
            for pos in deltas
            if maze.get(pos, Tile.Wall) in (Tile.Blank, Tile.Target)
        ]
    )
    visited = {(0, 0)}
    while queue:
        distance, position = queue.popleft()
        visited.add(position)
        if maze[position] is Tile.Target:
            return distance
        x, y = position
        for dx, dy in deltas:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited and maze.get((nx, ny), Tile.Wall) in (
                Tile.Blank,
                Tile.Target,
            ):
                queue.append((distance + 1, (nx, ny)))
    return -1


def explore_maze(program: List[int]) -> Dict[Position, Tile]:
    visited: Dict[Position, Tile] = {}
    queue: Deque[Droid] = deque()

    origin = Droid(IntCode(program))
    queue.append(origin)
    visited[origin.position] = Tile.Origin

    # step = 0
    while queue:
        # step += 1
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
                queue.appendleft(new)
        # render_maze_frame(visited, step)

    return visited


def main(program: List[int]) -> int:
    maze = explore_maze(program)
    distance_to_system = bfs_distance(maze)

    return distance_to_system


# def render_maze_frame(maze: Dict[Position, Tile], suffix: int) -> None:
#     image = []
#     writer = png.Writer(len(X_RANGE), len(Y_RANGE), greyscale=False)

#     for y in Y_RANGE:
#         row = []
#         for x in X_RANGE:
#             tile = maze.get((x, y), Tile.Wall)
#             if tile is Tile.Blank:
#                 row.extend(WHITE)
#             elif tile is Tile.Wall:
#                 row.extend(BLACK)
#             elif tile is Tile.Origin:
#                 row.extend(BLUE)
#             elif tile is Tile.Target:
#                 row.extend(RED)
#             else:
#                 assert False, "Should be unreachable"
#         image.append(row)

#     subdir = Path("aoc_2019_15_maze")
#     subdir.mkdir(exist_ok=True)
#     filename = f"{subdir}/{suffix:03}.png-s"
#     with open(filename, "wb") as png_file:
#         writer.write(png_file, image)

#     saved = Image.open(filename)
#     resized = saved.resize((saved.size[0] * 12, saved.size[1] * 12))
#     resized.save(filename[:-2])

#     Path(filename).unlink()


if __name__ == "__main__":
    part_one_solution = main(parse_program(aoc_common.load_puzzle_input(DAY)))

    assert (
        part_one_solution == 244
    ), "Part one solution doesn't match known-correct answer."

    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
