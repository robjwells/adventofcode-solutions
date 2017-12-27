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


def first_house_with_n_presents(target_presents):
	"""Return the number of the first house with at least total_presents"""
	presents = 0
	house_number = 0
	while presents < total_presents:
		house_number += 1
		presents = total_presents(house_number)
	return house_number


def test_house_total_presents():
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


def test_first_house_with_n_presents():
	test_input = [
		(10, 1),
		(30, 2),
		(40, 3),
		(70, 4),
		(60, 5),
		(120, 6),
		(80, 7),
		(150, 8),
		(130, 9),
		]	


def first_house_with_n_presents(total_presents):
	"""Return the number of the first house with at least total_presents"""
	pass


def main(puzzle_input):
	pass


if __name__ == '__main__':
	puzzle_input = None
	main(puzzle_input)
	