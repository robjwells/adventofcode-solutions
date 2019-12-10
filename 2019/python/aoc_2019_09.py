"""Day 9: Sensor Boost"""
from typing import List

import aoc_common
from intcode import IntCode, parse_program

DAY = 9


def main(program: List[int]) -> int:
    computer = IntCode(program)
    computer.pass_input(1)
    computer.run_until_halt()
    while len(computer.output_queue) > 1:
        print(f"Failed BOOST test for instruction: {computer.read_output()}")
    boost_keycode = computer.read_output()
    return boost_keycode


if __name__ == "__main__":
    program = parse_program(aoc_common.load_puzzle_input(DAY))
    part_one_solution = main(program)
    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
