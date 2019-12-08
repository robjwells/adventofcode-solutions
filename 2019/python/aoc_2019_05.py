"""Day 5: Sunny with a Chance of Asteroids"""
from typing import List, Tuple

import aoc_common
from intcode import IntCode, parse_program

DAY = 5


def main(program: List[int]) -> Tuple[int, int]:
    # Part one: provide 1 as input
    computer = IntCode(program)
    computer.pass_input(1)
    computer.run_until_halt()
    while computer.has_output():
        output = computer.read_output()
        if not computer.has_output():
            part_one_solution = output

    # Part two: provide 5 as input
    computer = IntCode(program)
    computer.pass_input(5)
    computer.run_until_halt()
    part_two_solution = computer.read_output()

    return (part_one_solution, part_two_solution)


if __name__ == "__main__":
    program = parse_program(aoc_common.load_puzzle_input(DAY))
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
