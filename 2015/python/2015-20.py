def total_presents(house_number, presents_per_elf=10):
    """Calculate how many presents house_number should receive

    Each house is visited by numbered elves which match the divisors of
    house_number, and each elf delivers a quantity of presents that
    match the elf’s number times by presents_per_elf.

    For instance, given:
        house_number == 9
        presents_per_elf = 10
    The divisors (and therefore the elves) are:
        [1, 3, 9]
    And the presents delivered by each:
        [10, 30, 90]
    For a total number of presents:
        130
    """
    # Set a bound within which to search for divisors
    int_sqrt_ish = int(house_number ** 0.5)
    # All the numbers that cleanly divide house_number
    divisors = [
        (x, house_number / x)
        for x in range(1, int_sqrt_ish + 1)
        if house_number % x == 0
        ]
    # Flat map the divisors and remove duplicates
    divisors = {divisor for divisor_pair in divisors
                        for divisor in divisor_pair}
    return sum(d * presents_per_elf for d in divisors)


def first_house_with_n_presents_linear(target_presents, head_start=50):
    """Return the number of the first house with at least total_presents

    head_start determines which house to start at — smaller numbers give
    a larger head start (it is used to divide target_presents).

    This implements a linear search.
    """
    presents = 0
    house_number = target_presents // head_start

    while presents < target_presents:
        house_number += 1
        presents = total_presents(house_number)

    return house_number


def first_house_with_n_presents_binary(target_presents,
                                       low_point=1, high_point=None):
    """Return the number of the first house with at least total_presents

    This implements a binary, or divide and conquer, search.

    It doesn’t actually work for this puzzle because the search space
    is not linearly ascending — lower numbered houses can have higher
    numbers of presents.
    """
    if high_point is None:
        high_point = target_presents
    closest_presents = high_point * 2
    closest_house = None

    while closest_presents >= target_presents:
        if low_point == high_point:
            return low_point
        elif high_point - low_point == 1:
            high_presents = total_presents(high_point)
            low_presents = total_presents(low_point)
            if low_presents >= target_presents:
                return low_point
            else:
                return high_point

        mid_point = low_point + ((high_point - low_point) // 2)
        mid_point_presents = total_presents(mid_point)

        if mid_point_presents == target_presents:
            # Found the number of presents exactly (unlikely!)
            return mid_point

        if mid_point_presents < target_presents:
            low_point = mid_point
        elif mid_point_presents > (target_presents * 1.05):
            # Greater than 5% away from the target number of presents
            high_point = mid_point


def test_house_total_presents():
    test_input = [
        (1, 10),
        (2, 30),
        (3, 40),
        (4, 70),
        (5, 60),
        (6, 120),
        (7, 80),
        (8, 150),
        (9, 130),
        ]
    for house_number, expected_presents in test_input:
        assert total_presents(house_number) == expected_presents


def test_first_house_with_n_presents():
    test_input = [
        (10, 1),
        (20, 2),
        (30, 2),
        (40, 3),
        (50, 4),
        (60, 4),
        (70, 4),
        (80, 6),
        (90, 6),
        (100, 6),
        (110, 6),
        (120, 6),
        (130, 8),
        (140, 8),
        (150, 8),
        ]

    for presents, house_number in test_input:
        assert first_house_with_n_presents_linear(presents) == house_number
        assert first_house_with_n_presents_binary(presents) == house_number


def main(puzzle_input):
    part_one_result = first_house_with_n_presents_linear(puzzle_input)
    print(f'Part one: {part_one_result:,}')


if __name__ == '__main__':
    puzzle_input = 36000000
    main(puzzle_input)
