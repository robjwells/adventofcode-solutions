"""Day 10: Monitoring Station"""
from collections import defaultdict, deque
from functools import partial
from math import atan2, gcd, sqrt
from typing import DefaultDict, Deque, Iterable, Iterator, List, NamedTuple, Set, Tuple

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
    return Direction(dest.across - source.across, dest.down - source.down)


def basic_direction(source: Location, dest: Location) -> Direction:
    return reduce_direction(relative_distance(source, dest))


def find_best_spot_for_monitoring_station(grid: ParsedGrid) -> AsteroidObservation:
    observations: List[AsteroidObservation] = []
    for this in grid.asteroids:
        directions = {
            basic_direction(this, other) for other in grid.asteroids if other != this
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


def distance(a: Location, b: Location) -> float:
    return sqrt((b.across - a.across) ** 2 + (b.down - a.down) ** 2)


def direction_and_distance(
    first: Location, second: Location
) -> Tuple[Direction, float]:
    return (basic_direction(first, second), distance(first, second))


def clockwise_asteroid_queues(
    centre: Location, asteroids: Iterable[Location]
) -> List[Deque[Location]]:
    direction_and_distance_from_centre = partial(direction_and_distance, centre)

    # Build dictionary of asteroids by location after pre-sorting the asteroids
    # by direction and then distance order. Pre-sorting avoids having to sort
    # the queues individually later.
    direction_queues: DefaultDict[Direction, Deque[Location]] = defaultdict(deque)
    for asteroid in sorted(asteroids, key=direction_and_distance_from_centre):
        direction = basic_direction(centre, asteroid)
        direction_queues[direction].append(asteroid)

    # Sort the queues (not their elements) by the angle of their basic
    # direction (the key) so that the asteroids can be iterated in a
    # circular manner.
    #
    # We deliberately misprovide the arguments to atan2 to adjust the ray
    # from which the angle is calculated, and the direction in which it is
    # calculated.
    #
    # `-atan2(x, y)` would usually give an anti-clockwise order from
    # the 6 position, but as our vertical axis is inverted it gives the
    # equivalent of `-atan2(x, -y)`, which is a clockwise traversal
    # from the 12 position.
    sorted_by_angle = sorted(
        direction_queues.items(), key=lambda item: -atan2(item[0].across, item[0].down)
    )
    return [queue for direction, queue in sorted_by_angle]


def destroy_asteroids_in_order(
    laser: Location, asteroids: Iterable[Location]
) -> Iterator[Location]:
    clockwise_order_from_above = clockwise_asteroid_queues(laser, asteroids)
    while clockwise_order_from_above:
        for queue in clockwise_order_from_above:
            try:
                # Closer asteroids are at the front of the queue,
                # so popleft rather than just pop.
                yield queue.popleft()
            except IndexError:
                # Queue is exhausted, so remove it.
                clockwise_order_from_above.remove(queue)


def find_nth_asteroid_destroyed(
    laser: Location, asteroids: Iterable[Location], n: int = 200
) -> Location:
    destroyed_gen = destroy_asteroids_in_order(laser, asteroids)
    for number, destroyed_asteroid in enumerate(destroyed_gen, start=1):
        if number == n:
            return destroyed_asteroid
    raise ValueError(f"Too few asteroids given to find number {n} destroyed.")


def test_asteroid_destruction() -> None:
    grid_string = """\
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
"""
    grid = parse_grid(grid_string)
    laser = find_best_spot_for_monitoring_station(grid).asteroid
    asteroids = grid.asteroids - {laser}
    destruction_order = list(destroy_asteroids_in_order(laser, asteroids))
    expected = (
        (1, (11, 12)),
        (2, (12, 1)),
        (3, (12, 2)),
        (10, (12, 8)),
        (20, (16, 0)),
        (50, (16, 9)),
        (100, (10, 16)),
        (199, (9, 6)),
        (200, (8, 2)),
        (201, (10, 9)),
        (299, (11, 1)),
    )
    filtered = [destruction_order[n - 1] for n, _ in expected]
    locations = [Location(*coords) for _, coords in expected]
    assert locations == filtered


def main(grid: ParsedGrid) -> Tuple[int, int]:
    best_spot = find_best_spot_for_monitoring_station(grid)
    asteroid_200 = find_nth_asteroid_destroyed(
        best_spot.asteroid, grid.asteroids - {best_spot.asteroid}
    )
    asteroid_200_coord = asteroid_200.across * 100 + asteroid_200.down
    return best_spot.asteroids_visible, asteroid_200_coord


if __name__ == "__main__":
    grid = parse_grid(aoc_common.load_puzzle_input(DAY))
    part_one_solution, part_two_solution = main(grid)
    assert (
        part_one_solution == 276
    ), "Part one solution doesn't match known-correct answer."
    assert (
        part_two_solution == 1321
    ), "Part two solution doesn't match known-correct answer."
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution=part_two_solution,
    )
