"""Day 12: The N-Body Problem"""
from __future__ import annotations

from itertools import combinations
from typing import List, NamedTuple, Tuple
import re

import aoc_common

DAY = 12


class Position(NamedTuple):
    x: int
    y: int
    z: int


class Velocity(NamedTuple):
    x: int
    y: int
    z: int

    @classmethod
    def static(cls) -> Velocity:
        return cls(0, 0, 0)

    @staticmethod
    def _single_delta(a: int, b: int) -> Tuple[int, int]:
        if a < b:
            return (1, -1)
        elif b < a:
            return (-1, 1)
        return (0, 0)

    @classmethod
    def compute_deltas(cls, a: Velocity, b: Velocity) -> Tuple[Velocity, Velocity]:
        deltas = [
            Velocity._single_delta(a_component, b_component)
            for a_component, b_component in zip(a, b)
        ]
        velocity_deltas = [Velocity(x, y, z) for x, y, z in zip(*deltas)]
        return velocity_deltas[0], velocity_deltas[1]


class Moon(NamedTuple):
    position: Position
    velocity: Velocity


# def simulate_step(moons=List[Moon]) -> List[Moon]:
#     pairings = combinations(moons, 2)
#     # for moon_a, moon_b in pairings:


def parse_input(input_string: str) -> List[Moon]:
    moon_regex = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    matches = [moon_regex.match(line) for line in input_string.splitlines()]
    assert all(
        match is not None for match in matches
    ), "Could not parse all input lines."
    positions = [Position(*map(int, m.groups())) for m in matches]  # type: ignore
    return [Moon(pos, Velocity.static()) for pos in positions]


if __name__ == "__main__":
    moons = parse_input(aoc_common.load_puzzle_input(DAY))
