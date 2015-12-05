#!/usr/local/bin/node

'use strict';

var fs = require('fs');

var instructions = fs.readFileSync('../day2_input.txt', 'utf-8')
    .trimRight()
    .split('\n')
    .map(function (el) {
        return el
            .split('x')
            .map(function (el) {
                return parseInt(el, 10);
            });
    });

var surface_area = function (l, w, h) {
    return (2 * l * w) + (2 * w * h) + (2 * h * l);
};
var smallest_side = function (l, w, h) {
    return Math.min((l * w), (w * h), (h * l));
};


// Part one

var wrapping_paper = 0;
instructions.forEach(function (dimensions) {
    wrapping_paper += surface_area.apply(null, dimensions);
    wrapping_paper += smallest_side.apply(null, dimensions);
});

console.log('wrapping paper:', wrapping_paper);

// Part two

var ribbon = 0;
instructions.forEach(function (dimensions) {
    var dimensions_copy = dimensions.slice();  // JS only sorts in place
    dimensions_copy.sort(function (a, b) {
        // JS compares numbers by their string representation by default.
        // You have to provide your own comparison function to compare
        // numbers as numbers. JavaScript is mad.
        return a - b;
    });

    var s1 = dimensions_copy[0],
        s2 = dimensions_copy[1],
        s3 = dimensions_copy[2];
    ribbon += (2 * s1) + (2 * s2);
    ribbon += s1 * s2 * s3;
});

console.log('ribbon:', ribbon);
