from __future__ import annotations

import re
from typing import Sequence

import pytest
from more_itertools import windowed

from aoc_common import load_puzzle_input, report_solution


class IPv7Address:
    full_address: str
    ordinary_parts: list[str]
    hypernet_parts: list[str]

    def __init__(self, ipv7_address: str) -> None:
        self.full_address = ipv7_address
        parts = re.split(r"\[|\]", ipv7_address)
        # Ordinary and hypernet parts alternate
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

    @staticmethod
    def _is_aba(seq: Sequence[str]) -> bool:
        return len(seq) == 3 and seq[0] == seq[2] and seq[0] != seq[1]

    def _find_aba(self) -> list[str]:
        return [
            "".join(triple)
            for part in self.ordinary_parts
            for triple in windowed(part, 3, fillvalue="")
            if self._is_aba(triple)
        ]

    def _find_bab(self, abas: list[str]) -> list[str]:
        return [
            "".join(triple)
            for part in self.hypernet_parts
            for triple in windowed(part, 3, fillvalue="")
            if self._is_aba(triple) and triple[1] + triple[0] + triple[1] in abas
        ]

    @property
    def supports_ssl(self) -> bool:
        return any(self._find_bab(self._find_aba()))

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
    full_address: str, ordinary_parts: list[str], hypernet_parts: list[str]
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


@pytest.mark.parametrize(
    "address,supports_ssl",
    [
        ("aba[bab]xyz", True),
        ("xyx[xyx]xyx", False),
        ("aaa[kek]eke", True),
        ("zazbz[bzb]cdb", True),
    ],
)
def test_ipv7_ssl(address: str, supports_ssl: bool) -> None:
    sut = IPv7Address(address)
    assert sut.supports_ssl == supports_ssl


if __name__ == "__main__":
    addresses = [IPv7Address(line) for line in load_puzzle_input(day=7).splitlines()]
    support_tls = [address for address in addresses if address.supports_tls]
    support_ssl = [address for address in addresses if address.supports_ssl]
    report_solution(
        puzzle_title="Day 7: Internet Protocol Version 7",
        part_one_solution=len(support_tls),
        part_two_solution=len(support_ssl),
    )
