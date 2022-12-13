from util import read_input


def sum_groups(puzzle_text: str) -> list[int]:
    groups: list[list[int]] = [[]]
    for line in puzzle_text.splitlines():
        if not line.strip():
            groups.append([])
            continue
        groups[-1].append(int(line.strip()))
    sums = [sum(g) for g in groups]
    return sums


def solve_part_one(sums: list[int]) -> int:
    return max(sums)


def solve_part_two(sums: list[int]) -> int:
    return sum(sorted(sums)[-3:])


def main() -> None:
    puzzle_input = read_input(1)
    sums = sum_groups(puzzle_input)

    part_one = solve_part_one(sums)
    print(f"Part one: {part_one}")

    part_two = solve_part_two(sums)
    print(f"Part two: {part_two}")


if __name__ == "__main__":
    main()


SAMPLE_INPUT = """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def test_part_one_max_calories() -> None:
    assert solve_part_one(sum_groups(SAMPLE_INPUT)) == 24_000


def test_real_part_one() -> None:
    assert solve_part_one(sum_groups(read_input(1))) == 72_240


def test_part_two_sum_top_three() -> None:
    assert solve_part_two(sum_groups(SAMPLE_INPUT)) == 45_000


def test_real_part_two() -> None:
    assert solve_part_two(sum_groups(read_input(1))) == 210_957
