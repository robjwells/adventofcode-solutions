from __future__ import annotations

from collections import Counter
from functools import reduce
from typing import Counter as TCounter
from typing import List

from aoc_common import T, load_puzzle_input, report_solution


def update_counters_with_characters(
    counters: List[TCounter[str]], string: str
) -> List[TCounter[str]]:
    for counter, character in zip(counters, string):
        counter.update(character)
    return counters


def most_common_counter_element(counter: TCounter[T]) -> T:
    assert counter
    return counter.most_common(1)[0][0]


def most_likely_message(signals: List[str]) -> str:
    counters: List[TCounter[str]] = [Counter() for _ in range(len(signals[0]))]
    _ = reduce(update_counters_with_characters, signals, counters)
    most_common = [most_common_counter_element(c) for c in counters]
    return "".join(most_common)


def test_most_likely_message() -> None:
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
    expected = "easter"
    assert most_likely_message(signals) == expected


if __name__ == "__main__":
    signals = load_puzzle_input(day=6).splitlines()
    likely_message = most_likely_message(signals)
    report_solution(
        puzzle_title="Day 6: Signals and Noise", part_one_solution=likely_message
    )
