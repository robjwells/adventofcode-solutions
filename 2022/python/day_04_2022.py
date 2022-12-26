from __future__ import annotations

from util import read_input


def parse_range(r: str) -> set[int]:
    start, last = [int(n) for n in r.split("-", 1)]
    return set(range(start, last + 1))


def parse_pair(pair: str) -> tuple[set[int], set[int]]:
    first, second = pair.split(",", 1)
    return (parse_range(first), parse_range(second))


Pair = tuple[set[int], set[int]]


def parse(puzzle_input: str) -> list[Pair]:
    return [parse_pair(p) for p in puzzle_input.splitlines()]


def solve_part_one(pairs: list[Pair]) -> int:
    either_fully_contained = [
        True
        for first, second in pairs
        if first <= second or second <= first
    ]
    return len(either_fully_contained)


def solve_part_two(pairs: list[Pair]) -> int:
    return len([True for first, second in pairs if first & second])


def main() -> None:
    puzzle_input = read_input(4)
    pairs = parse(puzzle_input)

    part_one = solve_part_one(pairs)
    print(f"Part one: {part_one:,}")

    part_two = solve_part_two(pairs)
    print(f"Part two: {part_two:,}")


if __name__ == "__main__":
    main()


SAMPLE_INPUT = parse(
    """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""
)


def test_sample_input_part_one() -> None:
    assert solve_part_one(SAMPLE_INPUT) == 2


def test_sample_input_part_two() -> None:
    assert solve_part_two(SAMPLE_INPUT) == 4
