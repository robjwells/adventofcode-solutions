#!/usr/bin/env python3
"""Advent of Code 2015, Day 17: No Such Thing as Too Much"""

from itertools import combinations

puzzle_input = [
    43,
    3,
    4,
    10,
    21,
    44,
    4,
    6,
    47,
    41,
    34,
    17,
    17,
    44,
    36,
    31,
    46,
    9,
    27,
    38,
]
puzzle_input.sort()


def brute_force(containers, amount):
    combo_lengths = [
        len(c)
        for i in range(len(containers))
        for c in combinations(containers, i)
        if sum(c) == amount
    ]
    number_combos = len(combo_lengths)
    min_ways = combo_lengths.count(min(combo_lengths))
    return (number_combos, min_ways)


# I got completely stuck on the recursion (it'd been a while!)
# and was helped along by this blog post:
# https://blog.jverkamp.com/2015/12/17/advent-of-code-day-17/
def find_containers(containers, amount):
    if not amount:
        yield []
    elif containers and min(containers) > amount:
        # This is just an early return for lists of containers that
        # can’t possibly work.
        return
    else:
        for idx, container in enumerate(containers):
            if container <= amount:
                for others in find_containers(
                    containers[idx + 1 :], amount - container
                ):
                    yield [container] + others


# This is much faster than brute forcing, about 3 times
def recursive(containers, amount):
    containers.sort()
    container_lengths = [len(c) for c in find_containers(containers, amount)]

    # Part one
    number_combos = len(container_lengths)
    # Part two
    min_ways = container_lengths.count(min(container_lengths))
    return (number_combos, min_ways)


# print(brute_force(puzzle_input, 150))
print(recursive(puzzle_input, 150))
