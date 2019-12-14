"""Day 13: Care Package"""
from __future__ import annotations

from enum import Enum
from typing import Dict, List, Tuple

import aoc_common
from intcode import HaltExecution, IntCode, parse_program

DAY = 13


class Tile(Enum):
    Empty = 0
    Wall = 1
    Block = 2
    HorizontalPaddle = 3
    Ball = 4


class JoystickPosition(Enum):
    Neutral = 0
    Left = -1
    Right = 1


class ArcadeCabinet:
    screen: Dict[Tuple[int, int], Tile] = {}
    computer: IntCode

    def __init__(self, program: List[int], play_for_free: bool = False):
        program = program[:]
        if play_for_free:
            program[0] = 2
        self.computer = IntCode(program)

    def play_until_game_over(self) -> None:
        try:
            while True:
                self.computer.step()
                self.render_screen()
        except HaltExecution:
            pass

    def render_screen(self) -> None:
        while len(self.computer.output_queue) >= 3:
            x, y = self.computer.read_output(), self.computer.read_output()
            tile = Tile(self.computer.read_output())
            self.screen[(x, y)] = tile


def main(program: List[int]) -> int:
    cabinet = ArcadeCabinet(program)
    cabinet.play_until_game_over()
    num_blocks = len(
        [pos for pos, tile in cabinet.screen.items() if tile is Tile.Block]
    )

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
