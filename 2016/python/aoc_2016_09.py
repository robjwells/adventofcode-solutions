from __future__ import annotations

import re

import pytest

from aoc_common import load_puzzle_input, report_solution

_marker = re.compile(r"\( (?P<length> \d+ ) x (?P<times> \d+ ) \)", flags=re.VERBOSE)


def decompressed_length(string: str, position: int = 0, length: int = 0) -> int:
    if position >= len(string):
        return length
    if match := _marker.match(string, pos=position):
        repeat_length = int(match["length"])
        repeat_times = int(match["times"])
        new_length = length + (repeat_length * repeat_times)
        new_position = match.end(0) + repeat_length
        return decompressed_length(string, new_position, new_length)
    return decompressed_length(string, position + 1, length + 1)


@pytest.mark.parametrize(
    "string,expected",
    [
        ("ADVENT", 6),
        ("A(1x5)BC", 7),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 6),
        ("X(8x2)(3x3)ABCY", 18),
    ],
)
def test_decompressed_length(string: str, expected: int) -> None:
    assert decompressed_length(string) == expected


if __name__ == "__main__":
    compressed = load_puzzle_input(day=9)
    v1_length = decompressed_length(compressed)
    report_solution(
        puzzle_title="Day 9: Explosives in Cyberspace", part_one_solution=v1_length
    )
