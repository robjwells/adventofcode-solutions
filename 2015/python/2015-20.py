def total_presents(house_number, presents_per_elf, elf_limit=None):
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

    # Flatten the divisors list and remove duplicates
    divisors = {divisor for divisor_pair in divisors
                        for divisor in divisor_pair}
    if elf_limit is not None:
        divisors = (d for d in divisors
                    if d * elf_limit >= house_number)
    return sum(d * presents_per_elf for d in divisors)


def first_house_with_n_presents(
        target_presents, head_start=50,
        elf_limit=None, presents_per_elf=10):
    """Return the number of the first house with at least total_presents

    head_start determines which house to start at — smaller numbers give
    a larger head start (it is used to divide target_presents).

    This implements a linear search.
    """
    presents = 0
    house_number = target_presents // head_start

    while presents < target_presents:
        house_number += 1
        presents = total_presents(house_number, elf_limit=elf_limit,
                                  presents_per_elf=presents_per_elf)
    return house_number


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
        assert first_house_with_n_presents(presents) == house_number


def main(puzzle_input):
    part_one_result = first_house_with_n_presents(puzzle_input)
    print(f'Part one: {part_one_result:,}')

    part_two_result = first_house_with_n_presents(
        puzzle_input, elf_limit=50, presents_per_elf=11)
    print(f'Part two: {part_two_result:,}')


if __name__ == '__main__':
    puzzle_input = 36000000
    main(puzzle_input)
