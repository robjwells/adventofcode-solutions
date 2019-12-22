"""Day 17: Set and Forget"""

from enum import Enum
from itertools import chain, islice, repeat
from typing import Any, Dict, Iterable, List, Optional, Tuple

import aoc_common
from intcode import IntCode, parse_program

DAY = 17


SCAFFOLD = "#"
EMPTY = "."
ROBOT_CHARS = ("^", "v", "<", ">")

SENTINEL = object()


def chunked(iterable: Iterable[Any], count: int, *, fill: Any = SENTINEL):
    """Yield count-long chunks from iterable.

    If the length of the iterable is not a multiple of count,
    the final chunk will be short, unless `fill` is provided
    as a keyword argument, in which case the final chunk will
    be filled with the given value.
    """
    iterator = iter(iterable)
    should_fill = fill is not SENTINEL
    while True:
        chunk = list(islice(iterator, count))
        if not chunk:
            return
        if len(chunk) < count and should_fill:
            chunk += repeat(fill, count - len(chunk))
        yield chunk


def create_grid(ascii: Iterable[int]) -> Dict[Tuple[int, int], str]:
    grid: Dict[Tuple[int, int], str] = {}
    x = y = 0
    for tile in map(chr, ascii):
        if tile == "\n":
            y += 1
            x = 0
            continue
        grid[(x, y)] = tile
        x += 1
    return grid


def find_intersections(grid: Dict[Tuple[int, int], str]) -> List[Tuple[int, int]]:
    max_x = max(x for x, y in grid)
    max_y = max(y for x, y in grid)
    return [
        (x, y)
        for y in range(1, max_y)
        for x in range(1, max_x)
        if all(
            grid[pos] != "."
            for pos in [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        )
    ]


def print_grid(
    grid: Dict[Tuple[int, int], str],
    intersections: Optional[Iterable[Tuple[int, int]]] = None,
) -> None:
    if intersections is None:
        intersections = []
    line_length = max(x for x, y in grid) + 1

    for line in chunked(grid.items(), count=line_length):
        for pos, tile in line:
            if pos in intersections:
                print("O", end="")
            else:
                print(tile, end="")
        print()


def parse_ascii_instructions(text: str) -> List[int]:
    output = []
    for instruction in text.split():
        for char in instruction:
            output.append(ord(char))
        output.append(44)
    if output[-1] == 44:
        output.pop()  # Remove trailing comma
    output.append(10)
    return output


def main(program: List[int]) -> Tuple[int, int]:
    computer = IntCode(program)
    computer.run_until_halt()
    grid = create_grid(computer.output_queue)
    intersections = find_intersections(grid)
    print_grid(grid, intersections)
    alignment_params = [x * y for x, y in intersections]

    instructions = {
        routine_name: parse_ascii_instructions(instructions)
        for routine_name, instructions in [
            ("A", "L 12 L 6 L 8 R 6"),
            ("B", "L 8 L 8 R 4 R 6 R 6"),
            ("C", "L 12 R 6 L 8"),
        ]
    }

    main_program = parse_ascii_instructions("A B A B C C B A B C")

    patched = program
    patched[0] = 2
    robot = IntCode(program)
    for ascii_code in chain(main_program, *instructions.values()):
        robot.pass_input(ascii_code)
    robot.pass_input(ord("n"))
    robot.pass_input(10)
    robot.run_until_halt()
    for codepoint in robot.output_queue:
        if codepoint < 128:
            print(chr(codepoint), end="")
        else:
            print(codepoint)

    space_dust = robot.output_queue.pop()

    return sum(alignment_params), space_dust


if __name__ == "__main__":
    program = parse_program(aoc_common.load_puzzle_input(DAY))
    part_one_solution, part_two_solution = main(program)
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution=part_two_solution,
    )
