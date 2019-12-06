"""Day 5: Sunny with a Chance of Asteroids"""
from typing import List

import aoc_common
from intcode import IntCode

DAY = 5


def parse_input(puzzle_input: str) -> List[int]:
    return [int(x) for x in puzzle_input.split(",")]


def main(program: List[int]) -> None:
    computer = IntCode(program)

    # Part one: provide 1 as input
    computer.input_queue.append(1)
    computer.run_until_halt()
    while computer.output_queue:
        print(computer.output_queue.popleft())
        # Expected result for my input is 7566643


if __name__ == "__main__":
    program = parse_input(aoc_common.load_puzzle_input(DAY))
    main(program)
