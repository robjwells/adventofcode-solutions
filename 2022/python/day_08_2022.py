from __future__ import annotations

from util import read_input

Grid = list[list[int]]


def parse(s: str) -> Grid:
    return [[int(c) for c in line] for line in s.splitlines()]


def solve_part_one(grid: Grid) -> int:
    forward = range(len(grid))
    backward = range(len(grid) - 1, -1, -1)
    visibility = [[0 for _ in forward] for _ in forward]

    def f(
        grid: Grid, vg: Grid, outer: range, inner: range, row_major: bool
    ) -> None:
        for row in outer:
            previous_highest = -1
            for col in inner:
                val = grid[row][col] if row_major else grid[col][row]
                if val > previous_highest:
                    if row_major:
                        vg[row][col] += 1
                    else:
                        vg[col][row] += 1
                previous_highest = max(previous_highest, val)

    f(grid, visibility, forward, forward, True)
    f(grid, visibility, forward, backward, True)
    f(grid, visibility, forward, forward, False)
    f(grid, visibility, forward, backward, False)

    pg = ["".join([str(v) for v in row]) for row in grid]
    pvg = ["".join([str(v) if v else " " for v in row]) for row in visibility]
    print(*pg, sep="\n")
    print()
    print(*pvg, sep="\n")
    return sum([
        len([v for v in row if v > 0])
        for row in visibility
    ])


def solve_part_two(root: Grid) -> int:
    ...


def main() -> None:
    puzzle_input = read_input(8)
    grid = parse(puzzle_input)

    part_one = solve_part_one(grid)
    assert part_one == 1_782
    print(f"Part one: {part_one:,}")

    # part_two = solve_part_two(grid)
    # print(f"Part two: {part_two:,}")


if __name__ == "__main__":
    main()


SAMPLE_INPUT = """\
30373
25512
65332
33549
35390
"""


def test_solve_part_one_sample_input() -> None:
    assert solve_part_one(parse(SAMPLE_INPUT)) == 21


# def test_solve_part_two_sample_input() -> None:
#     assert solve_part_two(parse(SAMPLE_INPUT)) == 24933642
