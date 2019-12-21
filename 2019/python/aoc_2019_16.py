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


@pytest.mark.parametrize("place,first_eight_digits", [
    (1, [1, 0, -1, 0, 1, 0, -1, 0]),
    (2, [0, 1, 1, 0, 0, -1, -1, 0]),
    (3, [0, 0, 1, 1, 1, 0, 0, 0]),
    (4, [0, 0, 0, 1, 1, 1, 1, 0]),
    (5, [0, 0, 0, 0, 1, 1, 1, 1]),
    (6, [0, 0, 0, 0, 0, 1, 1, 1]),
    (7, [0, 0, 0, 0, 0, 0, 1, 1]),
    (8, [0, 0, 0, 0, 0, 0, 0, 1]),
])
def test_pattern(place: int, first_eight_digits: List[int]) -> None:
    assert [p for p, _ in zip(pattern(place), range(8))] == first_eight_digits


def main(signal: List[int]) -> None:
    pass



if __name__ == "__main__":
    signal = aoc_common.split_number_by_places(int(aoc_common.load_puzzle_input(DAY)))
