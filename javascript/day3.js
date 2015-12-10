#!/usr/local/bin/node

'use strict';
var fs = require('fs');

var instructions = fs.readFileSync('../day3_input.txt', 'utf-8')
    .trimRight()
    .split('');


var Point = function (x, y) {
    return {
        'x': x,
        'y': y,
        'toString': function () {
            // This is needed to store the Points in a set, because we don't
            // have the luxury of Python's namedtuples and JavaScript Sets
            // treat all objects as unequal.
            return [this.x, this.y].join(',');
        }
    };
};


var new_location = function (current, move) {
    var movements = {
        '^': current => new Point(current.x, current.y + 1),
        'v': current => new Point(current.x, current.y - 1),
        '>': current => new Point(current.x + 1, current.y),
        '<': current => new Point(current.x - 1, current.y)
    };
    return movements[move](current)
};


// Part one

var current = new Point(0, 0);
var visited = new Set([current.toString()]);

instructions.forEach(function (move) {
    current = new_location(current, move);
    visited.add(current.toString());
});

console.log('At least one present with just Santa:', visited.size)


// Part two

var santa = new Point(0, 0);
var robot = new Point(0, 0);
var both_visited = new Set([santa.toString(), robot.toString()]);

instructions.forEach(function (move, idx) {
    if (idx % 2 === 0) {
        santa = new_location(santa, move);
        both_visited.add(santa.toString());
    } else {
        robot = new_location(robot, move);
        both_visited.add(robot.toString());
    }
});

console.log('At least one present with Santa and robot:', both_visited.size)
