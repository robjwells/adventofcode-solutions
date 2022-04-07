"""--- Day 4: Giant Squid ---"""
from __future__ import annotations

from dataclasses import dataclass
from typing import cast

import aoc


class Board:
    _line_width = 5
    _lines: list[list[int | None]]
    _numbers: set[int]

    def __init__(self, lines: list[list[int]]) -> None:
        _l = cast(list[list[int | None]], lines)
        self._lines = _l
        self._numbers = {col for line in lines for col in line}

    @classmethod
    def from_string(cls, string: str) -> Board:
        lines = [[int(part) for part in line.split()] for line in string.splitlines()]
        return cls(lines)

    def __contains__(self, item: int) -> bool:
        return item in self._numbers

    def mark(self, number: int) -> None:
        if number not in self:
            # Early return if the number isn't on the board.
            return
        else:
            # Recreate _lines without the called number.
            self._lines = [
                [n if n != number else None for n in line] for line in self._lines
            ]
            self._numbers.remove(number)

    def _any_empty_rows(self) -> bool:
        return not all([[n for n in line if n is not None] for line in self._lines])

    def _any_empty_columns(self) -> bool:
        return not all(
            [
                [line[idx] for line in self._lines if line[idx] is not None]
                for idx in range(self._line_width)
            ]
        )

    def __str__(self) -> str:
        return (
            "\n".join(
                [
                    " ".join([f"{n:2}" if n is not None else " x" for n in line])
                    for line in self._lines
                ]
            )
            + "\n"
        )

    @property
    def has_won(self) -> bool:
        return self._any_empty_rows() or self._any_empty_columns()

    @property
    def unmarked_numbers(self) -> list[int]:
        return [n for line in self._lines for n in line if n is not None]


def test_board_not_won():
    b = Board.from_string(
        """\
1 1 1 1 1
2 2 2 2 2
3 3 3 3 3
4 4 4 4 4
5 5 5 5 5
"""
    )
    assert not b.has_won


def test_board_won_row():
    b = Board.from_string(
        """\
1 1 1 1 1
2 2 2 2 2
3 3 3 3 3
4 4 4 4 4
5 5 5 5 5
"""
    )
    b.mark(3)
    assert b.has_won


def test_board_won_column():
    b = Board.from_string(
        """\
1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
1 2 3 4 5
"""
    )
    b.mark(3)
    assert b.has_won


def test_board_not_won_diagonal():
    b = Board.from_string(
        """\
3 2 1 4 5
1 3 1 4 5
1 2 3 4 5
1 2 1 3 5
1 2 1 4 3
"""
    )
    b.mark(3)
    assert not b.has_won


def test_board_won_after_sequence():
    b = Board.from_string(
        """\
 1  2  3  4  5
 6  7  8  9 10
11 12 13 14 15
16 17 18 19 20
21 22 23 24 25
"""
    )
    nums = [1, 6, 11, 25, 16, 21]
    for n in nums[:-1]:
        b.mark(n)
        assert not b.has_won
    b.mark(nums[-1])
    print(b)
    assert b.has_won


@dataclass
class Bingo:
    draw_order: list[int]
    boards: list[Board]
    last_drawn: int | None = None

    @classmethod
    def from_string(cls, puzzle_input: str) -> Bingo:
        draw_order, *board_input = puzzle_input.split("\n\n")
        numbers = [int(part) for part in draw_order.split(",")]
        board_objects = [Board.from_string(bs) for bs in board_input]
        return cls(numbers, board_objects)

    def draw(self) -> None:
        number = self.draw_order.pop(0)
        for board in self.boards:
            board.mark(number)
        self.last_drawn = number

    @property
    def any_won(self) -> bool:
        return any(board.has_won for board in self.boards)

    def play_until_won(self) -> Board:
        while not self.any_won:
            self.draw()
        winner = [b for b in self.boards if b.has_won][0]
        return winner


def test_example_input() -> None:
    example_data = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
8   2 23  4 24
21  9 14 16  7
6  10  3 18  5
1  12 20 15 19

3 15   0  2 22
9 18  13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
2  0  12  3  7
"""
    game = Bingo.from_string(example_data)
    winner = game.play_until_won()
    last_number_played = game.last_drawn
    assert last_number_played == 24
    unmarked_sum = sum(winner.unmarked_numbers)
    assert unmarked_sum == 188


def calculate_first_winner_final_score(game: Bingo) -> int:
    winner = game.play_until_won()
    last_number_played = cast(int, game.last_drawn)
    unmarked_sum = sum(winner.unmarked_numbers)
    return unmarked_sum * last_number_played


def main(puzzle_input: str) -> tuple[int, None]:
    bingo = Bingo.from_string(puzzle_input)
    p1 = calculate_first_winner_final_score(bingo)
    return p1, None


if __name__ == "__main__":
    puzzle_input = aoc.load_puzzle_input(2021, 4)
    p1, p2 = main(puzzle_input)
    print(aoc.format_solution(title=__doc__, part_one=p1, part_two=p2))
