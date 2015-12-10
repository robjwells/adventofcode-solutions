#!/usr/local/bin/python3

from ast import literal_eval    # safer than plain eval
import re

with open('../day8_input.txt') as f:
    strings = f.read().splitlines()

# Part one
total_symbols = sum(len(s) for s in strings)
total_chars = sum(len(literal_eval(s)) for s in strings)
print('Part one:', total_symbols - total_chars)

# Part two
newly_encoded_chars = sum(
    len(re.escape(s)) + 2   # Add 2 for the (missing) surrounding quotes
    for s in strings)
print('Part two:', newly_encoded_chars - total_symbols)
