#!/usr/bin/env python3

import pathlib

input_file = pathlib.Path(__file__).parent.parent.joinpath('day18_input.txt')


def parse_input(text):
    return [1 if s == '#' else 0 for s in text.replace('\n', '')]


def test_parse():
    assert parse_input('......\n######') == [0, 0, 0, 0, 0, 0,
                                             1, 1, 1, 1, 1, 1]

