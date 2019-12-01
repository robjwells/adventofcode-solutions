"""Day 1: The Tyranny of the Rocket Equation"""
import aoc_common
import pytest
from typing import List

DAY = 1


def fuel_to_launch_module(module_mass: int) -> int:
    """Calculate the fuel to launch a module of the given mass.

    Fuel required to launch a given module is based on its mass.
    Specifically, to find the fuel required for a module,
    take its mass, divide by three, round down, and subtract 2.
    """
    return max(module_mass // 3 - 2, 0)


def comprehensive_fuel_to_launch_module(mass: int) -> int:
    if mass <= 0:
        return 0
    immediate_fuel_required = fuel_to_launch_module(mass)
    fuel_required_for_fuel = comprehensive_fuel_to_launch_module(
        immediate_fuel_required
    )
    return immediate_fuel_required + fuel_required_for_fuel


@pytest.mark.parametrize("mass,fuel", [(12, 2), (14, 2), (1969, 654), (100756, 33583)])
def test_mass_to_fuel(mass: int, fuel: int) -> None:
    assert fuel_to_launch_module(mass) == fuel


@pytest.mark.parametrize("mass,fuel", [(14, 2), (1969, 966), (100756, 50346)])
def test_comprehensive_fuel_to_launch_module(mass: int, fuel: int) -> None:
    assert comprehensive_fuel_to_launch_module(mass) == fuel


def solve_part_one(puzzle_input: List[int]) -> int:
    return sum(fuel_to_launch_module(mass) for mass in puzzle_input)


def solve_part_two(puzzle_input: List[int]) -> int:
    return sum(comprehensive_fuel_to_launch_module(mass) for mass in puzzle_input)


def parse_input(puzzle_input: str) -> List[int]:
    return [int(line) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    puzzle_input = aoc_common.load_puzzle_input(DAY)
    parsed = parse_input(puzzle_input)
    fuel_required_for_modules = solve_part_one(parsed)
    total_fuel_required = solve_part_two(parsed)
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=fuel_required_for_modules,
        part_two_solution=total_fuel_required,
    )
