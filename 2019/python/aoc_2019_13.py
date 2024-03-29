"""Day 13: Care Package"""
from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Tuple

import aoc
from intcode import HaltExecution, IntCode, parse_program

DAY = 13


class Tile(Enum):
    Empty = 0
    Wall = 1
    Block = 2
    Paddle = 3
    Ball = 4


class JoystickPosition(Enum):
    Neutral = 0
    Left = -1
    Right = 1


State = Dict[Tuple[int, int], Tile]


class ArcadeCabinet:
    state: State = {}
    score: int = 0
    computer: IntCode
    playable: bool = False
    paddle_position: Optional[Tuple[int, int]] = None
    ball_position: Optional[Tuple[int, int]] = None

    def __init__(self, program: List[int], enable_play: bool = False):
        program = program[:]
        if enable_play:
            program[0] = 2
            self.playable = True
        self.computer = IntCode(program)

    def play_until_game_over(self) -> None:
        try:
            while True:
                if self.playable:
                    self.computer.input_queue.clear()  # Ensure input doesn't build up
                    self.computer.pass_input(self.bot_move(self.state).value)
                self.computer.step()
                self.update_state()
        except HaltExecution:
            pass

    def update_state(self) -> None:
        while len(self.computer.output_queue) >= 3:
            pos = self.computer.read_output(), self.computer.read_output()
            if pos == (-1, 0):
                self.score = self.computer.read_output()
            else:
                tile = Tile(self.computer.read_output())
                if tile is Tile.Paddle:
                    self.paddle_position = pos
                elif tile is Tile.Ball:
                    self.ball_position = pos
                self.state[pos] = tile

    def bot_move(self, state: State) -> JoystickPosition:
        if self.ball_position is None or self.paddle_position is None:
            return JoystickPosition.Neutral

        if self.ball_position[0] < self.paddle_position[0]:
            return JoystickPosition.Left
        elif self.ball_position[0] > self.paddle_position[0]:
            return JoystickPosition.Right
        else:
            return JoystickPosition.Neutral


def main(program: List[int]) -> Tuple[int, int]:
    cabinet = ArcadeCabinet(program)
    cabinet.play_until_game_over()
    num_blocks = len([pos for pos, tile in cabinet.state.items() if tile is Tile.Block])

    cabinet = ArcadeCabinet(program, enable_play=True)
    cabinet.play_until_game_over()
    score = cabinet.score

    return num_blocks, score


if __name__ == "__main__":
    program = parse_program(aoc.load_puzzle_input(2019, DAY))
    part_one_solution, part_two_solution = main(program)

    assert (
        part_one_solution == 247
    ), "Part one solution doesn't match known-correct answer."

    assert (
        part_two_solution == 12954
    ), "Part two solution doesn't match known-correct answer."

    print(
        aoc.format_solution(
            title=__doc__,
            part_one=part_one_solution,
            part_two=part_two_solution,
        )
    )
