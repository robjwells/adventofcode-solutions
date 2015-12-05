#!/usr/local/bin/python3

with open('day2_input.txt') as f:
    instructions = f.read().rstrip()


def surface_area(l, w, h):
    return (2 * l * w) + (2 * w * h) + (2 * h * l)


def smallest_side(l, w, h):
    return min([(l * w), (w * h), (h * l)])


total = 0

for line in instructions.splitlines():
    l, w, h = map(int, line.split('x'))
    total += surface_area(l, w, h)
    total += smallest_side(l, w, h)
else:
    print('wrapping paper:', total)

ribbon = 0

for line in instructions.splitlines():
    l, w, h = map(int, line.split('x'))
    s1, s2, s3 = sorted([l, w, h])
    ribbon += 2 * s1 + 2 * s2
    ribbon += l * w * h  # bow
else:
    print('ribbon:', ribbon)
