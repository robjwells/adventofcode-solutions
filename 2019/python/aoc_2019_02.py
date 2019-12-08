"""Day 2: 1202 Program Alarm"""
from typing import List, Optional

import aoc_common
from intcode import IntCode, parse_program

DAY = 2


def patch_input(input_data: List[int], noun: int, verb: int) -> List[int]:
    data = input_data[:]
    data[1] = noun
    data[2] = verb
    return data


def solve_part_one(input_data: List[int]) -> int:
    data = patch_input(input_data, noun=12, verb=2)
    executed_data = IntCode.execute_program(data)
    return executed_data[0]


def solve_part_two(input_data: List[int]) -> Optional[int]:
    for noun in range(100):
        for verb in range(100):
            data = patch_input(input_data, noun, verb)
            executed_data = IntCode.execute_program(data)
            if executed_data[0] == 19690720:
                return 100 * noun + verb
    return None


if __name__ == "__main__":
    puzzle_input = aoc_common.load_puzzle_input(DAY)
    parsed = parse_program(puzzle_input)
    part_one_solution = solve_part_one(parsed)
    assert part_one_solution == 5866663, "Solution does not match known-correct"
    part_two_solution = solve_part_two(parsed)
    assert part_two_solution == 4259, "Solution does not match known-correct"
    if part_two_solution is None:
        print("!! Failed to find part two solution.")
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution=part_two_solution,
    )
