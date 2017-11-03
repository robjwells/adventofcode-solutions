#!/usr/local/bin/python3

from itertools import permutations
import pathlib
import re

input_file = pathlib.Path(__file__).parent.parent.joinpath('day13_input.txt')

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
    """Return a list of all permutations of guests with reversals removed

    Comparing the first and last elements works because at the point
    this starts to fail, the reverse permutation is already stored in
    the list.

    You can verify this by building a set and only storing elements whose
    reversals aren’t already present in the set. That set contains the
    same elements as building one in this manner.
    """
    perms = permutations(guests)
    return [p for p in perms if p[0] < p[-1]]


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
        '^(\w)\w+ \w+ (gain|lose) (\d+)[ a-z]+([A-Z])[a-z]+\.$'
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


if __name__ == '__main__':
    with open(input_file) as f:
        happiness_dict = parse_happiness(f.read())

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
