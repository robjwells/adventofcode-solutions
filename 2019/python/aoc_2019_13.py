"""Day 13: Care Package"""
from __future__ import annotations

from enum import Enum
from typing import Dict, List, Tuple

import aoc_common
from intcode import IntCode, parse_program

DAY = 13


class Tile(Enum):
    Empty = 0
    Wall = 1
    Block = 2
    HorizontalPaddle = 3
    Ball = 4


def render_screen(computer: IntCode) -> Dict[Tuple[int, int], Tile]:
    screen: Dict[Tuple[int, int], Tile] = {}
    while computer.has_output():
        x, y = computer.read_output(), computer.read_output()
        tile = Tile(computer.read_output())
        screen[(x, y)] = tile
    return screen


def main(program: List[int]) -> int:
    computer = IntCode(program)
    computer.run_until_halt()
    screen = render_screen(computer)
    num_blocks = len([pos for pos, tile in screen.items() if tile is Tile.Block])
    return num_blocks


if __name__ == "__main__":
    program = parse_program(aoc_common.load_puzzle_input(DAY))
    part_one_solution = main(program)

    assert (
        part_one_solution == 247
    ), "Part one solution doesn't match known-correct answer."

    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
