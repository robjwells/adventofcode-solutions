"""Advent of Code 2018 Day 7: The Sum of Its Parts"""
import aoc_common

from collections import deque, defaultdict

DAY = 7

TEST_INPUT = """\
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""


def solve_part_one(puzzle_input):
    return resolve_dependencies(puzzle_input)


def solve_part_two(puzzle_input):
    return timeParallelWork(puzzle_input)


def create_dependency_structures(pairs):
    must_finish = {first for first, _ in pairs}
    waiting = {second for _, second in pairs}

    order_finished = deque(sorted(must_finish - waiting))
    completed = must_finish - waiting
    to_go = defaultdict(list)
    for dependency, task in pairs:
        to_go[task].append(dependency)
    return (order_finished, completed, to_go)


def resolve_dependencies(pairs):
    order_finished, completed, to_go = create_dependency_structures(pairs)

    while len(to_go):
        for task, dependencies in sorted(to_go.items()):
            if not len(set(dependencies) - completed):
                order_finished.append(task)
                completed.add(task)
                del to_go[task]
                break  # Important as earlier-letter tasks run first

    return "".join(order_finished)


def task_time(task):
    return ord(task) - 64


def timeParallelWork(pairs, workers=5, time_bias=60):
    order_completed, _, unassigned = create_dependency_structures(pairs)
    workers_times = [0] * workers
    workers_tasks = list(order_completed)
    if len(workers_tasks) > workers:
        raise ValueError
    completed = set()
    total_time = 0

    # Set outstanding times for tasks with no dependencies
    for idx, task in enumerate(workers_tasks):
        workers_times[idx] = task_time(task) + time_bias
    workers_tasks.extend([None] * (workers - len(workers_tasks)))

    while sum(workers_times):
        total_time += 1
        workers_times = [max(0, t - 1) for t in workers_times]
        for idx, (time, task) in enumerate(zip(workers_times, workers_tasks)):
            if not time:
                completed.add(task)
                workers_tasks[idx] = None

        for task, dependencies in sorted(unassigned.items()):
            if not any(t == 0 for t in workers_times):
                break  # Important as earlier-letter tasks run first

            if not len(set(dependencies) - completed):
                # Assign task to worker
                time = task_time(task) + time_bias
                for idx, t in enumerate(workers_times):
                    if not t:
                        workers_times[idx] = time
                        workers_tasks[idx] = task
                        break
                del unassigned[task]

    return total_time


def parse_puzzle_input(puzzle_input):
    return [
        (parts[1], parts[-3])
        for parts in [line.split() for line in puzzle_input.splitlines()]
    ]


def test_parse_puzzle_input():
    expected = [
        ("C", "A"),
        ("C", "F"),
        ("A", "B"),
        ("A", "D"),
        ("B", "E"),
        ("D", "E"),
        ("F", "E"),
    ]
    assert parse_puzzle_input(TEST_INPUT) == expected


def test_resolve_dependencies():
    assert resolve_dependencies(parse_puzzle_input(TEST_INPUT)) == "CABDFE"


def test_time_parallel_work():
    assert (
        timeParallelWork(parse_puzzle_input(TEST_INPUT), workers=2, time_bias=0) == 15
    )


if __name__ == "__main__":
    puzzle_input = parse_puzzle_input(aoc_common.load_puzzle_input(DAY))

    print(__doc__)

    part_one_solution = solve_part_one(puzzle_input)
    assert part_one_solution == "GJFMDHNBCIVTUWEQYALSPXZORK"
    print("Part one:", part_one_solution)

    part_two_solution = solve_part_two(puzzle_input)
    assert part_two_solution == 1050
    print("Part two:", part_two_solution)
