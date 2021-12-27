"""Day 16: Flawed Frequency Transmission"""
from itertools import accumulate, chain, cycle
from typing import Iterator, List, Tuple

import pytest

import aoc

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


def create_pattern_table(num_elements: int) -> List[List[int]]:
    return [
        [p for p, _ in zip(pattern(place), range(num_elements))]
        for place in range(1, num_elements + 1)
    ]


def test_create_pattern_table() -> None:
    expected = [
        [1, 0, -1, 0, 1, 0, -1, 0],
        [0, 1, 1, 0, 0, -1, -1, 0],
        [0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 1],
    ]
    assert create_pattern_table(8) == expected


def fft(signal: List[int], pattern_table: List[List[int]]) -> List[int]:
    output: List[int] = []
    midpoint = len(signal) // 2
    for single_pattern in pattern_table[:midpoint]:
        total = sum(
            signal_digit * pattern_digit
            for signal_digit, pattern_digit in zip(signal, single_pattern)
            if pattern_digit
        )
        output.append(abs(total) % 10)
    # After the pattern row with the index `midpoint`, the elements in the
    # pattern row from `midpoint` are all 1 and can just be summed.
    output.extend(
        abs(sum(signal[index:])) % 10 for index in range(midpoint, len(signal))
    )
    return output


def repeat_fft(signal: List[int], phases: int) -> List[int]:
    pattern_table = create_pattern_table(len(signal))
    for _ in range(phases):
        signal = fft(signal, pattern_table)
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
    result_signal = repeat_fft(aoc.split_number_by_places(signal), phases)
    assert "".join(map(str, result_signal[:8])) == first_eight_string


def cheating_fft(signal: List[int], offset: int) -> List[int]:
    relevant = signal[offset:]
    for phase in range(100):
        r_cumulative = accumulate(reversed(relevant))
        relevant = [total % 10 for total in reversed(list(r_cumulative))]
    return relevant


@pytest.mark.parametrize(
    "signal_string,first_eight",
    [
        ("03036732577212944063491565474664", "84462026"),
        ("02935109699940807407585447034323", "78725270"),
        ("03081770884921959731165446850517", "53553731"),
    ],
)
def test_cheating_fft(signal_string: str, first_eight: str) -> None:
    real_signal = (list(map(int, signal_string))) * 10_000
    offset = int("".join(map(str, real_signal[:7])))
    result = cheating_fft(real_signal, offset)
    assert "".join(map(str, result[:8])) == first_eight


def main(signal: List[int]) -> Tuple[str, str]:
    after_100_phases = repeat_fft(signal, phases=100)
    after_100_first_eight = "".join(map(str, after_100_phases[:8]))

    real_signal = signal * 10_000
    offset = int("".join(map(str, signal[:7])))
    real_after_100_phases = cheating_fft(real_signal, offset)
    real_after_100_first_eight = "".join(map(str, real_after_100_phases[:8]))

    return after_100_first_eight, real_after_100_first_eight


if __name__ == "__main__":
    signal = aoc.split_number_by_places(int(aoc.load_puzzle_input(2019, DAY)))
    part_one_solution, part_two_solution = main(signal)

    assert (
        part_one_solution == "76795888"
    ), "Part one solution doesn't match known-correct answer."

    assert (
        part_two_solution == "84024125"
    ), "Part two solution doesn't match known-correct answer."

    print(
        aoc.format_solution(
            title=__doc__,
            part_one=part_one_solution,
            part_two=part_two_solution,
        )
    )
