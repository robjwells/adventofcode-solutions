"""Day 12: The N-Body Problem"""
from __future__ import annotations

import re
from collections import defaultdict
from functools import reduce
from itertools import combinations
from typing import DefaultDict, Iterable, List, NamedTuple, Tuple

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
        return deltas_by_moon[0], deltas_by_moon[1]

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

    @property
    def potential_energy(self) -> int:
        return sum(map(abs, self.position))  # type: ignore # something odd with abs

    @property
    def kinetic_energy(self) -> int:
        return sum(map(abs, self.velocity))  # type: ignore # something odd with abs

    @property
    def total_energy(self) -> int:
        return self.potential_energy * self.kinetic_energy

    def __str__(self) -> str:
        px, py, pz = self.position
        vx, vy, vz = self.velocity
        return f"pos=<x={px: 3}, y={py: 3}, z={pz: 3}>, vel=<x={vx: 3}, y={vy: 3}, z={vz: 3}>"


def simulate_step(moons: List[Moon]) -> List[Moon]:
    pairings = combinations(moons, 2)
    gravity_changes: DefaultDict[Moon, List[Velocity]] = defaultdict(list)
    for moon_a, moon_b in pairings:
        a_delta, b_delta = Moon.compute_gravity(moon_a, moon_b)
        gravity_changes[moon_a].append(a_delta)
        gravity_changes[moon_b].append(b_delta)
    return [
        moon.update_velocity(Velocity.combine(deltas)).apply_velocity()
        for moon, deltas in gravity_changes.items()
    ]


def simulate_n_steps(moons: List[Moon], n: int = 1000) -> List[Moon]:
    for _ in range(n):
        moons = simulate_step(moons)
    return moons


def parse_input(input_string: str) -> List[Moon]:
    moon_regex = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    matches = [moon_regex.match(line) for line in input_string.splitlines()]
    assert all(
        match is not None for match in matches
    ), "Could not parse all input lines."
    positions = [Position(*map(int, m.groups())) for m in matches]  # type: ignore
    return [Moon(pos, Velocity.static()) for pos in positions]


def main(moons: List[Moon]) -> int:
    after_1000_steps = simulate_n_steps(moons, 1000)
    all_moons_total_energy = sum(moon.total_energy for moon in after_1000_steps)

    return all_moons_total_energy


def test_total_energy() -> None:
    sample = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
"""
    moons = parse_input(sample)
    after_10_steps = simulate_n_steps(moons, 10)
    system_total_energy = sum(moon.total_energy for moon in after_10_steps)
    assert system_total_energy == 179


if __name__ == "__main__":

    moons = parse_input(aoc_common.load_puzzle_input(DAY))
    part_one_solution = main(moons)

    assert (
        part_one_solution == 12053
    ), "Part one solution doesn't match known-correct answer."

    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
