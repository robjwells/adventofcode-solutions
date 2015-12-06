#!/usr/local/bin/python3

with open('../day2_input.txt') as f:
    instructions = [[int(i) for i in line.split('x')]
                    for line in f.read().splitlines()]


def surface_area(l, w, h):
    return (2 * l * w) + (2 * w * h) + (2 * h * l)


def smallest_side(l, w, h):
    return min([(l * w), (w * h), (h * l)])


wrapping_paper = 0

for dimensions in instructions:
    wrapping_paper += surface_area(*dimensions)
    wrapping_paper += smallest_side(*dimensions)  # slack

print('wrapping paper:', wrapping_paper)


# Part two

ribbon = 0

for dimensions in instructions:
    s1, s2, s3 = sorted(dimensions)
    ribbon += 2 * s1 + 2 * s2
    ribbon += s1 * s2 * s3  # bow

print('ribbon:', ribbon)
