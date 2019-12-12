"""Day 12: The N-Body Problem"""
from __future__ import annotations

import re
from functools import reduce
from itertools import combinations
from typing import Iterable, List, NamedTuple, Tuple

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
    def combine(velocities: Iterable[Velocity]) -> Velocity:
        def reducer(total: Velocity, current: Velocity) -> Velocity:
            return Velocity(*[t + c for t, c in zip(total, current)])

        return reduce(reducer, velocities)


class Moon(NamedTuple):
    position: Position
    velocity: Velocity

    @staticmethod
    def compute_gravity(a: Moon, b: Moon) -> Tuple[Velocity, Velocity]:
        velocity_deltas = [
            Moon._single_gravity_delta(a, b) for a, b in zip(a.position, b.position)
        ]
        deltas_by_moon = [Velocity(*deltas) for deltas in zip(*velocity_deltas)]
        new_velocities = map(
            Velocity.combine, zip([a.velocity, b.velocity], deltas_by_moon)
        )
        return (next(new_velocities), next(new_velocities))

    @staticmethod
    def _single_gravity_delta(a: int, b: int) -> Tuple[int, int]:
        if a < b:
            return (1, -1)
        elif b < a:
            return (-1, 1)
        return (0, 0)

    def update_velocity(self, v: Velocity) -> Moon:
        return Moon(
            position=self.position, velocity=Velocity.combine([self.velocity, v])
        )

    def apply_velocity(self) -> Moon:
        return Moon(
            Position(*[p + v for p, v in zip(self.position, self.velocity)]),
            self.velocity,
        )


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
