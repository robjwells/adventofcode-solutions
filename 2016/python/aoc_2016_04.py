from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from aoc_common import load_puzzle_input, report_solution


@dataclass
class Room:
    encrypted_name: str
    sector: int
    checksum: str

    _room_regex = re.compile(
        r"^(?P<name>[a-z-]+)(?P<sector>\d+)\[(?P<checksum>[a-z]+)\]$"
    )

    @staticmethod
    def _name_is_valid(name: str, checksum: str) -> bool:
        counter = Counter(name.replace("-", ""))
        top_five = sorted(counter.most_common(), key=lambda t: (-t[1], t[0]))[:5]
        joined = "".join([letter for letter, count in top_five])
        return joined == checksum

    @classmethod
    def from_string(cls, s: str) -> Optional[Room]:
        if not (match := cls._room_regex.match(s.strip())):
            return None

        name = match["name"]
        sector = int(match["sector"])
        checksum = match["checksum"]

        if not cls._name_is_valid(name, checksum):
            return None

        return Room(name, sector, checksum)


if __name__ == "__main__":
    room_details = load_puzzle_input(day=4).splitlines()
    valid_rooms = [
        r for r in [Room.from_string(line) for line in room_details] if r is not None
    ]
    sum_of_sector_ids = sum(room.sector for room in valid_rooms)
    report_solution(
        puzzle_title="Day 4: Security Through Obscurity",
        part_one_solution=sum_of_sector_ids,
    )
