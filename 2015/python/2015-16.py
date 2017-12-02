#!/usr/local/bin/python3

import itertools
import operator
import pathlib

input_file = pathlib.Path(__file__).parent.parent.joinpath('day16_input.txt')


def parse_input(text):
    sues = []
    for line in text.splitlines():
        sue_num, details = line.split(': ', maxsplit=1)
        sue_num = int(sue_num.split()[1])
        details = [(a, int(b)) for a, b in
                   [p.split(': ') for p in details.split(', ')]]
        details.append(('matches', 0))
        sues.append((sue_num, dict(details)))
    return sues


def gift_sue():
    text = '''children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
'''
    sue = dict(
        (a, int(b)) for a, b in
        (line.split(': ') for line in text.splitlines()))
    return sue


def sue_search(target_sue, all_sues, truth_functions):
    """Compare values exactly of part one of the puzzle"""
    candidates = [(sue_num, details.copy()) for sue_num, details in all_sues]
    for quality, value in target_sue.items():
        for sue_num, details in candidates:
            if quality in details:
                if truth_functions[quality](details[quality], value):
                    details['matches'] += 1
                else:
                    details['matches'] -= 1
    candidates.sort(key=lambda t: t[1]['matches'])
    return candidates[-1][0]


if __name__ == '__main__':
    all_sues = parse_input(input_file.read_text())
    target_sue = gift_sue()

    truth_functions = dict(zip(target_sue, itertools.repeat(operator.eq)))
    part_one_sue = sue_search(target_sue, all_sues, truth_functions)
    print(f'Part one: Sue {part_one_sue}')

    for k in ('cats', 'trees'):
        truth_functions[k] = operator.gt
    for k in ('pomeranians', 'goldfish'):
        truth_functions[k] = operator.lt
    part_two_sue = sue_search(target_sue, all_sues, truth_functions)
    print(f'Part two: Sue {part_two_sue}')
