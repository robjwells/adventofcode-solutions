from __future__ import annotations

from util import read_input

from more_itertools import sliding_window
import pytest


PACKET_MARKER = 4
MESSAGE_MARKER = 14


def find_marker(buffer: str, marker_length: int) -> int:
    windows = sliding_window(buffer, marker_length)
    indexed = enumerate(windows, start=marker_length)
    marker_end_points = (
        n_chars_to_marker_end
        for n_chars_to_marker_end, window in indexed
        if len(set(window)) == marker_length
    )
    return next(marker_end_points)


def main() -> None:
    puzzle_text = read_input(6)

    part_one = find_marker(puzzle_text, PACKET_MARKER)
    assert part_one == 1343
    print(f"Part one: {part_one}")

    part_two = find_marker(puzzle_text, MESSAGE_MARKER)
    assert part_two == 2193
    print(f"Part two: {part_two}")


if __name__ == "__main__":
    main()

SAMPLE_INPUT_LABELS = [
    "buffer",
    "characters_to_packet",
    "characters_to_message",
]

SAMPLE_INPUTS = [
    ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 7, 19),
    ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5, 23),
    ("nppdvjthqldpwncqszvftbrmjlhg", 6, 23),
    ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10, 29),
    ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11, 26),
]


@pytest.mark.parametrize(SAMPLE_INPUT_LABELS, SAMPLE_INPUTS)
def test_sample_input(
    buffer: str, characters_to_packet: int, characters_to_message: int
) -> None:
    assert find_marker(buffer, PACKET_MARKER) == characters_to_packet
    assert find_marker(buffer, MESSAGE_MARKER) == characters_to_message
