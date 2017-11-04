#!/usr/local/bin/python3

from functools import reduce
import operator
import pathlib

input_file = pathlib.Path(__file__).parent.parent.joinpath('day15_input.txt')


def parse_input(text):
    parsed = dict()
    for line in text.splitlines():
        ingredient, qualities = line.split(': ', maxsplit=1)
        parsed[ingredient] = dict()
        for qual_pair in qualities.split(', '):
            quality, magnitude = qual_pair.split()
            parsed[ingredient][quality] = int(magnitude)
    return parsed


def test_parse():
    sample_input = '''\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''
    expected = dict(
        Butterscotch=dict(
            capacity=-1, durability=-2, flavor=6, texture=3, calories=8),
        Cinnamon=dict(
            capacity=2, durability=3, flavor=-2, texture=-1, calories=3))
    assert parse_input(sample_input) == expected


def cookie_score(recipe, ingredient_dict, ignore_calories=True):
    qual_scores = [
        [amount * magnitude
            for quality, magnitude in ingredient_dict[ingredient].items()
            if quality != 'calories']
        for ingredient, amount in recipe]

    qual_totals = map(sum, zip(*qual_scores))
    # Set negative numbers to zero
    qual_totals = map(lambda x: x if x > 0 else 0, qual_totals)
    cookie_score = reduce(operator.mul, qual_totals)
    return cookie_score


def test_score():
    sample_data = dict(
        Butterscotch=dict(
            capacity=-1, durability=-2, flavor=6, texture=3, calories=8),
        Cinnamon=dict(
            capacity=2, durability=3, flavor=-2, texture=-1, calories=3))
    recipe = [('Butterscotch', 44), ('Cinnamon', 56)]
    assert cookie_score(recipe, sample_data) == 62842880


def test_score_zero():
    """Score is zero when any ingredients have negative total"""
    sample_data = dict(
        Butterscotch=dict(
            capacity=-1, durability=-2, flavor=6, texture=3, calories=8),
        Cinnamon=dict(
            capacity=2, durability=3, flavor=-2, texture=-1, calories=3))
    recipe = [('Butterscotch', 100)]
    assert cookie_score(recipe, sample_data) == 0


def add_lists(*lists):
    """Add two lists together without numpy

    For example, given lists:
        [1, 2]  [3, 4]
    The result is:
        [4, 6]

    Lists are sliced to prevent mutation.
    """
    lists = (l[:] for l in lists)
    return list(map(sum, zip(*lists)))


single_changes = (1, -1, 0, 0)
single_change_permutations = set(permutations(single_changes))


# This is more general but slower than the range-based version below
def combinations(length, total):
    """Return a tuple of given length containing integers with sum total"""
    if length == 1:
        yield (total,)
        return
    for n in range(total + 1):
        x = n
        for y in combinations(length - 1, total - x):
            yield (x,) + y


# This is about twice as fast as the general recursive version above
def combo_four(total):
    """Return a tuple of four integers totalling 100"""
    for i in range(total + 1):
        for j in range(total + 1 - i):
            for k in range(total + 1 - i - j):
                l = total - i - j - k
                yield (i, j, k, l)


def brute_force_cookie(ingredients, teaspoons):
    """Choose best from all possible recipes for number of teaspoons"""
    pass
