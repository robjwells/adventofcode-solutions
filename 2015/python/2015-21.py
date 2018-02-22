#!/usr/bin/env python3
"""Advent of Code 2015, Day 21: RPG Simulator 20XX"""

from collections import namedtuple
import itertools

import pytest


Item = namedtuple('Item', ['name', 'cost', 'damage', 'armor'])


def item_combinations(items, combo_range):
    """Return a set of item combinations, allowing no item to be chosen

    `combo_range` is the acceptable lengths of the combinations, with None
    inserted so the length of the combination is always the upper
    limit of the range. For instance:
        [a, b], range(2)    ->      (a), (b), (None)
        [a, b], range(3)    ->      (a, b), (a, None), (b, None),
                                        (None, None)

    You can force an item to be chosen by excluding 0 from the range:
        [a, b], range(1, 2)     ->      (a), (b)
        [a, b], range(1, 3)     ->      (a, b)
        [a, b, c], range(1, 3)  ->      (a, b), (a, c), (b, c)
    """
    if combo_range.start < 0 or combo_range.stop < 0:
        raise ValueError('Range must not be negative')
    elif (combo_range.start == combo_range.stop or
            combo_range.start == 0 and combo_range.stop == 1):
        # Choices are of length zero
        return []

    full_length_combos = []
    if combo_range.start == 0:
        no_choice = [None for _ in range(combo_range.stop - 1)]
        full_length_combos.append(tuple(no_choice))
        combo_range = range(1, combo_range.stop)

    expected_length = combo_range.stop - 1
    for length in combo_range:
        combos = itertools.combinations(items, length)
        if length < expected_length:
            combos = [c + tuple([None] * (expected_length - length))
                      for c in combos]
        full_length_combos.extend(combos)

    return full_length_combos


@pytest.mark.parametrize('items,combo_range,expected', [
    (['a', 'b'], range(1), []),
    (['a', 'b'], range(2), [(None,), ('a',), ('b',)]),
    (['a', 'b'], range(1, 2), [('a',), ('b',)]),
    (['a', 'b'], range(3),
        [(None, None), ('a', None), ('b', None), ('a', 'b')]),
    (['a', 'b'], range(1, 2), [('a',), ('b',)]),
    (['a', 'b'], range(2, 3), [('a', 'b')]),
])
def test_combos(items, combo_range, expected):
    assert item_combinations(items, combo_range) == expected


def test_combos_disallows_negative():
    for r in [range(-2, 2), range(2, -2)]:
        with pytest.raises(ValueError):
            item_combinations([], r)


def main(enemy, weapons, armor, rings):
    pass


if __name__ == '__main__':
    # Puzzle input (boss stats):
    #     Hit Points: 104
    #     Damage: 8
    #     Armor: 1
    boss_stats = (104, 8, 1)

    # Items
    # name, cost, damage, armor
    weapons = [Item(*t) for t in [
        ('Dagger',      8,  4,  0),
        ('Shortsword', 10,  5,  0),
        ('Warhammer',  25,  6,  0),
        ('Longsword',  40,  7,  0),
        ('Greataxe',   74,  8,  0),
        ]]

    armor = [Item(*t) for t in [
        ('Leather',    13,  0,  1),
        ('Chainmail',  31,  0,  2),
        ('Splintmail', 53,  0,  3),
        ('Bandedmail', 75,  0,  4),
        ('Platemail', 102,  0,  5),
        ]]

    rings = [Item(*t) for t in [
        ('Damage +1',  25,  1,  0),
        ('Damage +2',  50,  2,  0),
        ('Damage +3', 100,  3,  0),
        ('Defense +1', 20,  0,  1),
        ('Defense +2', 40,  0,  2),
        ('Defense +3', 80,  0,  3),
        ]]

    main(boss_stats, weapons, armor, rings)
