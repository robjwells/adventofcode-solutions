#!/usr/local/bin/python3

puzzle_input = 1113122113

def parse_input(sequence):
    char, *text = str(sequence)
    count = 1
    output = ''
    for new_char in text:
        if new_char == char:
            count += 1
        else:
            output += str(count) + char
            char = new_char
            count = 1
    else:
        # This is needed to ensure final digit is accounted for
        output += str(count) + char
    return output

def test_parse_input():
    assert parse_input('211') == '1221'

if __name__ == '__main__':
    for x in range(50):
        if x == 40:
            print(len(puzzle_input))
        puzzle_input = parse_input(puzzle_input)
    print(len(puzzle_input))
