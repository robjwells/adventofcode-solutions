#!/usr/local/bin/python3

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
