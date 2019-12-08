"""Day 7: Amplification Circuit"""
from itertools import permutations
from typing import List

import pytest

import aoc_common
from intcode import IntCode, parse_program

DAY = 7


def max_of_single_amp_run(program: List[int], phase_range: range = range(5)) -> int:
    possible_phases = permutations(phase_range)
    max_output = 0

    for phases in possible_phases:
        amps = [IntCode(program) for _ in phase_range]
        for amp, phase in zip(amps, phases):
            amp.input_queue.append(phase)

        amps[0].input_queue.append(0)
        amps[0].run_until_halt()

        for idx, amp_b in enumerate(amps[1:], start=1):
            amp_b.input_queue.append(amps[idx - 1].output_queue.popleft())
            amp_b.run_until_halt()

        last_amp_output = amps[-1].output_queue.popleft()
        if last_amp_output > max_output:
            max_output = last_amp_output

    return max_output


def main(program: List[int]) -> int:
    return max_of_single_amp_run(program)


@pytest.mark.parametrize(
    "program,expected_result",
    [
        # fmt: off
        (
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            43210
        ),
        (
            [
                3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23,
                23, 1, 24, 23, 23, 4, 23, 99, 0, 0
            ],
            54321
        ),
        (
            [
                3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0,
                33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99,
                0, 0, 0
            ],
            65210
        ),
        # fmt: on
    ],
)
def test_max_of_single_amp_run(program: List[int], expected_result: int) -> None:
    assert max_of_single_amp_run(program) == expected_result


if __name__ == "__main__":
    program = parse_program(aoc_common.load_puzzle_input(DAY))
    part_one_solution = main(program)
    assert (
        part_one_solution == 14902
    ), "Part one solution does not match known-correct solution."
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution=None,
    )
