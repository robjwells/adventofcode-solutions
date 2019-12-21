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


@pytest.mark.parametrize(
    "signal,phases,first_eight_string",
    [
        (12345678, 1, "48226158"),
        (12345678, 2, "34040438"),
        (12345678, 3, "03415518"),
        (12345678, 4, "01029498"),
        (80871224585914546619083218645595, 100, "24176176"),
        (19617804207202209144916044189917, 100, "73745418"),
        (69317163492948606335995924319873, 100, "52432133"),
    ],
)
def test_fft(signal: int, phases: int, first_eight_string: str) -> None:
    result_signal = repeat_fft(aoc_common.split_number_by_places(signal), phases)
    assert "".join(map(str, result_signal[:8])) == first_eight_string


def main(signal: List[int]) -> str:
    after_100_phases = repeat_fft(signal, phases=100)
    after_100_first_eight = "".join(map(str, after_100_phases[:8]))
    return after_100_first_eight


if __name__ == "__main__":
    signal = aoc_common.split_number_by_places(int(aoc_common.load_puzzle_input(DAY)))
    part_one_solution = main(signal)

    assert (
        part_one_solution == "76795888"
    ), "Part one solution doesn't match known-correct answer."

    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
