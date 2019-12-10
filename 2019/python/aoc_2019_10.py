"""Day 10: Monitoring Station"""
from math import gcd
from typing import List, NamedTuple, Set

import pytest

import aoc_common

DAY = 10


class Location(NamedTuple):
    across: int
    down: int


class Direction(NamedTuple):
    across: int
    down: int


class AsteroidObservation(NamedTuple):
    asteroid: Location
    asteroids_visible: int


class ParsedGrid(NamedTuple):
    width: int
    height: int
    asteroids: Set[Location]


def parse_grid(grid: str) -> ParsedGrid:
    grid_rows = grid.strip().splitlines()
    height = len(grid_rows)
    width = len(grid_rows[0])
    asteroids = {
        Location(across, down)
        for down in range(height)
        for across in range(width)
        if grid_rows[down][across] == "#"
    }
    return ParsedGrid(width, height, asteroids)


def reduce_direction(unsimplified: Direction) -> Direction:
    divisor = gcd(abs(unsimplified.across), abs(unsimplified.down))
    return Direction(
        int(unsimplified.across / divisor), int(unsimplified.down / divisor)
    )


def relative_distance(source: Location, dest: Location) -> Direction:
    return Direction(source.across - dest.across, source.down - dest.down)


def find_best_spot_for_monitoring_station(grid: ParsedGrid) -> AsteroidObservation:
    observations: List[AsteroidObservation] = []
    for this in grid.asteroids:
        directions = {
            reduce_direction(relative_distance(this, other))
            for other in grid.asteroids
            if other != this
        }
        observations.append(AsteroidObservation(this, len(directions)))
    return max(observations, key=lambda ao: ao.asteroids_visible)


@pytest.mark.parametrize(
    "grid_string,expected_observation",
    [
        # fmt: off
    (
"""\
.#..#
.....
#####
....#
...##
""", AsteroidObservation(Location(3, 4), 8)
    ),
    (
"""\
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
""", AsteroidObservation(Location(5, 8), 33)
    ),
    (
"""\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
""", AsteroidObservation(Location(1, 2), 35)
    ),
    (
"""\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
""", AsteroidObservation(Location(6, 3), 41)
    ),
    (
"""\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
""", AsteroidObservation(Location(11, 13), 210)
    )
        # fmt: on
    ],
)
def test_find_best_spot_for_monitoring_station(
    grid_string: str, expected_observation: int
) -> None:
    parsed = parse_grid(grid_string)
    assert find_best_spot_for_monitoring_station(parsed) == expected_observation


def main(grid: ParsedGrid) -> int:
    return find_best_spot_for_monitoring_station(grid).asteroids_visible


if __name__ == "__main__":
    grid = parse_grid(aoc_common.load_puzzle_input(DAY))
    part_one_solution = main(grid)
    assert (
        part_one_solution == 276
    ), "Part one solution doesn't match known-correct answer."
    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
