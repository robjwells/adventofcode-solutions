"""Day 14: Space Stoichiometry"""
from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Iterator, List, Set, Tuple

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


def topo_dfs(graph: Dict[str, List[str]]) -> Deque[str]:
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


def main(reaction: List[Reaction]) -> None:
    names = {chem[0]: [r[0] for r in reqs] for chem, reqs in reactions}
    ts = topo_dfs(names)


if __name__ == "__main__":
    reactions = list(parse_input(aoc_common.load_puzzle_input(DAY)))
    main(reactions)
