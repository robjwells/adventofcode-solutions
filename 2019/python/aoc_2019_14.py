"""Day 14: Space Stoichiometry"""
from __future__ import annotations

from collections import defaultdict, deque
from math import ceil
from typing import DefaultDict, Deque, Dict, Iterator, List, Set, Tuple

import pytest

import aoc

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


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # fmt: off
    ("""\
10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL
""", 31),
    ("""\
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
""", 165),
    ("""\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
""", 13312),
    ("""\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
""", 180697),
    ("""\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
""", 2210736),
        # fmt: on
    ],
)
def test_min_ore_for_one_fuel(input_text: str, expected: int) -> None:
    parsed = dict(parse_input(input_text))
    assert ore_requirements(parsed) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        # fmt: off
    ("""\
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
""", 82892753),
    ("""\
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
""", 5586022),
    ("""\
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
""", 460664),
        # fmt: on
    ],
)
def test_max_fuel_for_one_trillion_ore(input_text: str, expected: int) -> None:
    parsed = dict(parse_input(input_text))
    assert max_fuel_for_ore(parsed) == expected


def max_fuel_for_ore(
    reactions: Reactions, ore_available: int = 1_000_000_000_000
) -> int:
    low = 0
    high = ore_available
    pivot = ore_available // 2

    while low < pivot < high:
        ore_required = ore_requirements(reactions, fuel_needed=pivot)
        if ore_required <= ore_available:
            low = pivot
        else:
            high = pivot
        pivot = low + ((high - low) // 2)

    return pivot


def main(reactions: Reactions) -> Tuple[int, int]:
    minimum_ore_for_one_fuel = ore_requirements(reactions)
    max_fuel_for_trillion_ore = max_fuel_for_ore(reactions)
    return minimum_ore_for_one_fuel, max_fuel_for_trillion_ore


if __name__ == "__main__":
    reactions = dict(parse_input(aoc.load_puzzle_input(2019, DAY)))
    part_one_solution, part_two_solution = main(reactions)

    assert (
        part_one_solution == 261960
    ), "Part one solution doesn't match known-correct answer."

    assert (
        part_two_solution == 4366186
    ), "Part two solution doesn't match known-correct answer."

    print(
        aoc.format_solution(
            title=__doc__,
            part_one=part_one_solution,
            part_two=part_two_solution,
        )
    )
