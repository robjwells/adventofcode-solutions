#!/usr/bin/env python3
"""Advent of Code 2015, Day 7: Some Assembly Required"""


def solve(wire):
    signal = wires.get(wire, wire)  # Fallback in case 'wire' is a number
    try:
        return int(signal)
    except ValueError:
        pass

    parts = signal.split()

    if len(parts) == 1:
        result = solve(parts[0])    # Refers to another wire
    if len(parts) == 2:     # NOT
        result = 65535 - solve(parts[1])    # Invert 16-bit unsigned integer
    elif len(parts) == 3:
        left, op, right = parts
        if op == 'AND':
            result = solve(left) & solve(right)
        elif op == 'OR':
            result = solve(left) | solve(right)
        elif op == 'LSHIFT':
            result = solve(left) << int(right)
        elif op == 'RSHIFT':
            result = solve(left) >> int(right)

    wires[wire] = result
    return wires[wire]


if __name__ == '__main__':
    with open('../input/2015-07.txt') as f:
        puzzle_input = [line.split(' -> ') for line in f.read().splitlines()]
        puzzle_input = {w: s for s, w in puzzle_input}

    # Part one - expecting 16076
    wires = puzzle_input.copy()
    a_value = solve('a')
    print('Signal on wire a:', a_value)

    # Part two - expecting 2797
    wires = puzzle_input.copy()
    wires['b'] = a_value
    print('Signal on wire a after overriding b:', solve('a'))
