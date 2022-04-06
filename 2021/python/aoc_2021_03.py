"""--- Day 3: Binary Diagnostic ---"""
from __future__ import annotations

from collections import Counter

import aoc


def most_common(*items: str) -> str:
    value, _ = Counter(items).most_common(1)[0]
    return value


def least_common(*items: str) -> str:
    value, _ = Counter(items).most_common()[-1]
    return value


def test_most_common() -> None:
    vals = ["0", "1", "1", "1", "1", "0", "0", "1", "1", "1", "0", "0"]
    assert most_common(*vals) == "1"


def test_least_common() -> None:
    vals = ["0", "1", "1", "1", "1", "0", "0", "1", "1", "1", "0", "0"]
    assert least_common(*vals) == "0"


def gamma_rate_binary(binary_numbers: list[str]) -> str:
    return "".join([most_common(*xs) for xs in zip(*binary_numbers)])


def epsilon_rate_binary(binary_numbers: list[str]) -> str:
    return "".join([least_common(*xs) for xs in zip(*binary_numbers)])


def test_gamma_rate_binary() -> None:
    binary_numbers = [
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
    assert gamma_rate_binary(binary_numbers) == "10110"


def test_epsilon_rate_binary() -> None:
    binary_numbers = [
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
    assert epsilon_rate_binary(binary_numbers) == "01001"


def power_consumption(binary_numbers: list[str]) -> int:
    gamma_b = gamma_rate_binary(binary_numbers)
    epsilon_b = epsilon_rate_binary(binary_numbers)
    return int(gamma_b, 2) * int(epsilon_b, 2)


def main(puzzle_input: str) -> tuple[int, None]:
    binary_numbers = puzzle_input.splitlines()
    p1 = power_consumption(binary_numbers)
    return p1, None


if __name__ == "__main__":
    puzzle_input = aoc.load_puzzle_input(2021, 3)
    p1, p2 = main(puzzle_input)
    print(aoc.format_solution(title=__doc__, part_one=p1, part_two=p2))
