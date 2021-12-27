#!/usr/bin/env python3
"""Advent of Code 2015, Day 7: Some Assembly Required"""

import aoc


class Circuit:
    """A set of wires connected with bitwise logic gates"""

    def __init__(self, instructions):
        """Parse instructions into a circuit layout

        instructions should be the text from the puzzle input without
        any processing.

        The wire signals are not 'solved' at this stage.
        """
        wires = [line.split(" -> ") for line in instructions.splitlines()]
        self._wires = {w: s for s, w in wires}

    def _solve(self, wire):
        """Return the signal provided to a wire

        The signal is discovered by recursively solving the circuit,
        according to the instructions provided in init.
        """
        value = self._wires.get(wire, wire)  # In case wire is an int
        try:
            number = int(value)
            # Just assigning is fairly quick instead of checking whether
            # the value in the dictionary is still a string, but don't
            # add extra keys that are just ints referencing themselves
            if wire != number:
                self._wires[wire] = number
            return number
        except ValueError:
            # Wire needs solving
            pass

        parts = value.split()
        if len(parts) == 1:
            result = self._solve(*parts)  # Another wire
        if len(parts) == 2:
            # "NOT": Invert 16-bit unsigned integer
            result = 65535 - self._solve(parts[1])
        elif len(parts) == 3:
            left, op, right = parts
            if op == "AND":
                result = self._solve(left) & self._solve(right)
            elif op == "OR":
                result = self._solve(left) | self._solve(right)
            elif op == "LSHIFT":
                result = self._solve(left) << int(right)
            elif op == "RSHIFT":
                result = self._solve(left) >> int(right)

        self._wires[wire] = result
        return self._wires[wire]

    def build(self):
        """Contruct the circuit so each wire has a signal"""
        for wire in list(self._wires):
            # list used to avoid 'dict changed size' error
            if not isinstance(self._wires[wire], int):
                self._solve(wire)

    def __getitem__(self, key):
        """Allow indexing on wire identifier"""
        return self._solve(key)

    def __setitem__(self, key, value):
        self._wires[key] = value


def test_circuit():
    """Test Circuit with some example instructions"""
    instructions = """\
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""
    expected = dict(
        [
            ("d", 72),
            ("e", 507),
            ("f", 492),
            ("g", 114),
            ("h", 65412),
            ("i", 65079),
            ("x", 123),
            ("y", 456),
        ]
    )
    circuit = Circuit(instructions)
    circuit.build()  # Ensure each wire has a value
    assert circuit._wires == expected


def main(puzzle_input):
    first = Circuit(puzzle_input)
    a_value = first["a"]
    print("Part one, signal on wire a:", a_value)

    second = Circuit(puzzle_input)
    second["b"] = a_value
    print("Part two, signal on wire a after overriding b:", second["a"])


if __name__ == "__main__":
    puzzle_input = aoc.load_puzzle_input(2015, 7)
    main(puzzle_input)
