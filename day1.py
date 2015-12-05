#!/usr/local/bin/python3

with open('day1_input.txt') as f:
    instructions = f.read().rstrip()

instruction_values = {'(': 1, ')': -1}

print('final floor:', sum(instruction_values[char] for char in instructions))


# Part two

floor = 0

for idx, char in enumerate(instructions, start=1):
    floor += instruction_values[char]
    if floor == -1:
        print('first basement instruction:', idx)
        break
