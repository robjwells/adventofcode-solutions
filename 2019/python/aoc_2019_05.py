"""Day 5: Sunny with a Chance of Asteroids"""
from typing import List, Tuple

import aoc_common
from intcode import IntCode

DAY = 5


def parse_input(puzzle_input: str) -> List[int]:
    return [int(x) for x in puzzle_input.split(",")]


def main(program: List[int]) -> Tuple[int, int]:
    # Part one: provide 1 as input
    computer = IntCode(program)
    computer.input_queue.append(1)
    computer.run_until_halt()
    while computer.output_queue:
        output = computer.output_queue.popleft()
        if not computer.output_queue:
            part_one_solution = output

    # Part two: provide 5 as input
    computer = IntCode(program)
    computer.input_queue.append(5)
    computer.run_until_halt()
    part_two_solution = computer.output_queue.popleft()

    return (part_one_solution, part_two_solution)


if __name__ == "__main__":
    program = parse_input(aoc_common.load_puzzle_input(DAY))
    part_one_solution, part_two_solution = main(program)
    assert (
        part_one_solution == 7566643
    ), "Part one solution different from known-correct."
    assert (
        part_two_solution == 9265694
    ), "Part two solution different from known-correct."
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution=part_two_solution,
    )
