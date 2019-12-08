from typing import List

import pytest

from intcode import IntCode


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
    assert IntCode.execute_program(input_data) == output_data


@pytest.mark.parametrize(
    "program,index_to_check,expected_value",
    [([1101, 100, -1, 4, 0], 4, 99), ([1002, 4, 3, 4, 33], 4, 99)],
)
def test_paramater_modes(
    program: List[int], index_to_check: int, expected_value: int
) -> None:
    result = IntCode.execute_program(program)
    assert result[index_to_check] == expected_value


@pytest.mark.parametrize(
    "program, program_input, expected_output",
    [
        # Equal to 8 -> 1, memory fetch
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 1, 0),
        # Less than 8 -> 1, memory fetch
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 2, 1),
        # Equal to 8 -> 1, immediate
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 1, 0),
        # Less than 8 -> 1, immediate
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 2, 1),
    ],
)
def test_comparisons(
    program: List[int], program_input: int, expected_output: int
) -> None:
    computer = IntCode(program)
    computer.pass_input(program_input)
    computer.run_until_halt()
    assert computer.read_output() == expected_output


@pytest.mark.parametrize(
    "program, program_input, expected_output",
    [
        # Jump if zero, memory fetch
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 20, 1),
        # Jump if zero, immediate
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 20, 1),
    ],
)
def test_jumps(program: List[int], program_input: int, expected_output: int) -> None:
    computer = IntCode(program)
    computer.pass_input(program_input)
    computer.run_until_halt()
    assert computer.read_output() == expected_output


@pytest.mark.parametrize(
    "program_input,expected_output",
    [
        (-1, 999),
        (0, 999),
        (1, 999),
        (2, 999),
        (3, 999),
        (4, 999),
        (5, 999),
        (6, 999),
        (7, 999),
        (8, 1000),
        (9, 1001),
        (10, 1001),
        (11, 1001),
        (12, 1001),
        (13, 1001),
        (14, 1001),
        (15, 1001),
        (16, 1001),
    ],
)
def test_larger_comparison(program_input: int, expected_output: int) -> None:
    # fmt: off
    program = [
        3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31, 1106,
        0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104, 999, 1105,
        1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99
    ]
    # fmt: on
    computer = IntCode(program)
    computer.pass_input(program_input)
    computer.run_until_halt()
    assert computer.read_output() == expected_output
