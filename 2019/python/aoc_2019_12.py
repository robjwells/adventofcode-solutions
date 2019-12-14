"""Day 12: The N-Body Problem"""
from __future__ import annotations

import re
from collections import defaultdict
from functools import reduce
from itertools import combinations, count
from math import gcd
from typing import Callable, DefaultDict, Iterable, List, NamedTuple, Tuple

import pytest

import aoc_common

DAY = 12


Position = Tuple[int, int, int]
Velocity = Tuple[int, int, int]


def combine_velocities(vs: List[Velocity]) -> Velocity:
    acc = list(vs[0])
    for v in vs[1:]:
        acc[0] += v[0]
        acc[1] += v[1]
        acc[2] += v[2]
    return tuple(acc)  # type: ignore


class Moon(NamedTuple):
    moon_id: int
    position: Position
    velocity: Velocity

    @staticmethod
    def compute_gravity(a: Moon, b: Moon) -> Tuple[Velocity, Velocity]:
        velocity_deltas = [
            Moon._single_gravity_delta(a.position[0], b.position[0]),
            Moon._single_gravity_delta(a.position[1], b.position[1]),
            Moon._single_gravity_delta(a.position[2], b.position[2]),
        ]
        return (
            (velocity_deltas[0][0], velocity_deltas[1][0], velocity_deltas[2][0]),
            (velocity_deltas[0][1], velocity_deltas[1][1], velocity_deltas[2][1]),
        )

    @staticmethod
    def _single_gravity_delta(a: int, b: int) -> Tuple[int, int]:
        if a < b:
            return (1, -1)
        elif b < a:
            return (-1, 1)
        return (0, 0)

    def update_velocity(self, v: Velocity) -> Moon:
        return Moon(
            moon_id=self.moon_id,
            position=self.position,
            velocity=(
                self.velocity[0] + v[0],
                self.velocity[1] + v[1],
                self.velocity[2] + v[2],
            ),
        )

    def apply_velocity(self) -> Moon:
        return Moon(
            moon_id=self.moon_id,
            position=(
                self.position[0] + self.velocity[0],
                self.position[1] + self.velocity[1],
                self.position[2] + self.velocity[2],
            ),
            velocity=self.velocity,
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
        moon.update_velocity(combine_velocities(deltas)).apply_velocity()
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
        [match is not None for match in matches]
    ), "Could not parse all input lines."
    positions = [tuple(map(int, m.groups())) for m in matches]  # type: ignore
    return [
        Moon(n, pos, (0, 0, 0)) for n, pos in zip(count(), positions)
    ]  # type: ignore


@pytest.mark.parametrize(
    "input_data,steps,expected_energy",
    [
        (
            (
                "<x=-1, y=0, z=2>\n"
                "<x=2, y=-10, z=-7>\n"
                "<x=4, y=-8, z=8>\n"
                "<x=3, y=5, z=-1>"
            ),
            10,
            179,
        ),
        (
            (
                "<x=-8, y=-10, z=0>\n"
                "<x=5, y=5, z=10>\n"
                "<x=2, y=-7, z=3>\n"
                "<x=9, y=-8, z=-3>"
            ),
            100,
            1940,
        ),
    ],
)
def test_total_energy(input_data: str, steps: int, expected_energy: int) -> None:
    moons = parse_input(input_data)
    after_n_steps = simulate_n_steps(moons, steps)
    system_total_energy = sum(moon.total_energy for moon in after_n_steps)
    assert system_total_energy == expected_energy


@pytest.mark.parametrize(
    "input_data,cycle_time",
    [
        (
            (
                "<x=-1, y=0, z=2>\n"
                "<x=2, y=-10, z=-7>\n"
                "<x=4, y=-8, z=8>\n"
                "<x=3, y=5, z=-1>"
            ),
            2772,
        ),
        (
            (
                "<x=-8, y=-10, z=0>\n"
                "<x=5, y=5, z=10>\n"
                "<x=2, y=-7, z=3>\n"
                "<x=9, y=-8, z=-3>"
            ),
            4_686_774_924,
        ),
    ],
)
def test_calculate_cycle_time(input_data: str, cycle_time: int) -> None:
    moons = parse_input(input_data)
    assert calculate_cycle_time(moons) == cycle_time


def least_common_multiple(*numbers: int) -> int:
    """Find the least common multiple of several numbers."""

    def lcm(a: int, b: int) -> int:
        """Find the least common multiple of two numbers."""
        return a * (b // gcd(a, b))

    return reduce(lcm, numbers)


@pytest.mark.parametrize(
    "numbers,expected",
    [
        ((3, 5), 15),
        ((4, 5), 20),
        ((6, 10), 30),
        ((4, 6, 8), 24),
        ((2, 7, 13), 182),
        ((5, 11, 13), 715),
    ],
)
def test_least_common_multiple(numbers: Iterable[int], expected: int) -> None:
    assert least_common_multiple(*numbers) == expected


def find_cycle_length(
    moons: List[Moon], extractor: Callable[[Moon], Tuple[int, int, int]]
) -> int:
    initial_state = sorted(map(extractor, moons))
    for cycle in count(start=1):
        moons = simulate_step(moons)
        state = sorted(map(extractor, moons))
        if state == initial_state:
            return cycle
    assert False, "Unreachable"  # Make mypy happy


def calculate_cycle_time(moons: List[Moon]) -> int:
    """Find the system cycle time by taking the LCM of the axis cycle times."""
    x_cycle = find_cycle_length(
        moons, lambda m: (m.moon_id, m.position[0], m.velocity[0])
    )
    y_cycle = find_cycle_length(
        moons, lambda m: (m.moon_id, m.position[1], m.velocity[1])
    )
    z_cycle = find_cycle_length(
        moons, lambda m: (m.moon_id, m.position[2], m.velocity[2])
    )
    print(x_cycle, y_cycle, z_cycle)
    lcm = least_common_multiple(x_cycle, y_cycle, z_cycle)
    return lcm


def main(moons: List[Moon]) -> Tuple[int, int]:
    after_1000_steps = simulate_n_steps(moons, 1000)
    all_moons_total_energy = sum(moon.total_energy for moon in after_1000_steps)

    system_cycle_time = calculate_cycle_time(moons)

    return all_moons_total_energy, system_cycle_time


if __name__ == "__main__":
    moons = parse_input(aoc_common.load_puzzle_input(DAY))
    part_one_solution, part_two_solution = main(moons)

    assert (
        part_one_solution == 12053
    ), "Part one solution doesn't match known-correct answer."

    assert (
        part_two_solution == 320_380_285_873_116
    ), "Part one solution doesn't match known-correct answer."

    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution=part_two_solution,
    )
