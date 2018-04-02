#!/usr/local/bin/python3

import pytest


puzzle_input = 1113122113


def parse_input(number):
    char, *text = str(number)
    count = 1
    output = ''
    for new_char in text:
        if new_char == char:
            count += 1
        else:
            output += str(count) + char
            char = new_char
            count = 1
    else:
        # This is needed to ensure final digit is accounted for
        output += str(count) + char
    return int(output)


@pytest.mark.parametrize('start,finish', [
    (1, 11),
    (11, 21),
    (21, 1211),
    (211, 1221),
    (1211, 111221),
    (111221, 312211),
    ])
def test_parse_input(start, finish):
    assert parse_input(start) == finish


if __name__ == '__main__':
    for x in range(50):
        if x == 40:
            print(len(puzzle_input))
        puzzle_input = parse_input(puzzle_input)
    print(len(puzzle_input))
