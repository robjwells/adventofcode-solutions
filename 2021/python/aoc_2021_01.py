"""--- Day 1: Sonar Sweep ---"""
from pathlib import Path

from more_itertools import windowed


def parse_puzzle_input(text: str) -> list[int]:
    return [int(line) for line in text.splitlines()]


def count_decreases(depths: list[int]) -> int:
    pairs = zip(depths[:-1], depths[1:], strict=True)
    return sum(1 for earlier, later in pairs if later > earlier)


def count_windowed_decreases(depths: list[int], window_size: int = 3) -> int:
    sums = [sum(w) for w in windowed(depths, n=window_size, fillvalue=0)]
    return count_decreases(sums)


def solve(puzzle_input_text: str) -> tuple[int, int]:
    depths = parse_puzzle_input(puzzle_input_text)
    part_one_result = count_decreases(depths)
    part_two_result = count_windowed_decreases(depths)
    return part_one_result, part_two_result


if __name__ == "__main__":
    puzzle_input_file = Path(__file__).parent.parent.joinpath("input", "2021-01.txt")
    p1, p2 = solve(puzzle_input_file.read_text())
    print(
        "=" * len(__doc__ or ""),
        __doc__,
        "=" * len(__doc__ or ""),
        f"Part one: {p1}",
        f"Part two: {p2}",
        sep="\n",
    )
