import hashlib
from itertools import count, islice
from typing import Dict, Iterator

from aoc_common import load_puzzle_input, report_solution


def stream_md5_hash_digests(door_id: str, prefix: str = "00000") -> Iterator[str]:
    for index in count():
        hash = hashlib.new("md5")
        hash.update(f"{door_id}{index}".encode())
        digest = hash.hexdigest()
        if digest.startswith(prefix):
            yield hash.hexdigest()


def find_password_in_order(door_id: str) -> str:
    digests = islice(stream_md5_hash_digests(door_id), 8)
    password = "".join(digest[5] for digest in digests)
    return password


def format_password(characters: Dict[int, str]) -> str:
    chars = [characters.get(position, "_") for position in range(8)]
    return "".join(chars)


def find_password_by_position(door_id: str) -> str:
    found_characters: Dict[int, str] = {}
    digests = stream_md5_hash_digests(door_id)
    while len(found_characters) < 8:
        digest = next(digests)
        pos_str = digest[5]
        if pos_str.isdigit():
            position = int(pos_str)
            if 0 <= position <= 7 and position not in found_characters:
                found_characters[position] = digest[6]
                # print(format_password(found_characters))  # Fun!
    return format_password(found_characters)


if __name__ == "__main__":
    door_id = load_puzzle_input(day=5)
    first_password = find_password_in_order(door_id)
    second_password = find_password_by_position(door_id)
    report_solution(
        puzzle_title="Day 5: How About a Nice Game of Chess?",
        part_one_solution=first_password,
        part_two_solution=second_password,
    )
