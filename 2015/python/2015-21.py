#!/usr/bin/env python3
"""Advent of Code 2015, Day 21: RPG Simulator 20XX"""

from collections import namedtuple
from functools import reduce
import itertools
import math

import pytest


Item = namedtuple('Item', ['name', 'cost', 'damage', 'armor'])
EquipmentSummary = namedtuple('EquipmentSummary', ['cost', 'damage', 'armor'])


def item_combinations(items, combo_range):
    """Return item combinations, allowing for no item to be chosen

    `combo_range` is the acceptable lengths of the combinations, with None
    inserted so the length of the combination is always the upper
    limit of the range. For instance:
        [a, b], range(2)    ->      (a), (b), (None)
        [a, b], range(3)    ->      (a, b), (a, None), (b, None),
                                        (None, None)

    You can force an item to be chosen by excluding 0 from the range:
        [a, b], range(1, 2)     ->      (a), (b)
        [a, b], range(1, 3)     ->      (a, b)
        [a, b, c], range(1, 3)  ->      (a, b), (a, c), (b, c)
    """
    if combo_range.start < 0 or combo_range.stop < 0:
        raise ValueError('Range must not be negative')
    elif (combo_range.start == combo_range.stop or
            combo_range.start == 0 and combo_range.stop == 1):
        # Choices are of length zero
        return []

    full_length_combos = []
    if combo_range.start == 0:
        no_choice = [None for _ in range(combo_range.stop - 1)]
        full_length_combos.append(tuple(no_choice))
        combo_range = range(1, combo_range.stop)

    expected_length = combo_range.stop - 1
    for length in combo_range:
        combos = itertools.combinations(items, length)
        if length < expected_length:
            combos = [c + tuple([None] * (expected_length - length))
                      for c in combos]
        full_length_combos.extend(combos)

    return full_length_combos


@pytest.mark.parametrize('items,combo_range,expected', [
    (['a', 'b'], range(1), []),
    (['a', 'b'], range(2), [(None,), ('a',), ('b',)]),
    (['a', 'b'], range(1, 2), [('a',), ('b',)]),
    (['a', 'b'], range(3),
        [(None, None), ('a', None), ('b', None), ('a', 'b')]),
    (['a', 'b'], range(1, 2), [('a',), ('b',)]),
    (['a', 'b'], range(2, 3), [('a', 'b')]),
])
def test_combos(items, combo_range, expected):
    assert item_combinations(items, combo_range) == expected


def test_combos_disallows_negative():
    for r in [range(-2, 2), range(2, -2)]:
        with pytest.raises(ValueError):
            item_combinations([], r)


class Fighter:
    def __init__(self, hit_points, damage, armor):
        self.hit_points = hit_points
        self.damage = damage
        self.armor = armor

    def __str__(self):
        return 'Fighter(hit_points={}, damage={}, armor={})'.format(
            self.hit_points, self.damage, self.armor)

    def __repr__(self):
        return self.__str__()

    def attack(self, enemy):
        """Deal damage to the enemy

        Damage is mitigated by any enemy armor, but at least
        1 damage is dealt on each attack.
        """
        damage_dealt = self.damage - enemy.armor
        if damage_dealt < 1:
            damage_dealt = 1
        enemy.hit_points -= damage_dealt


@pytest.mark.parametrize('fighter,enemy,expected_damage', [
    (Fighter(hit_points=8, damage=5, armor=5),
     Fighter(0, 0, 2), 3),
    (Fighter(hit_points=8, damage=7, armor=2),
     Fighter(0, 0, 5), 2),
    (Fighter(hit_points=0, damage=0, armor=0),
     Fighter(0, 0, 10), 1)
])
def test_Fighter_attack(fighter, enemy, expected_damage):
    """Fighter.attack does damage to the enemy

    Damage should be calculated based on the damage score of the fighter
    and the armor score of the enemy, doing at least 1 damage and reducing
    the hit points of the enemy appropriately.
    """
    fighter.attack(enemy)
    assert -enemy.hit_points == expected_damage


def simulate_player_wins_fight(player, boss):
    """Simulate a fight between player and boss and report if player won

    Returns True if player wins and False if boss wins.

    Player always attacks first.
    """
    while all(f.hit_points > 0 for f in [player, boss]):
        for a, b in [(player, boss), (boss, player)]:
            a.attack(b)
    return boss.hit_points <= 0


def calculate_player_wins_fight(player, boss):
    """Calculate whether player would win a fight against boss

    Returns True if player wins and False if boss wins.

    Player always attacks first.
    """
    player_total_damage = player.damage - boss.armor
    if player_total_damage <= 0:
        player_total_damage = 1

    boss_total_damage = boss.damage - player.armor
    if boss_total_damage <= 0:
        boss_total_damage = 1

    player_rounds = math.ceil(boss.hit_points / player_total_damage)
    boss_rounds = math.ceil(player.hit_points / boss_total_damage)

    # Player wins if it takes the same number or fewer attacks to
    # deplete the boss's hit points (as the player starts)
    return player_rounds <= boss_rounds


@pytest.mark.parametrize('fight_function', [
    simulate_player_wins_fight,
    calculate_player_wins_fight,
])
def test_player_boss_fight(fight_function):
    """Player should win when known stronger than boss

    fight_function allows us to test two different ways
    of deciding the fight.
    """
    player = Fighter(hit_points=8, damage=5, armor=5)
    boss = Fighter(hit_points=12, damage=7, armor=2)
    assert fight_function(player, boss)


def equipment_combinations(weapons, armor, rings):
    """Return a list of equipment combinations"""
    weapon_choices = item_combinations(weapons, range(1, 2))
    armor_choices = item_combinations(armor, range(2))
    ring_choices = item_combinations(rings, range(3))
    complete_choices = itertools.product(
        weapon_choices, armor_choices, ring_choices)
    return complete_choices


def summarise_equipment(equipment):
    """Sum the cost, damage and armor attributes of items in equipment"""
    totals = reduce(
        lambda total, gear: (total[0] + gear.cost,
                             total[1] + gear.damage,
                             total[2] + gear.armor),
        filter(lambda x: x is not None, itertools.chain(*equipment)),
        (0, 0, 0))
    return EquipmentSummary(*totals)


def main(boss_stats, weapons, armor, rings):
    gear_choices = equipment_combinations(weapons, armor, rings)
    gear_summaries = [summarise_equipment(g) for g in gear_choices]
    gear_by_cost = sorted(gear_summaries, key=lambda s: s.cost)

    # Part one: Least spent to win the fight
    for gear in gear_by_cost:
        boss = Fighter(*boss_stats)
        player = Fighter(hit_points=100, damage=gear.damage, armor=gear.armor)
        if simulate_player_wins_fight(player, boss):
            print(f'Part one, least spent to win: {gear.cost}')
            break

    # Part two: Most spent but lose the fight
    for gear in reversed(gear_by_cost):
        boss = Fighter(*boss_stats)
        player = Fighter(hit_points=100, damage=gear.damage, armor=gear.armor)
        if not simulate_player_wins_fight(player, boss):
            print(f'Part two, most spent to lose: {gear.cost}')
            break


if __name__ == '__main__':
    # Puzzle input (boss stats):
    #     Hit Points: 104
    #     Damage: 8
    #     Armor: 1
    boss_stats = (104, 8, 1)

    # Items
    # name, cost, damage, armor
    weapons = [Item(*t) for t in [
        ('Dagger',      8,  4,  0),
        ('Shortsword', 10,  5,  0),
        ('Warhammer',  25,  6,  0),
        ('Longsword',  40,  7,  0),
        ('Greataxe',   74,  8,  0),
        ]]

    armor = [Item(*t) for t in [
        ('Leather',    13,  0,  1),
        ('Chainmail',  31,  0,  2),
        ('Splintmail', 53,  0,  3),
        ('Bandedmail', 75,  0,  4),
        ('Platemail', 102,  0,  5),
        ]]

    rings = [Item(*t) for t in [
        ('Damage +1',  25,  1,  0),
        ('Damage +2',  50,  2,  0),
        ('Damage +3', 100,  3,  0),
        ('Defense +1', 20,  0,  1),
        ('Defense +2', 40,  0,  2),
        ('Defense +3', 80,  0,  3),
        ]]

    main(boss_stats, weapons, armor, rings)
