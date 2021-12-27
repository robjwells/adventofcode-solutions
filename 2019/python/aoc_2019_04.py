"""Day 4: Secure Container"""
from __future__ import annotations

from typing import List, Optional, Tuple

import aoc

DAY = 4


def test_acceptability() -> None:
    assert is_acceptable(111111)
    assert not is_acceptable(223450)
    assert not is_acceptable(123789)


def test_acceptability_nonoverlapping() -> None:
    assert is_acceptable(112233, overlapping_ok=False)
    assert not is_acceptable(123444, overlapping_ok=False)
    assert is_acceptable(111122, overlapping_ok=False)


def is_in_nondecreasing_order(place_list: List[int]) -> bool:
    for a, b in zip(place_list, place_list[1:]):
        if b < a:
            return False
    return True


def contains_double_number(place_list: List[int]) -> bool:
    for a, b in zip(place_list, place_list[1:]):
        if a == b:
            return True
    return False


def contains_nonoverlapping_double_number(place_list: List[int]) -> bool:
    group_lengths = []
    current = place_list[0]
    length = 1
    for n in place_list[1:]:
        if n == current:
            length += 1
        else:
            group_lengths.append(length)
            current = n
            length = 1
    group_lengths.append(length)  # Append group at the end
    return 2 in group_lengths


def is_acceptable(number: int, *, overlapping_ok: bool = True) -> bool:
    if overlapping_ok:
        double_func = contains_double_number
    else:
        double_func = contains_nonoverlapping_double_number
    place_list = aoc.split_number_by_places(number)
    return is_in_nondecreasing_order(place_list) and double_func(place_list)


def count_acceptable_numbers(
    puzzle_range: range, *, overlapping_ok: bool = True
) -> int:
    # Naive solution of just traversing the range
    count = 0
    for number in puzzle_range:
        if is_acceptable(number, overlapping_ok=overlapping_ok):
            count += 1
    return count


def parse_input(puzzle_input: str) -> range:
    """Split the input of dash-separated numbers into an inclusive range"""
    start, last = map(int, puzzle_input.split("-"))
    return range(start, last + 1)


def main() -> Tuple[int, Optional[int]]:
    puzzle_range = parse_input(aoc.load_puzzle_input(2019, DAY))
    number_acceptable = count_acceptable_numbers(puzzle_range)
    number_acceptable_nonoverlapping = count_acceptable_numbers(
        puzzle_range, overlapping_ok=False
    )
    return (number_acceptable, number_acceptable_nonoverlapping)


if __name__ == "__main__":
    part_one_solution, part_two_solution = main()
    print(
        aoc.format_solution(
            title=__doc__,
            part_one=part_one_solution,
            part_two=part_two_solution,
        )
    )
