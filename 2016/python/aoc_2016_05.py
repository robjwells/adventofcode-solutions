import hashlib
from itertools import count, islice
from typing import Iterator, Tuple

from aoc_common import load_puzzle_input, report_solution


def stream_md5_hash_digests(door_id: str) -> Iterator[str]:
    for index in count():
        h = hashlib.new("md5")
        h.update(f"{door_id}{index}".encode())
        yield h.hexdigest()


def stream_digests_with_five_leading_zeroes(door_id: str) -> Iterator[str]:
    for digest in stream_md5_hash_digests(door_id):
        if digest.startswith("00000"):
            yield digest


def stream_digest_positions_and_characters(door_id: str) -> Iterator[Tuple[int, str]]:
    for digest in stream_digests_with_five_leading_zeroes(door_id):
        if digest[5] in "01234567":
            yield (int(digest[5]), digest[6])


def find_password_in_order(door_id: str) -> str:
    digests = islice(stream_digests_with_five_leading_zeroes(door_id), 8)
    password = "".join(digest[5] for digest in digests)
    return password


def format_password(characters: dict[int, str]) -> str:
    chars = [characters.get(position, "_") for position in range(8)]
    return "".join(chars)


def find_password_by_position(door_id: str) -> str:
    found_characters: dict[int, str] = {}
    digests = stream_digest_positions_and_characters(door_id)
    while len(found_characters) < 8:
        position, character = next(digests)
        if position not in found_characters:
            found_characters[position] = character
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
