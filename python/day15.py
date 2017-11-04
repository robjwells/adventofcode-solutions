#!/usr/local/bin/python3

from collections import deque
from functools import reduce
from itertools import permutations
import operator
import pathlib
import random

input_file = pathlib.Path(__file__).parent.parent.joinpath('day15_input.txt')


def parse_input(text):
    parsed = dict()
    for line in text.splitlines():
        ingredient, qualities = line.split(': ', maxsplit=1)
        parsed[ingredient] = dict()
        for qual_pair in qualities.split(', '):
            quality, magnitude = qual_pair.split()
            parsed[ingredient][quality] = int(magnitude)
    return parsed


def test_parse():
    sample_input = '''\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''
    expected = dict(
        Butterscotch=dict(
            capacity=-1, durability=-2, flavor=6, texture=3, calories=8),
        Cinnamon=dict(
            capacity=2, durability=3, flavor=-2, texture=-1, calories=3))
    assert parse_input(sample_input) == expected


def cookie_score(recipe, ingredient_dict):
    qual_scores = [
        [amount * magnitude
            for quality, magnitude in ingredient_dict[ingredient].items()]
        for ingredient, amount in recipe]

    qual_totals = map(sum, zip(*qual_scores))
    # Set negative numbers to zero
    qual_totals = list(map(lambda x: x if x > 0 else 0, qual_totals))
    calories = qual_totals.pop()
    cookie_score = reduce(operator.mul, qual_totals)
    return (cookie_score, calories)


def test_score():
    sample_data = dict(
        Butterscotch=dict(
            capacity=-1, durability=-2, flavor=6, texture=3, calories=8),
        Cinnamon=dict(
            capacity=2, durability=3, flavor=-2, texture=-1, calories=3))
    recipe = [('Butterscotch', 44), ('Cinnamon', 56)]
    assert cookie_score(recipe, sample_data) == 62842880


def test_score_zero():
    """Score is zero when any ingredients have negative total"""
    sample_data = dict(
        Butterscotch=dict(
            capacity=-1, durability=-2, flavor=6, texture=3, calories=8),
        Cinnamon=dict(
            capacity=2, durability=3, flavor=-2, texture=-1, calories=3))
    recipe = [('Butterscotch', 100)]
    assert cookie_score(recipe, sample_data) == 0


def add_lists(*lists):
    """Add two lists together without numpy

    For example, given lists:
        [1, 2]  [3, 4]
    The result is:
        [4, 6]

    Lists are sliced to prevent mutation.
    """
    lists = (l[:] for l in lists)
    return list(map(sum, zip(*lists)))


# This is more general but slower than the range-based version below
def combinations(length, total):
    """Return a tuple of given length containing integers with sum total"""
    if length == 1:
        yield (total,)
        return
    for n in range(total + 1):
        x = n
        for y in combinations(length - 1, total - x):
            yield (x,) + y


# This is about twice as fast as the general recursive version above
def combo_four(total):
    """Return a tuple of four integers totalling 100"""
    for i in range(total + 1):
        for j in range(total + 1 - i):
            for k in range(total + 1 - i - j):
                l = total - i - j - k
                yield (i, j, k, l)


def brute_force_cookie(ingredients, teaspoons):
    """Choose best from all possible recipes for number of teaspoons"""
    all_scores = [cookie_score(zip(ingredients, amounts), ingredients)
                  for amounts in combo_four(teaspoons)]
    best_cookie = max(c[0] for c in all_scores)
    best_500_cal_cookie = max(c[0] for c in all_scores if c[1] == 500)
    return (best_cookie, best_500_cal_cookie)


def random_recipe(ingredients, teaspoons):
    """Produce a random recipe for x ingredients totally y teaspoons"""
    amounts = []
    for _ in range(len(ingredients) - 1):
        remaining = teaspoons - sum(amounts)
        amounts.append(random.randint(0, remaining))
    return amounts + [teaspoons - sum(amounts)]


# This is quicker, almost never gets the top-score cookie wrong
# but gets the 500-calorie cookie wrong about 5% of the time.
# However, it is roughly 3 times faster than the brute-force search.
def search_for_best_cookie(starting_recipe, ingredients, teaspoons,
                           recipes_tried, cal_target=500):
    """Incrementally improve starting recipe until it can’t be better"""
    single_changes = (1, -1, 0, 0)
    single_change_permutations = set(permutations(single_changes))
    recipes_tried.add(tuple(starting_recipe))

    def score_helper(recipe):
        return cookie_score(zip(ingredients, recipe), ingredients)

    def new_recipes(current_recipe):
        for c in single_change_permutations:
            candidate = tuple(add_lists(current_recipe, c))
            suitable = (
                candidate not in recipes_tried and
                sum(candidate) == teaspoons and
                min(candidate) >= 0 and
                max(candidate) <= teaspoons)
            if suitable:
                yield candidate
            else:
                continue

    def initial_check(starting_recipe):
        candidates = [starting_recipe]
        candidates.extend(new_recipes(starting_recipe))
        score_pairs = []
        for c in candidates:
            score, calories = score_helper(c)
            if score:
                score_pairs.append((c, score, calories))
        max_score = max(score_pairs,
                        key=lambda t: t[1],
                        default=(tuple(), 0, 0))
        return max_score

    starting_recipe, best_score, best_cals = initial_check(starting_recipe)
    if not best_score:
        return (0, 0)

    best_calorie_limit_score = 0

    recipes_to_try = deque()
    recipes_to_try.extend(new_recipes(starting_recipe))

    while recipes_to_try:
        current = recipes_to_try.popleft()
        score, calories = score_helper(current)
        recipes_to_add = []
        if score >= best_score:
            best_score = score
            recipes_to_add.extend(new_recipes(current))
        if score and abs(cal_target - calories) <= abs(cal_target - best_cals):
            best_cals = calories
            if calories == cal_target and score > best_calorie_limit_score:
                best_calorie_limit_score = score
            recipes_to_add.extend(new_recipes(current))
        recipes_to_try.extend(recipes_to_add)
        recipes_tried.add(current)

    return best_score, best_calorie_limit_score


def repeated_search(ingredients, teaspoons, iterations):
    scores = []
    visited = set()
    while iterations:
        recipe = random_recipe(ingredients, 100)
        if tuple(recipe) in visited:
            continue
        else:
            iterations -= 1
        score = search_for_best_cookie(
            recipe, ingredients, 100,
            recipes_tried=visited)
        if sum(score):
            scores.append(score)
    if not scores:
        return (0, 0)
    else:
        return (max(t[0] for t in scores),
                max(t[1] for t in scores))


if __name__ == '__main__':
    ingredients = parse_input(input_file.read_text())
    p1_cookie, p2_cookie = brute_force_cookie(ingredients, 100)
    print('Brute force search')
    print(f'Part one: {p1_cookie}')
    print(f'Part two: {p2_cookie}')
    p1_cookie, p2_cookie = repeated_search(ingredients, 100, 2000)
    print('Incremental random search')
    print(f'Part one: {p1_cookie}')
    print(f'Part two: {p2_cookie}')
