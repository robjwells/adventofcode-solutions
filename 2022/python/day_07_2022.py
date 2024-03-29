from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import reduce
from typing import Iterator, Sequence

import pytest
from pyrsistent import PVector, v

from util import read_input


@dataclass(frozen=True)
class File:
    name: str
    size: int

    def __str__(self) -> str:
        return f"{self.size:>8}  {self.name}"


class Directory:
    name: str
    dirs: dict[str, Directory]
    files: dict[str, File]
    _size: int | None

    def __init__(self, name: str) -> None:
        self.name = name
        self.dirs = {}
        self.files = {}
        self._size = None

    def ensure_dir(self, name: str) -> Directory:
        return self.dirs.setdefault(name, Directory(name))

    def add_file(self, name: str, size: int) -> None:
        assert name not in self.files, f"File {name!r} already exists."
        self.files[name] = File(name, size)

    @property
    def size(self) -> int:
        if self._size is None:
            files_total = sum(f.size for f in self.files.values())
            dirs_total = sum(d.size for d in self.dirs.values())
            self._size = files_total + dirs_total
        return self._size

    def __str__(self) -> str:
        output = f"- {self.name}\n"
        for file in sorted(self.files.values(), key=lambda f: f.name):
            output += f"| {file}\n"
        for dir in sorted(self.dirs.values(), key=lambda d: d.name):
            for line in str(dir).splitlines():
                output += f"  {line}\n"
        return output

    def lookup(self, *names: str) -> Directory | File:
        cwd = self
        for name in names:
            if name in cwd.dirs:
                cwd = cwd.dirs[name]
            elif name == self.name:
                return self
            elif name in cwd.files:
                assert names[-1] == name, "Path components after filename."
                return cwd.files[name]
            else:
                raise ValueError(f"Not found: {cwd.name}/{name}")
        return cwd


def _parse_line(path: PVector[Directory], line: str) -> PVector[Directory]:
    match line.split():
        case ["$", "ls"]:
            return path
        case ["$", "cd", ".."]:
            return path.delete(-1)
        case ["$", "cd", d] if not path:
            return path.append(Directory(d))
        case ["$", "cd", d] if path:
            nd = path[-1].ensure_dir(d)
            return path.append(nd)
        case ["dir", _]:
            return path
        case [size, name]:
            path[-1].add_file(name, int(size))
            return path
        case _:
            raise ValueError(r"Unexpected line: {line!r}")


def parse(s: str) -> Directory:
    root, *_ = reduce(_parse_line, s.splitlines(), v())
    return root


def walk_dirs(root: Directory) -> Iterator[Directory]:
    queue = deque([root])
    while queue:
        cwd = queue.popleft()
        queue.extend(cwd.dirs.values())
        yield cwd


def solve_part_one(root: Directory) -> int:
    assert root.name == "/"
    return sum(d.size for d in walk_dirs(root) if d.size <= 100_000)


def solve_part_two(root: Directory) -> int:
    # Smallest directory that can be deleted to free up enough space.

    total_size = 70000000
    needed_free = 30000000
    current_free = total_size - root.size
    minimum_size = needed_free - current_free

    return min(d.size for d in walk_dirs(root) if d.size >= minimum_size)


def main() -> None:
    puzzle_input = read_input(7)
    root = parse(puzzle_input)

    part_one = solve_part_one(root)
    assert part_one == 1_077_191
    print(f"Part one: {part_one:,}")

    part_two = solve_part_two(root)
    assert part_two == 5_649_896
    print(f"Part two: {part_two:,}")


if __name__ == "__main__":
    main()


SAMPLE_INPUT = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


@pytest.mark.parametrize(
    ["names", "size"],
    [
        (("a", "e", "i"), 584),
        (("a", "e"), 584),
        (("a"), 94_853),
        (("d",), 24_933_642),
        (("/",), 48_381_165),
    ],
)  # type: ignore
def test_parse(names: Sequence[str], size: int) -> None:
    tree = parse(SAMPLE_INPUT)
    assert tree.name == "/"
    assert tree.lookup(*names).size == size


def test_solve_part_one_sample_input() -> None:
    assert solve_part_one(parse(SAMPLE_INPUT)) == 95_437


def test_solve_part_two_sample_input() -> None:
    assert solve_part_two(parse(SAMPLE_INPUT)) == 24933642
