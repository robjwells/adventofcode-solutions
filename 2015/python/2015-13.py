#!/usr/bin/env python3
"""Advent of Code 2015, Day 13: Knights of the Dinner Table"""

from itertools import permutations
import re

import pytest


SAMPLE_INPUT = '''\
Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.
'''


def unique_seating_permutations(guests):
    """Yield unique circular permutations of guests """
    if len(guests) < 3:
        # Only one plan for groups of three or less
        yield guests
        return

    def pair(*args):
        return tuple(sorted(args))

    perms = permutations(guests)
    seen_uniques = set()
    for p in perms:
        char_pairs = {pair(c1, c2) for c1, c2 in zip(p, p[1:])}
        char_pairs.add(pair(p[0], p[-1]))
        if char_pairs not in seen_uniques:
            yield p
            seen_uniques.add(frozenset(char_pairs))


def neighbours(guest, plan):
    """Return guests’s adjacent neighbours in plan

    Guests at one end of the plan are considered to be sitting next
    to the guest at the opposite end.
    """
    g_index = plan.index(guest)
    left = plan[g_index - 1]
    right = plan[(g_index + 1) % len(plan)]  # Wrap around to zero
    return (left, right)


def parse_happiness(text):
    """Parse the instructions and return a dict of happiness relations"""
    regex = re.compile(
        r'^(\w)\w+ \w+ (gain|lose) (\d+)[ a-z]+([A-Z])[a-z]+\.$'
    )
    happiness_dict = dict()
    for line in text.splitlines():
        match = regex.match(line)
        person, change, amount, neighbour = match.groups()
        amount = int(amount)
        if change == 'lose':
            amount = -amount
        if person not in happiness_dict:
            happiness_dict[person] = dict()
        happiness_dict[person][neighbour] = amount
    return happiness_dict


def sum_happiness(happiness_dict, plan):
    """Sum the happiness change of the seating plan"""
    total = 0
    for guest in plan:
        left, right = neighbours(guest, plan)
        total += happiness_dict[guest][left]
        total += happiness_dict[guest][right]
    return total


def find_best_plan(happiness_dict):
    best_happiness = 0
    best_plan = None
    perms = unique_seating_permutations(happiness_dict.keys())
    for plan in perms:
        happiness_change = sum_happiness(happiness_dict, plan)
        if happiness_change > best_happiness:
            best_happiness = happiness_change
            best_plan = plan
    return (best_happiness, best_plan)


def test_parse():
    expected = dict(
        A=dict(B=54, C=-79, D=-2),
        B=dict(A=83, C=-7, D=-63),
        C=dict(A=-62, B=60, D=55),
        D=dict(A=46, B=-7, C=41))
    assert parse_happiness(SAMPLE_INPUT) == expected


def test_sum_happiness():
    happiness_dict = parse_happiness(SAMPLE_INPUT)
    assert sum_happiness(happiness_dict, 'ABCD') == 330


def test_find_known_best_plan_for_example():
    """find_best_plan returns ABCD for the sample scenario"""
    happiness_dict = parse_happiness(SAMPLE_INPUT)
    expected = (330, tuple('ABCD'))
    assert find_best_plan(happiness_dict) == expected


@pytest.mark.parametrize('guests', ['A', 'AB', 'ABC'])
def test_unique_seat_plans_only_one_plan(guests):
    """unique_seating_permutations gives expected number of plans """
    assert len(list(unique_seating_permutations(guests))) == 1


@pytest.mark.parametrize('plan', ['ABCD', 'ABCDE', 'ABCDEF'])
def test_unique_plans_are_unique(plan):
    """unique_seating_permutations returns only unique plans"""
    plan_pairs_set = set()
    for char_tuple in unique_seating_permutations(plan):
        pair_set = {''.join(sorted([c1, c2]))
                    for c1, c2 in zip(char_tuple, char_tuple[1:])}
        pair_set.add(''.join(sorted([char_tuple[0], char_tuple[-1]])))
        assert pair_set not in plan_pairs_set
        plan_pairs_set.add(frozenset(pair_set))


def main(puzzle_input):
    happiness_dict = parse_happiness(puzzle_input)

    # Part one
    p1_change, p1_plan = find_best_plan(happiness_dict)
    print(f'Part one: {p1_change}, {"".join(p1_plan)}')

    # Part two
    # Add myself to happiness dict, with 0 change
    guests_only = list(happiness_dict.keys())
    happiness_dict['Z'] = dict()
    for g in guests_only:
        happiness_dict[g]['Z'] = 0
        happiness_dict['Z'][g] = 0

    p2_change, p2_plan = find_best_plan(happiness_dict)
    print(f'Part two: {p2_change}, {"".join(p2_plan)}')


if __name__ == '__main__':
    with open('../input/2015-13.txt') as f:
        puzzle_input = f.read()
    main(puzzle_input)
