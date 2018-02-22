#!/usr/bin/env python3
"""Advent of Code 2015, Day 21: RPG Simulator 20XX"""

import itertools

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


def main(puzzle_input):
    pass


if __name__ == '__main__':
    # Puzzle input (boss stats):
    #     Hit Points: 104
    #     Damage: 8
    #     Armor: 1
    main()
