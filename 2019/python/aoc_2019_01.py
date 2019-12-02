"""Day 1: The Tyranny of the Rocket Equation"""
import aoc_common
import pytest
from typing import Callable, List

DAY = 1


def fuel_to_launch_mass(module_mass: int) -> int:
    """Calculate the fuel to launch a module of the given mass."""
    return max(module_mass // 3 - 2, 0)


def fuel_to_launch_mass_and_fuel(mass: int) -> int:
    """Calculate fuel required for initial mass and fuel itself.

    Recursively calculate the fuel required to launch a module of
    the given mass (initial call), then fuel required to launch
    that fuel, and so on until the amount of additional fuel
    needed is zero.
    """
    if mass <= 0:
        return 0
    immediate_fuel = fuel_to_launch_mass(mass)
    return immediate_fuel + fuel_to_launch_mass_and_fuel(immediate_fuel)


@pytest.mark.parametrize("mass,fuel", [(12, 2), (14, 2), (1969, 654), (100756, 33583)])
def test_mass_to_fuel(mass: int, fuel: int) -> None:
    assert fuel_to_launch_mass(mass) == fuel


@pytest.mark.parametrize("mass,fuel", [(14, 2), (1969, 966), (100756, 50346)])
def test_comprehensive_fuel_to_launch_module(mass: int, fuel: int) -> None:
    assert fuel_to_launch_mass_and_fuel(mass) == fuel


def parse_input(puzzle_input: str) -> List[int]:
    return [int(line) for line in puzzle_input.splitlines()]


if __name__ == "__main__":
    puzzle_input = aoc_common.load_puzzle_input(DAY)
    parsed = parse_input(puzzle_input)
    fuel_required_for_modules = sum(map(fuel_to_launch_mass, parsed))
    total_fuel_required = sum(map(fuel_to_launch_mass_and_fuel, parsed))
    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=fuel_required_for_modules,
        part_two_solution=total_fuel_required,
    )
