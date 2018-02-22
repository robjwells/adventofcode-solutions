#!/usr/bin/env python3
"""Advent of Code 2015, Day 21: RPG Simulator 20XX"""

import pytest


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
    pass


@pytest.mark.parametrize('items,combo_range,expected', [
    (['a', 'b'], range(1), []),
    (['a', 'b'], range(2), [(None,), ('a',), ('b',)]),
    (['a', 'b'], range(1, 2), [('a',), ('b',)]),
    (['a', 'b'], range(3),
        [(None, None), ('a', None), ('b', None), ('a', 'b')]),
    (['a', 'b'], range(1, 3), [('a', 'b')]),
])
def test_combos(items, combo_range, expected):
    assert sorted(item_combinations(items, combo_range)) == sorted(expected)


def main(puzzle_input):
    pass


if __name__ == '__main__':
    # Puzzle input (boss stats):
    #     Hit Points: 104
    #     Damage: 8
    #     Armor: 1
    main()
