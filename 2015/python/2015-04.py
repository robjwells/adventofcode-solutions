#!/usr/local/bin/python3

import hashlib


def suffix_for_md5_prefix(secret_key, char='0', length=5, starting_integer=1):
    """Return the first integer suffix to secret_key that produces wanted hash

    The wanted hash is expected to have a prefix of `char`
    repeated `length` times.

    For example, the defaults would return the first integer appended to
    `secret_key` that produces a hash beginning with five zeroes.

    `starting_integer` is the first integer appended to `secret_key` and then
    hashed. It can be used to get a head start on calculations.
    """
    int_suffix = starting_integer
    wanted_prefix = char * length
    while True:
        clear_text = secret_key + str(int_suffix)
        md5_hash = hashlib.md5(clear_text.encode()).hexdigest()
        if md5_hash.startswith(wanted_prefix):
            return int_suffix
        int_suffix += 1


def test_prefix():
    test_cases = [
        ('abcdef', 609043),
        ('pqrstuv', 1048970)]
    for key, int_suffix in test_cases:
        assert suffix_for_md5_prefix(secret_key=key) == int_suffix


def main(secret_key):
    pass


if __name__ == '__main__':
    puzzle_input = 'ckczppom'
    main(puzzle_input)
