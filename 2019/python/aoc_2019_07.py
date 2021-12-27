"""Day 7: Amplification Circuit"""
from itertools import permutations
from typing import List, Tuple

import pytest

import aoc
from intcode import HaltExecution, IntCode, parse_program

DAY = 7


def max_of_single_amp_run(program: List[int], phase_range: range = range(5)) -> int:
    possible_phases = permutations(phase_range)
    max_output = 0

    for phases in possible_phases:
        amps = [IntCode(program) for _ in phase_range]
        for amp, phase in zip(amps, phases):
            amp.pass_input(phase)

        amps[0].pass_input(0)
        amps[0].run_until_halt()

        for idx, amp_b in enumerate(amps[1:], start=1):
            amp_b.pass_input(amps[idx - 1].read_output())
            amp_b.run_until_halt()

        last_amp_output = amps[-1].read_output()
        if last_amp_output > max_output:
            max_output = last_amp_output

    return max_output


class OutputSignal(Exception):
    pass


def max_of_feedback_loop(program: List[int], phase_range: range = range(5, 10)) -> int:
    possible_phases = permutations(phase_range)
    max_output = 0

    for phases in possible_phases:
        result = perform_feedback_loop(program, phases)
        if result > max_output:
            max_output = result

    return max_output


def perform_feedback_loop(program: List[int], phases: Tuple[int, ...]) -> int:
    def make_bufferer_and_signaller(amp: IntCode):
        def inner(value: int):
            amp.output_queue.append(value)
            raise OutputSignal(value)

        return inner

    amps = [IntCode(program, description=f"Amp {i}") for i in phases]
    for amp, phase in zip(amps, phases):
        amp.pass_input(phase)
        amp.output_action = make_bufferer_and_signaller(amp)  # type: ignore

    amps[0].pass_input(0)
    current_index = 0
    current_amp = amps[current_index]
    still_running = len(amps)
    while still_running > 0:
        try:
            while True:
                current_amp.step()
        except OutputSignal as exc:
            value = exc.args[0]
        except HaltExecution:
            still_running -= 1
            value = current_amp.output_queue.pop()  # Last output value from the amp
        current_index = (current_index + 1) % len(phases)
        current_amp = amps[current_index]
        current_amp.pass_input(value)
    return value


def main(program: List[int]) -> Tuple[int, int]:
    part_one_solution = max_of_single_amp_run(program)
    part_two_solution = max_of_feedback_loop(program)
    return part_one_solution, part_two_solution


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


@pytest.mark.parametrize(
    "program,expected_result",
    [
        # fmt: off
        (
            [
                3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27,
                4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5
            ],
            139629729
        ),
        (
            [
                3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55,
                1005, 55, 26, 1001, 54, -5, 54, 1105, 1, 12, 1, 53, 54, 53,
                1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001,
                56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10
            ],
            18216
        )
        # fmt: on
    ],
)
def test_max_of_feedback_loop(program: List[int], expected_result: int) -> None:
    assert max_of_feedback_loop(program) == expected_result


if __name__ == "__main__":
    program = parse_program(aoc.load_puzzle_input(2019, DAY))
    part_one_solution, part_two_solution = main(program)
    assert (
        part_one_solution == 14902
    ), "Part one solution does not match known-correct solution."
    assert (
        part_two_solution == 6489132
    ), "Part one solution does not match known-correct solution."
    print(
        aoc.format_solution(
            title=__doc__,
            part_one=part_one_solution,
            part_two=part_two_solution,
        )
    )
