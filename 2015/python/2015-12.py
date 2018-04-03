#!/usr/bin/env python3
"""Advent of Code 2015, Day 12: JSAbacusFramework.io"""

import json

import pathlib

input_file = pathlib.Path(__file__).parent.parent.joinpath('day12_input.txt')


def sum_data(d):
    total = 0
    if isinstance(d, dict):
        d = d.values()
        if 'red' in d:
            return 0
    for item in d:
        if isinstance(item, int):
            total += item
        elif isinstance(item, (list, dict)):
            total += sum_data(item)
        else:
            continue    # Some other type we’re not interested in
    return total


def sum_json(raw_json):
    parsed = json.loads(raw_json)
    return sum_data(parsed)


def test_simple():
    assert sum_json('[1,2,3]') == 6
    assert sum_json('{"a":2,"b":4}') == 6


def test_nested():
    assert sum_json('[[[3]]]') == 3
    assert sum_json('{"a":{"b":4},"c":-1}') == 3


def test_mixed():
    assert sum_json('{"a":[-1,1]}') == 0
    assert sum_json('[-1,{"a":1}]') == 0


def test_empty():
    assert sum_json('[]') == 0
    assert sum_json('{}') == 0


if __name__ == '__main__':
    with open(input_file) as json_file:
        json_data = json_file.read()
    print(sum_json(json_data))
