#!/usr/bin/env python3
"""Advent of Code 2015, Day 8: Matchsticks"""

import re

import pytest


def parse_for_length(string):
    """Return the length of string once escapes and quotes are parsed

    Recognised escapes are the following:
        \\      Escaped backslash
        \"      Escaped quote
        \x27    Hex character escape
    """
    literal_length = len(string)
    # Account for and trim surrounding double quotes
    # (Trimming allows for counting \" sequences accurately.)
    length = literal_length - 2
    string = string[1:-1]
    # Escaped backslashes
    length -= string.count(r'\\')
    # Escaped quotes
    length -= string.count(r'\"')
    # Hex character escapes
    # (Times 3 because we want to reduce 4 chars to 1)
    hex_regex = re.compile(r'\\x[0-9a-f]{2}', flags=re.I)
    length -= len(re.findall(hex_regex, string)) * 3
    return length


@pytest.mark.parametrize('string,length', [
    (r'""', 0),
    (r'"abc"', 3),
    (r'"aaa\"aaa"', 7),
    (r'"\x27"', 1),
    (r'"\\"', 1),
    ])
def test_parse_for_length(string, length):
    """parse_for_length returns expected lengths for known strings"""
    assert parse_for_length(string) == length


def extra_chars_to_encode(string):
    """Return the additional chars needed to escape string

    For example:
        ""      becomes     "\"\""  ie two escaped quotes with
                                    additional surrounding quotes

        "abc"               "\"abc\""
        "aaa\"aaa"          "\"abc\\\"aaa\""
        "\x27"              "\"\\x27\""
    """
    # Start with the additional enclosing quotes
    total_extra = 2
    # Then backlashes needed for existing quotes
    total_extra += string.count('"')
    # Then backlashes for backslashes
    total_extra += string.count('\\')
    return total_extra


@pytest.mark.parametrize('string,extra_chars', [
    (r'""', 4),
    (r'"abc"', 4),
    (r'"aaa\"aaa"', 6),
    (r'"\x27"', 5),
    (r'"\\"', 6),
    ])
def test_extra_chars_to_encode(string, extra_chars):
    """extra_chars… returns expected additional characters"""
    assert extra_chars_to_encode(string) == extra_chars


def main(puzzle_input):
    # Part one
    total_symbols = sum(len(s) for s in strings)
    parsed_total = sum(parse_for_length(s) for s in strings)
    print('Part one:', total_symbols - parsed_total)

    # Part two
    total_extra_chars = sum(extra_chars_to_encode(s) for s in strings)
    print('Part two:', total_extra_chars)


if __name__ == '__main__':
    with open('../input/2015-08.txt') as f:
        strings = f.read().splitlines()
    main(strings)
