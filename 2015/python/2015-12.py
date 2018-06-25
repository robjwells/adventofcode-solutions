#!/usr/bin/env python3
"""Advent of Code 2015, Day 12: JSAbacusFramework.io"""

import json


def sum_data(d, ignore_red=False):
    total = 0
    if isinstance(d, dict):
        d = d.values()
        if ignore_red and 'red' in d:
            return 0
    for item in d:
        if isinstance(item, int):
            total += item
        elif isinstance(item, (list, dict)):
            total += sum_data(item, ignore_red)
        else:
            continue    # Some other type we’re not interested in
    return total


def sum_json(raw_json, ignore_red=False):
    parsed = json.loads(raw_json)
    return sum_data(parsed, ignore_red=ignore_red)


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


def main(puzzle_input):
    print('Part one:', sum_json(puzzle_input))
    print('Part two:', sum_json(puzzle_input, ignore_red=True))


if __name__ == '__main__':
    with open('../input/2015-12.txt') as json_file:
        json_data = json_file.read()
    main(json_data)
