from __future__ import annotations
from dataclasses import dataclass

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

    def __init__(self, name: str) -> None:
        self.name = name
        self.dirs = {}
        self.files = {}

    def ensure_dir(self, name: str) -> Directory:
        return self.dirs.setdefault(name, Directory(name))

    def add_file(self, name: str, size: int) -> None:
        assert name not in self.files, f"File {name!r} already exists."
        self.files[name] = File(name, size)

    def __str__(self) -> str:
        output = f"- {self.name}\n"
        for file in sorted(self.files.values(), key=lambda f: f.name):
            output += f"| {file}\n"
        for dir in sorted(self.dirs.values(), key=lambda d: d.name):
            for line in str(dir).splitlines():
                output += f"  {line}\n"
        return output


def ensure_dir(tree, path):
    for dir in path:
        if dir not in tree:
            tree[dir] = {}
        tree = tree[dir]
    return tree


def record_file(tree, path, filename, size):
    dir = ensure_dir(tree, path)
    dir[filename] = size


def parse(s: str) -> dict:
    tree = {}
    cwd: list[str] = []
    ds: list[Directory] = []
    padding = lambda: "  " * len(cwd)
    for line in s.splitlines():
        if line.startswith("$"):
            line = line.split(" ", 1)[1]
            if line.startswith("ls"):
                continue
            if line.startswith("cd"):
                new_dir = line.split()[1]
                if new_dir == "..":
                    old_dir = cwd.pop()
                    print(padding() + f"Leaving {old_dir}")
                    old_dir = ds.pop()
                    print(padding() + f"Leaving {old_dir.name}")
                    continue
                else:
                    print(padding() + f"Entering {new_dir}")
                    cwd.append(new_dir)
                    ensure_dir(tree, cwd)

                    if not ds:
                        ds.append(Directory(new_dir))
                    else:
                        nd = ds[-1].ensure_dir(new_dir)
                        ds.append(nd)
                    continue
        if line.startswith("dir"):
            print(padding() + line)
        else:
            size, name = line.split()
            record_file(tree, cwd, name, int(size))
            ds[-1].add_file(name, int(size))
            print(padding() + str(File(name, int(size))))

    from json import dumps
    print(dumps(tree, sort_keys=True, indent=2))
    print(ds[0])



def solve_part_one(puzzle_input: str) -> int:
    ...


def main() -> None:
    puzzle_input = read_input(7)
    part_one = solve_part_one(puzzle_input)
    print(f"Part one: {part_one:,}")



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


def test_parse() -> None:
    tree = parse(SAMPLE_INPUT)
    assert tree["/"]["a"]["e"]["i"].size == 584

def test_solve_part_one_sample_input() -> None:
    assert solve_part_one(SAMPLE_INPUT) == 95_437
