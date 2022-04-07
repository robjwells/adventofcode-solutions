"""--- Day 3: Binary Diagnostic ---"""
from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from typing import Iterable

import aoc
import pytest


def all_the_same(items: Iterable[int]) -> bool:
    return len(set(items)) == 1


def most_common(items: list[str]) -> str:
    counter = Counter(items)
    if not all_the_same(counter.values()):
        value, _ = counter.most_common(1)[0]
        return value
    else:
        return "1"


def least_common(items: list[str]) -> str:
    return "1" if most_common(items) == "0" else "0"


def test_most_common() -> None:
    vals = ["0", "1", "1", "1", "1", "0", "0", "1", "1", "1", "0", "0"]
    assert most_common(vals) == "1"


def test_least_common() -> None:
    vals = ["0", "1", "1", "1", "1", "0", "0", "1", "1", "1", "0", "0"]
    assert least_common(vals) == "0"


def map_characters(function, binary_numbers: list[str]) -> str:
    return "".join([function(list(xs)) for xs in zip(*binary_numbers)])


def gamma_rate_binary(binary_numbers: list[str]) -> str:
    return map_characters(most_common, binary_numbers)


def epsilon_rate_binary(binary_numbers: list[str]) -> str:
    return map_characters(least_common, binary_numbers)


@pytest.fixture
def test_numbers() -> list[str]:
    return [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]


def test_epsilon_rate_binary(test_numbers: list[str]) -> None:
    assert epsilon_rate_binary(test_numbers) == "01001"


def test_gamma_rate_binary(test_numbers: list[str]) -> None:
    assert gamma_rate_binary(test_numbers) == "10110"


def power_consumption(binary_numbers: list[str]) -> int:
    gamma_b = gamma_rate_binary(binary_numbers)
    epsilon_b = epsilon_rate_binary(binary_numbers)
    return int(gamma_b, 2) * int(epsilon_b, 2)


def filter_characters(
    function: Callable[[list[str]], str], binary_numbers: list[str]
) -> str:
    remaining = binary_numbers
    for index in range(len(binary_numbers[0])):
        bit_criteria = function([bn[index] for bn in remaining])
        remaining = [bn for bn in remaining if bn[index] == bit_criteria]
        if len(remaining) == 1:
            return remaining[0]
    assert False, "Filtered out all numbers."


def oxygen_generator_rating(binary_numbers: list[str]) -> str:
    return filter_characters(most_common, binary_numbers)


def co2_scrubber_rating(binary_numbers: list[str]) -> str:
    return filter_characters(least_common, binary_numbers)


def test_oxygen_generator_rating(test_numbers: list[str]) -> None:
    assert oxygen_generator_rating(test_numbers) == "10111"


def test_co2_scrubber_rating(test_numbers: list[str]) -> None:
    assert co2_scrubber_rating(test_numbers) == "01010"


def life_support_rating(binary_numbers: list[str]) -> int:
    oxygen_b = oxygen_generator_rating(binary_numbers)
    co2_b = co2_scrubber_rating(binary_numbers)
    return int(oxygen_b, 2) * int(co2_b, 2)


def main(puzzle_input: str) -> tuple[int, int]:
    binary_numbers = puzzle_input.splitlines()
    p1 = power_consumption(binary_numbers)
    p2 = life_support_rating(binary_numbers)
    return p1, p2


if __name__ == "__main__":
    puzzle_input = aoc.load_puzzle_input(2021, 3)
    p1, p2 = main(puzzle_input)
    print(aoc.format_solution(title=__doc__, part_one=p1, part_two=p2))
