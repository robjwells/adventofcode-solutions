"""--- Day 1: Sonar Sweep ---"""

import aoc
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
    puzzle_input = aoc.load_puzzle_input(2021, 1)
    p1, p2 = solve(puzzle_input)
    print(aoc.format_solution(title=__doc__, part_one=p1, part_two=p2))
