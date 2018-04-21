#!/usr/bin/env python3
"""Advent of Code 2015, Day 11: Corporate Policy"""

import re
import string

import pytest


def validate_password(password):
    windowed = (''.join(t) for t in zip(password, password[1:], password[2:]))
    for straight in windowed:
        if straight in string.ascii_lowercase:
            break
    else:
        return False

    exclude_letters = re.compile(r'^[^iol]+$')
    if not exclude_letters.match(password):
        return False

    two_doubles = re.compile(
        r'^ \w* (\w)\1 \w* (\w)\2 \w* $',
        flags=re.VERBOSE)
    double_match = two_doubles.match(password)
    if not double_match or double_match[1] == double_match[2]:
        return False

    return True


def clean_bad_letters(password):
    """Return a candidate password after checking for invalid characters

    If password doesn't contain the characters i, o, or l it is returned
    immediately.

    If it does, the string returned is the next potentially valid password
    after short-circuiting and skipping passwords containing the invalid
    letter in that particular position.

    For example:
        xi      ->   xj
        xix     ->   xja
        xixyz   ->   xjaaa
    """
    first_invalid_char = re.search(r'([iol])', password)
    if first_invalid_char is None:
        return password

    cut_pos = first_invalid_char.start()
    new_letter = increment_letter(first_invalid_char.group())
    letter_a_to_add = len(password[cut_pos:]) - 1
    return password[:cut_pos] + new_letter + 'a' * letter_a_to_add


def increment_letter(letter):
    """Return the character after `letter` in a restricted circular alphabet

    This increments a single letter at a time: a becomes b,
    z becomes a and so on.

    i, o and l are excluded from the alphabet used as they are
    not allowed to appear in valid passwords acccording to the
    problem description.

    It is, however, safe to increment those restricted letters
    using this function as a special case is made for them.
    """
    restricted_dict = {'i': 'j', 'l': 'm', 'o': 'p'}
    if letter in restricted_dict:
        return restricted_dict[letter]

    ok_letters = 'abcdefghjkmnpqrstuvwxyz'
    current_index = ok_letters.index(letter)
    is_final_index = current_index == len(ok_letters) - 1
    new_index = 0 if is_final_index else current_index + 1
    return ok_letters[new_index]


def increment_password(current_pw, pw_index=None):
    pw_list = list(current_pw)
    if pw_index is None:
        pw_index = len(pw_list) - 1
    new_letter = increment_letter(pw_list[pw_index])
    pw_list[pw_index] = new_letter
    if new_letter == 'a' and pw_index > 0:
        pw_list = increment_password(pw_list, pw_index=pw_index - 1)
    return ''.join(pw_list)


def new_password(current_password):
    """Find the next new password starting at current_password

    Only valid passwords are returned, with the requirements being:
        * must include one increasing straight of at least three
          letters, like abc, bcd, cde, and so on, up to xyz.
          They cannot skip letters; abd doesn't count.
        * may not contain the letters i, o, or l
        * must contain at least two different, non-overlapping
          pairs of letters, like aa, bb, or zz.

    Passwords must also be exactly eight letters long, but the
    clear assumption in the problem is that existing passwords
    are only ever that length, so there is no specific check
    to maintain the eight-character limit (as there is no
    specified response).
    """
    candidate = clean_bad_letters(current_password)
    if candidate == current_password:
        candidate = increment_password(candidate)
    while not validate_password(candidate):
        candidate = increment_password(candidate)
    return candidate


@pytest.mark.parametrize('invalid_pass', [
    'hijklmmn',
    'abbceffg',
    'abbcegjk',
    ])
def test_invalid_password(invalid_pass):
    assert not validate_password(invalid_pass)


@pytest.mark.parametrize('valid_pass', [
    'abcdffaa',
    'ghjaabcc',
    ])
def test_valid_password(valid_pass):
    assert validate_password(valid_pass)


@pytest.mark.parametrize('old,new', [
    ('abcdefgh', 'abcdffaa'),
    ('ghijklmn', 'ghjaabcc'),
    ])
def test_new_password(old, new):
    assert new_password(old) == new


if __name__ == '__main__':
    # Part one
    puzzle_input = 'vzbxkghb'
    part_one_pw = new_password(puzzle_input)
    print(part_one_pw)
    # Part two
    print(new_password(part_one_pw))
