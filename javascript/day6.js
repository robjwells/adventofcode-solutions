#!/usr/local/bin/node

'use strict';
var fs = require('fs');

var instructions = fs.readFileSync('../day6_input.txt', 'utf-8')
    .trimRight()
    .split('\n')
    .map(line => line.match(/([\w ]+) (\d+,\d+) through (\d+,\d+)/))
    .map(match => [match[1],
                   match[2].split(',').map(num => parseInt(num, 10)),
                   match[3].split(',').map(num => parseInt(num, 10))]);
                   // The anonymous function feeding parseInt is
                   // necessary otherwise you end up with NaN.
                   // No, I don't know why.

// var grid = Array(1000).fill(Array(1000).fill(false));
// Can't do this. Array.fill reuses the same array reference,
// so changes to one affect all the filled arrays.
// This is like [[False] * 5] * 5 in Python
var grid = [];
for (var x = 0; x < 1000; x += 1) {
    grid[x] = [];
    for (var y = 0; y < 1000; y += 1) {
        // grid[x].push(false);     // Part one
        grid[x].push(0);
    }
}

var transformations = {
    // 'turn on': state => true,    // Part one
    'turn on': state => state + 1,  // Part two
    // 'turn off': state => false,  // Part one
    'turn off': state => state === 0 ? 0 : state -1,    // Part two
    // 'toggle': state => !state    // Part one
    'toggle': state => state + 2    // Part two
};

instructions.forEach(function (line) {
    var func = transformations[line[0]];
    var start_x = line[1][0];
    var start_y = line[1][1];
    var end_x = line[2][0];
    var end_y = line[2][1];

    for (var col = start_x; col < end_x + 1; col += 1) {
        for (var row = start_y; row < end_y + 1; row += 1) {
            grid[col][row] = func(grid[col][row]);
        }
    }
});

console.log([].concat.apply([], grid).reduce((prev, cur) => prev + cur))
