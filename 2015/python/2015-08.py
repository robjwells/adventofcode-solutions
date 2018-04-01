#!/usr/local/bin/python3

import re


def parse_for_length(string):
    """Return the length of string once escapes are parsed"""
    literal_length = len(string)
    # Account for and trim surrounding double quotes
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


def test_parse_for_length():
    """parse_for_length returns expected lengths for known strings"""
    assert parse_for_length(r'""') == 0
    assert parse_for_length(r'"abc"') == 3
    assert parse_for_length(r'"aaa\"aaa"') == 7
    assert parse_for_length(r'"\x27"') == 1
    assert parse_for_length(r'"\\"') == 1


def extra_chars_to_encode(string):
    """Return the additional chars needed to escape string"""
    pass


def test_extra_chars_to_encode():
    pass


def main(puzzle_input):
    # Part one
    total_symbols = sum(len(s) for s in strings)
    parsed_total = sum(parse_for_length(s) for s in strings)
    print('Part one:', total_symbols - parsed_total)

    # Part two
    # Instead of actually escaping the string using re.escape and measuring it,
    # you can work out the number of extra characters needed by counting the
    # characters that would need escaping. Add 1 for the extra surrounding
    # quote marks mentioned in the problem description.
    total_extra_chars = sum(s.count('"') + s.count('\\') + 1 for s in strings)
    print('Part two:', total_extra_chars)


if __name__ == '__main__':
    with open('../input/2015-08.txt') as f:
        strings = f.read().splitlines()
    main(strings)
