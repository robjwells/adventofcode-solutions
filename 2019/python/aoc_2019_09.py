"""Day 9: Sensor Boost"""
from typing import List, Tuple

import aoc_common
from intcode import IntCode, parse_program

DAY = 9


def main(program: List[int]) -> Tuple[int, int]:
    boost_test = IntCode(program)
    boost_test.pass_input(1)
    boost_test.run_until_halt()
    while len(boost_test.output_queue) > 1:
        print(f"Failed BOOST test for instruction: {boost_test.read_output()}")
    boost_keycode = boost_test.read_output()

    boosted_sensors = IntCode(program)
    boosted_sensors.pass_input(2)
    boosted_sensors.run_until_halt()
    distress_signal_coords = boosted_sensors.read_output()

    return boost_keycode, distress_signal_coords


if __name__ == "__main__":
    program = parse_program(aoc_common.load_puzzle_input(DAY))
    part_one_solution, part_two_solution = main(program)
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution=part_two_solution,
    )
