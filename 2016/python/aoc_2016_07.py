from __future__ import annotations

import re
from typing import List

import pytest

from aoc_common import load_puzzle_input, report_solution


class IPv7Address:
    full_address: str
    ordinary_parts: List[str]
    hypernet_parts: List[str]

    def __init__(self, ipv7_address: str) -> None:
        self.full_address = ipv7_address
        parts = re.split(r"\[|\]", ipv7_address)
        self.ordinary_parts = parts[::2]
        self.hypernet_parts = parts[1::2]

    @staticmethod
    def _contains_abba(part: str) -> bool:
        pattern = r"([a-z])([a-z])\2\1"
        matches = re.findall(pattern, part)
        filtered = [m for m in matches if m[0] != m[1]]
        return any(filtered)

    @property
    def supports_tls(self) -> bool:
        ordinary_abba = map(self._contains_abba, self.ordinary_parts)
        hypernet_abba = map(self._contains_abba, self.hypernet_parts)
        return any(ordinary_abba) and not any(hypernet_abba)

    def __repr__(self) -> str:
        return f"IPv7Address('{self.full_address}')"


@pytest.mark.parametrize(
    "full_address, ordinary_parts, hypernet_parts",
    [
        ("abba[mnop]qrst", ["abba", "qrst"], ["mnop"]),
        ("abcd[bddb]xyyx", ["abcd", "xyyx"], ["bddb"]),
        ("aaaa[qwer]tyui", ["aaaa", "tyui"], ["qwer"]),
        ("ioxxoj[asdfgh]zxcvbn", ["ioxxoj", "zxcvbn"], ["asdfgh"]),
    ],
)
def test_ipv7(
    full_address: str, ordinary_parts: List[str], hypernet_parts: List[str]
) -> None:
    sut = IPv7Address(full_address)

    assert sut.full_address == full_address
    assert sut.ordinary_parts == ordinary_parts
    assert sut.hypernet_parts == hypernet_parts


@pytest.mark.parametrize(
    "address, supports_tls",
    [
        ("abba[mnop]qrst", True),
        ("abcd[bddb]xyyx", False),
        ("aaaa[qwer]tyui", False),
        ("ioxxoj[asdfgh]zxcvbn", True),
    ],
)
def test_ipv7_tls(address: str, supports_tls: bool) -> None:
    sut = IPv7Address(address)
    assert sut.supports_tls == supports_tls


if __name__ == "__main__":
    addresses = [IPv7Address(line) for line in load_puzzle_input(day=7).splitlines()]
    support_tls = [address for address in addresses if address.supports_tls]
    report_solution(
        puzzle_title="Day 7: Internet Protocol Version 7",
        part_one_solution=len(support_tls)
    )
