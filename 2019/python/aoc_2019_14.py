"""Day 14: Space Stoichiometry"""
from __future__ import annotations

from collections import defaultdict, deque
from math import ceil
from typing import DefaultDict, Deque, Dict, Iterator, List, Set, Tuple

import aoc_common

DAY = 14

Chemical = Tuple[str, int]
Reaction = Tuple[Chemical, List[Chemical]]
Reactions = Dict[Chemical, List[Chemical]]


def parse_input(data: str) -> Iterator[Reaction]:
    for line in data.splitlines():
        r, o = line.split("=>", maxsplit=1)
        reqs = [
            (name, int(quantity))
            for quantity, name in [chem.split() for chem in r.split(", ")]
        ]
        os = o.split()
        output = (os[1], int(os[0]))
        yield (output, reqs)


def topological_sort(graph: Dict[str, List[str]]) -> Deque[str]:
    L: Deque[str] = deque()
    unvisited = set(graph)
    temporary_mark: Set[str] = set()
    permanent_mark: Set[str] = set()

    def visit(n: str) -> None:
        if n in permanent_mark:
            return
        if n in temporary_mark:
            raise ValueError("Detected cycle in graph.")
        temporary_mark.add(n)
        for m in graph.get(n, []):
            visit(m)
        temporary_mark.remove(n)
        permanent_mark.add(n)
        L.appendleft(n)

    while unvisited or temporary_mark:
        visit(unvisited.pop())

    return L


def order_reactions(reactions: Reactions) -> Reactions:
    names = {chem[0]: [r[0] for r in reqs] for chem, reqs in reactions.items()}
    dependency_order = topological_sort(names)
    # Dictionaries are kept in insertion order from 3.6
    return dict(
        sorted(reactions.items(), key=lambda r: dependency_order.index(r[0][0]))
    )


def ore_requirements(reactions: Reactions, fuel_needed: int = 1) -> int:
    reactions = order_reactions(reactions)
    amounts: DefaultDict[str, int] = defaultdict(lambda: 0)
    amounts["FUEL"] = fuel_needed
    for product, precursors in reactions.items():
        product_name, product_batch_amount = product
        product_needed = amounts[product_name]
        batches_needed = ceil(product_needed / product_batch_amount)
        for precursor_name, precursor_per_batch in precursors:
            total_precursor_needed = batches_needed * precursor_per_batch
            amounts[precursor_name] += total_precursor_needed
    return amounts["ORE"]


def main(reactions: Reactions) -> int:
    minimum_ore_for_one_fuel = ore_requirements(reactions)
    return minimum_ore_for_one_fuel


if __name__ == "__main__":
    reactions = dict(parse_input(aoc_common.load_puzzle_input(DAY)))
    part_one_solution = main(reactions)

    assert (
        part_one_solution == 261960
    ), "Part one solution doesn't match known-correct answer."

    aoc_common.report_solution(
        puzzle_title=__doc__, part_one_solution=part_one_solution
    )
