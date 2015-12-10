#!/usr/local/bin/python3


def load_input():
    with open('../day7_input.txt') as f:
        wires = [line.split(' -> ') for line in f.read().splitlines()]
        wires = {w: s for s, w in wires}
    return wires


def solve(wire):
    signal = wires.get(wire, wire)  # Fallback in case 'wire' is a number
    try:
        return int(signal)
    except:
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


# Part one
wires = load_input()
a_value = solve('a')
print('Signal on wire a:', a_value)


# Part two
wires = load_input()
wires['b'] = a_value
print('Signal on wire a after overriding b:', solve('a'))
