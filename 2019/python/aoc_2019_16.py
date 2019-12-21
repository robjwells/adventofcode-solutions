"""Day 16: Flawed Frequency Transmission"""
from itertools import chain, cycle
from typing import Iterator, List

import aoc_common

import pytest

DAY = 16


def pattern(place: int = 1) -> Iterator[int]:
    base = [0, 1, 0, -1]
    output = []
    for digit in base:
        output.extend([digit] * place)
    return chain(output[1:], cycle(output))


@pytest.mark.parametrize(
    "place,first_eight_digits",
    [
        (1, [1, 0, -1, 0, 1, 0, -1, 0]),
        (2, [0, 1, 1, 0, 0, -1, -1, 0]),
        (3, [0, 0, 1, 1, 1, 0, 0, 0]),
        (4, [0, 0, 0, 1, 1, 1, 1, 0]),
        (5, [0, 0, 0, 0, 1, 1, 1, 1]),
        (6, [0, 0, 0, 0, 0, 1, 1, 1]),
        (7, [0, 0, 0, 0, 0, 0, 1, 1]),
        (8, [0, 0, 0, 0, 0, 0, 0, 1]),
    ],
)
def test_pattern(place: int, first_eight_digits: List[int]) -> None:
    assert all(
        expected == actual
        for expected, actual in zip(first_eight_digits, pattern(place))
    )


def fft(signal: List[int]) -> List[int]:
    output: List[int] = []
    for place in range(1, len(signal) + 1):
        sum_of_products = sum(
            signal_digit * pattern_digit
            for signal_digit, pattern_digit in zip(signal, pattern(place))
            if pattern_digit
        )
        new_digit = abs(sum_of_products) % 10
        output.append(new_digit)
    return output


def repeat_fft(signal: List[int], phases: int) -> List[int]:
    for _ in range(phases):
        signal = fft(signal)
    return signal


def rejoin_place_list(digits: List[int]) -> int:
    rejoined = 0
    for p10, digit in enumerate(reversed(digits)):
        rejoined += digit * 10 ** p10
    return rejoined


def main(signal: List[int]) -> int:
    after_100_phases = repeat_fft(signal, phases=100)
    after_100_first_eight = rejoin_place_list(after_100_phases[:8])
    return after_100_first_eight


if __name__ == "__main__":
    signal = aoc_common.split_number_by_places(int(aoc_common.load_puzzle_input(DAY)))
    part_one_solution = main(signal)

    assert (
        part_one_solution == 76795888
    ), "Part one solution doesn't match known-correct answer."

    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
