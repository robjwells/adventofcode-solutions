"""Day 2: 1202 Program Alarm"""
import aoc_common
from operator import add, mul
import pytest
from typing import Callable, List

DAY = 2

PC_INCREMENT = 4
HALT = 99


@pytest.mark.parametrize(
    "input_data,output_data",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
def test_execute_program(input_data: List[int], output_data: List[int]) -> None:
    assert execute_program(input_data) == output_data


def opcode_to_function(opcode: int) -> Callable[[int, int], int]:
    functions = {1: add, 2: mul}
    return functions[opcode]


def execute_program(input_data: List[int]) -> List[int]:
    data = input_data[:]
    for program_counter in range(0, len(data), PC_INCREMENT):
        opcode, *locations = data[program_counter : program_counter + PC_INCREMENT]
        if opcode == HALT:
            break
        source1, source2, destination = locations
        data[destination] = opcode_to_function(opcode)(data[source1], data[source2])
    return data


def patch_input(input_data: List[int]) -> List[int]:
    data = input_data[:]
    data[1] = 12
    data[2] = 2
    return data


def solve_part_one(input_data: List[int]) -> int:
    data = patch_input(input_data)
    executed_data = execute_program(data)
    return executed_data[0]


def parse_input(puzzle_input: str) -> List[int]:
    return [int(x) for x in puzzle_input.split(",")]


if __name__ == "__main__":
    puzzle_input = aoc_common.load_puzzle_input(DAY)
    parsed = parse_input(puzzle_input)
    part_one_solution = solve_part_one(parsed)
    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
