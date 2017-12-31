#!/usr/local/bin/python3

from ast import literal_eval    # Safer than plain eval

with open('../input/2015-08.txt') as f:
    strings = f.read().splitlines()

# Part one
total_symbols = sum(len(s) for s in strings)
total_chars = sum(len(literal_eval(s)) for s in strings)
print('Part one:', total_symbols - total_chars)

# Part two
# Instead of actually escaping the string using re.escape and measuring it,
# you can work out the number of extra characters needed by counting the
# characters that would need escaping. Add 2 for the extra surrounding quote
# marks mentioned in the problem description.
total_extra_chars = sum(s.count('"') + s.count('\\') + 2 for s in strings)
print('Part two:', total_extra_chars)
