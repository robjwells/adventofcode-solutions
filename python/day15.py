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
