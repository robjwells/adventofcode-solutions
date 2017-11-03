#!/usr/local/bin/python3

from itertools import permutations


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
    g_index = plan.index(g)
    left = plan[g_index - 1]
    right = plan[(g_index + 1) % len(plan)]  # Wrap around to zero
    return (left, right)


def parse_happiness(text):
    pass


def test_parse():
    sample_input = '''\
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
    expected = dict(
        A=dict(B=54, C=-79, D=-2),
        B=dict(A=83, C=-7, D=-63),
        C=dict(A=-62, B=60, D=55),
        D=dict(A=46, B=-7, C=41))
    assert parse_happiness(sample_input) == expected


if __name__ == '__main__':
    guests = 'ABC'
    for g in guests:
        print(f'Guest {g}, neighbours: {neighbours(g, guests)}')
