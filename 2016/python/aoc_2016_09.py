from __future__ import annotations

import re
from enum import Enum, auto

import pytest

from aoc import load_puzzle_input, format_solution

_marker = re.compile(r"\( (?P<length> \d+ ) x (?P<times> \d+ ) \)", flags=re.VERBOSE)


class FormatVersion(Enum):
    ONE = auto()
    TWO = auto()


def decompressed_length(
    string: str,
    format_version: FormatVersion = FormatVersion.ONE,
    *,
    position: int = 0,
    length: int = 0,
) -> int:
    if position >= len(string):
        return length
    if match := _marker.match(string, pos=position):
        repeat_length = int(match["length"])
        repeat_times = int(match["times"])
        next_position = match.end(0) + repeat_length
        if format_version is FormatVersion.ONE:
            new_length = length + (repeat_length * repeat_times)
        elif format_version is FormatVersion.TWO:
            recursive_length = decompressed_length(
                string[match.end(0) : next_position], format_version
            )
            new_length = length + (recursive_length * repeat_times)
        else:
            raise ValueError(f"Unknown format version: {format_version}")
        return decompressed_length(
            string, format_version, position=next_position, length=new_length
        )
    return decompressed_length(
        string, format_version, position=position + 1, length=length + 1
    )


@pytest.mark.parametrize(
    "string,expected_length",
    [
        ("ADVENT", 6),
        ("A(1x5)BC", 7),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 6),
        ("X(8x2)(3x3)ABCY", 18),
    ],
)
def test_decompressed_length(string: str, expected_length: int) -> None:
    assert decompressed_length(string) == expected_length


@pytest.mark.parametrize(
    "string,expected_length",
    [
        ("(3x3)XYZ", 9),
        ("X(8x2)(3x3)ABCY", 20),
        ("(27x12)(20x12)(13x14)(7x10)(1x12)A", 241920),
        ("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN", 445),
    ],
)
def test_v2_decompressed_length(string: str, expected_length: int) -> None:
    assert decompressed_length(string, FormatVersion.TWO) == expected_length


if __name__ == "__main__":
    compressed = load_puzzle_input(2016, day=9)
    v1_length = decompressed_length(compressed)
    v2_length = decompressed_length(compressed, FormatVersion.TWO)
    print(
        format_solution(
            title="Day 9: Explosives in Cyberspace",
            part_one=v1_length,
            part_two=v2_length,
        )
    )
