#!/usr/local/bin/python3

with open('../day6_input.txt') as f:
    lines = [line.rsplit(maxsplit=3) for line in f.read().splitlines()]

# Part one
# lights = [[False for i in range(1000)] for j in range(1000)]

# Part two
lights = [[0 for i in range(1000)] for j in range(1000)]

for instruction, start, _, end in lines:
    start_x, start_y = [int(part) for part in start.split(',')]
    end_x, end_y = [int(part) for part in end.split(',')]

    if instruction == 'turn on':
        # func = lambda state: True         # Part one
        func = lambda state: state + 1      # Part two
    elif instruction == 'turn off':
        # func = lambda state: False        # Part one
        func = lambda state: state if state == 0 else state - 1  # Part two
    elif instruction == 'toggle':
        # func = lambda state: not state    # Part one
        func = lambda state: state + 2      # Part two

    for col in range(start_x, end_x + 1):
        row_part = slice(start_y, end_y + 1)
        lights[col][row_part] = map(func, lights[col][row_part])


print(sum(sum(col) for col in lights))
