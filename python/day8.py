#!/usr/local/bin/python3

import re

with open('../day8_input.txt') as f:
    strings = f.read().splitlines()

# Part one
total_symbols = sum(len(s) for s in strings)
total_chars = sum(len(eval(s)) for s in strings)
print(total_symbols - total_chars)

# Part two
newly_encoded_chars = sum(len(re.escape(s)) + 2 for s in strings)
print(newly_encoded_chars - total_symbols)
