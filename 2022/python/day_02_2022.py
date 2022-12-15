from __future__ import annotations
from dataclasses import dataclass

from enum import IntEnum

from util import read_input


class Shape(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def parse(cls, char: str) -> Shape:
        match char:
            case "A" | "X":
                return cls.ROCK
            case "B" | "Y":
                return cls.PAPER
            case "C" | "Z":
                return cls.SCISSORS
            case _:
                raise ValueError(f"Invalid abbreviation: {char!r}")


class Result(IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6

    @classmethod
    def parse(cls, char: str) -> Result:
        match char:
            case "X":
                return cls.LOSE
            case "Y":
                return cls.DRAW
            case "Z":
                return cls.WIN
            case _:
                raise ValueError(f"Invalid abbreviation: {char!r}")


def responses_to_opponent_shape(s: Shape) -> dict[Shape, Result]:
    # Opponent's Shape -> My Shape -> Result (for me)
    STRATEGY: dict[Shape, dict[Shape, Result]] = {
        # They play
        Shape.ROCK: {
            # I play
            Shape.SCISSORS: Result.LOSE,
            Shape.ROCK: Result.DRAW,
            Shape.PAPER: Result.WIN,
        },
        # They play
        Shape.PAPER: {
            # I play
            Shape.ROCK: Result.LOSE,
            Shape.PAPER: Result.DRAW,
            Shape.SCISSORS: Result.WIN,
        },
        # They play
        Shape.SCISSORS: {
            # I play
            Shape.PAPER: Result.LOSE,
            Shape.SCISSORS: Result.DRAW,
            Shape.ROCK: Result.WIN,
        },
    }
    return STRATEGY[s]


def judge_round(*, me: Shape, opponent: Shape) -> Result:
    return responses_to_opponent_shape(opponent)[me]


@dataclass(frozen=True)
class ShapePair:
    opponent: Shape
    me: Shape


def parse_shape_pairs(puzzle_input: str) -> list[ShapePair]:
    parts = [line.split() for line in puzzle_input.splitlines()]
    return [
        ShapePair(opponent=Shape.parse(opponent), me=Shape.parse(me))
        for opponent, me in parts
    ]


def solve_part_one(puzzle_input: str) -> int:
    shape_pairs = parse_shape_pairs(puzzle_input)
    round_scores = [
        pair.me + judge_round(me=pair.me, opponent=pair.opponent)
        for pair in shape_pairs
    ]
    return sum(round_scores)


@dataclass(frozen=True)
class ShapeResult:
    opponent: Shape
    outcome: Result


def parse_shape_and_result(puzzle_input: str) -> list[ShapeResult]:
    parts = [line.split() for line in puzzle_input.splitlines()]
    return [
        ShapeResult(opponent=Shape.parse(opponent), outcome=Result.parse(outcome))
        for opponent, outcome in parts
    ]


def match_shape_to_outcome(opponent: Shape, desired_result: Result) -> Shape:
    for shape, result in responses_to_opponent_shape(opponent).items():
        if result == desired_result:
            return shape
    raise ValueError(
        f"Should be unreachable. Got args:  {opponent=}  {desired_result=}"
    )


def solve_part_two(puzzle_input: str) -> int:
    result_pairs = parse_shape_and_result(puzzle_input)
    swapped = [
        match_shape_to_outcome(pair.opponent, pair.outcome) + pair.outcome
        for pair in result_pairs
    ]
    return sum(swapped)


def main() -> None:
    puzzle_input = read_input(2)
    part_one = solve_part_one(puzzle_input)
    print(f"Part one: {part_one:,}")

    part_two = solve_part_two(puzzle_input)
    print(f"Part two: {part_two:,}")


if __name__ == "__main__":
    main()


SAMPLE_INPUT = """\
A Y
B X
C Z
"""


def test_sample_input_part_one() -> None:
    assert solve_part_one(SAMPLE_INPUT) == 15


def test_sample_input_part_two() -> None:
    assert solve_part_two(SAMPLE_INPUT) == 12
