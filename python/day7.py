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
        result = solve(parts[0])
    if len(parts) == 2:     # NOT
        result = 65535 - solve(parts[1])
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
print(solve('a'))


# Part two
wires = load_input()
wires['b'] = 16076
print(solve('a'))
