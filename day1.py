#!/usr/local/bin/python3

with open('day1_input.txt') as f:
    instructions = f.read().rstrip()

floor = 0

for char in instructions:
    if char == '(':
        floor += 1
    else:
        floor -= 1

print('final floor:', floor)


# Part two


floor = 0

for idx, char in enumerate(instructions, start=1):
    if char == '(':
        floor += 1
    else:
        floor -= 1
    if floor == -1:
        print('first basement instruction:', idx)
        break
