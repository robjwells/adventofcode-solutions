"""Day 14: Space Stoichiometry"""
from __future__ import annotations

from collections import defaultdict, deque
from math import ceil
from typing import Iterator, List, NamedTuple, Tuple, Set
from pprint import pprint

import aoc_common

DAY = 14

Chemical = Tuple[str, int]
Reaction = Tuple[Chemical, List[Chemical]]


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


def topological_sort(graph: Dict[str, List[str]], start_nodes: List[str], skip_nodes: List[str]):
    L = []
    S = set(start_nodes)
    while S:
        n = S.pop()
        if n in skip_nodes:
            continue
        edges = graph.pop(n)
        L.append(n)
        for m in edges:
            if not any(m in reqs for reqs in graph.values()):
                S.add(m)
    return L


def main(reaction_gen) -> None:
    reactions = list(reaction_gen)
    names = {chem[0]: [r[0] for r in reqs] for chem, reqs in reactions}
    reaction_graph = {
        reaction[0][0]: reaction
        for reaction in reactions
    }
    ts = topological_sort(names, ["FUEL"], ["ORE"])
    pprint(ts)
    pprint(reactions)
    # ceil(need / made) * req_amount

if __name__ == "__main__":
    main(parse_input(aoc_common.load_puzzle_input(DAY)))
