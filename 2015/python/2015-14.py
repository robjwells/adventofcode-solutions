#!/usr/local/bin/python3

from collections import defaultdict
import pathlib
import re

input_file = pathlib.Path(__file__).parent.parent.joinpath('day14_input.txt')


def calc_distance(race_time, speed, flight_time, rest_time):
    full_period = flight_time + rest_time
    periods_completed, remaining = divmod(race_time, full_period)
    distance = speed * flight_time * periods_completed
    if remaining >= flight_time:
        distance += flight_time * speed
    else:
        distance += remaining * speed
    return distance


def parse_input(text):
    regex = re.compile(
        r'''
        ^
        (?P<name>\w+) \D+
        (?P<speed>\d+) \D+
        (?P<flight>\d+) \D+
        (?P<rest>\d+) \D+
        $''',
        flags=re.VERBOSE)
    reindeer_dict = dict()
    for line in text.splitlines():
        match = regex.match(line)
        name = match['name']
        reindeer_dict[name] = match.groupdict().copy()
        del reindeer_dict[name]['name']
        for k in reindeer_dict[name]:
            reindeer_dict[name][k] = int(reindeer_dict[name][k])
    return reindeer_dict


def test_calc():
    """Test calc_distance using the sample data

    Comet can fly 14 km/s for 10s, but then must rest for 127s.
    Dancer can fly 16 km/s for 11s, but then must rest for 162s.

    After 1000 seconds, Comet is at 1120km, Dancer at 1056km.
    """
    assert calc_distance(1000, 14, 10, 127) == 1120
    assert calc_distance(1000, 16, 11, 162) == 1056


def test_parse():
    sample_input = '''\
Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'''
    assert parse_input(sample_input) == dict(
        Comet=dict(speed=14, flight=10, rest=127),
        Dancer=dict(speed=16, flight=11, rest=162))


if __name__ == '__main__':
    reindeers = parse_input(input_file.read_text())

    race_time = 2503

    # Part one
    print(max([
        calc_distance(race_time, reindeers[k]['speed'],
                      reindeers[k]['flight'], reindeers[k]['rest'])
        for k in reindeers
        ]))

    # Part two
    reindeer_scores = defaultdict(int)
    for time in range(1, race_time + 1):
        distances = defaultdict(int)
        for r in reindeers:
            distances[r] = calc_distance(
                time, reindeers[r]['speed'],
                reindeers[r]['flight'], reindeers[r]['rest'])
        ordered = sorted(distances.items(), key=lambda x: x[1], reverse=True)
        top_score = ordered[0][1]
        leaders = [r for r, d in ordered if d == top_score]
        for r in leaders:
            reindeer_scores[r] += 1
    print(max(reindeer_scores.items(), key=lambda x: x[1]))
