#!/usr/local/bin/python3

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
    if re.match(r'^[^iol]+$', password):
        return password
    cut_pos = re.search(r'[iol]', password).start()
    letter = password[cut_pos]
    new_letter = {'i': 'j', 'l': 'm', 'o': 'p'}[letter]
    extra_as = len(password[cut_pos:]) - 1
    return password[:cut_pos] + new_letter + 'a' * extra_as


def increment_letter(letter):
    ok_letters = 'abcdefghjkmnpqrstuvwxyz'
    cur_index = ok_letters.index(letter)
    if cur_index == len(ok_letters) - 1:
        new_index = 0
    else:
        new_index = cur_index + 1
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
