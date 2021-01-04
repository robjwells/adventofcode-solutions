from __future__ import annotations

from collections import Counter
from functools import reduce
from typing import Callable
from typing import Counter as TCounter
from typing import List

import pytest

from aoc_common import T, load_puzzle_input, report_solution


def update_counters_with_characters(
    counters: List[TCounter[str]], string: str
) -> List[TCounter[str]]:
    for counter, character in zip(counters, string):
        counter.update(character)
    return counters


def select_nth_most_common(counter: TCounter[T], n: int) -> T:
    assert counter, "counter must not be empty"
    return counter.most_common()[n][0]


def most_common_counter_element(counter: TCounter[T]) -> T:
    return select_nth_most_common(counter, 0)


def least_common_counter_element(counter: TCounter[T]) -> T:
    return select_nth_most_common(counter, -1)


Selector = Callable[[TCounter[T]], T]


def most_likely_message(signals: List[str], selector: Selector[str]) -> str:
    counters: List[TCounter[str]] = [Counter() for _ in range(len(signals[0]))]
    _ = reduce(update_counters_with_characters, signals, counters)
    most_likely = [selector(c) for c in counters]
    return "".join(most_likely)


@pytest.mark.parametrize(
    "selector,expected",
    [
        (most_common_counter_element, "easter"),
        (least_common_counter_element, "advent"),
    ],
)
def test_most_likely_message(selector: Selector[str], expected: str) -> None:
    signals = """\
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""".splitlines()
    assert most_likely_message(signals, selector) == expected


if __name__ == "__main__":
    signals = load_puzzle_input(day=6).splitlines()
    most_common = most_likely_message(signals, selector=most_common_counter_element)
    least_common = most_likely_message(signals, selector=least_common_counter_element)
    report_solution(
        puzzle_title="Day 6: Signals and Noise",
        part_one_solution=most_common,
        part_two_solution=least_common,
    )
