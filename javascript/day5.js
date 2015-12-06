#!/usr/local/bin/node

'use strict';
var fs = require('fs');

var instructions = fs.readFileSync('../day5_input.txt', 'utf-8')
    .trimRight()
    .split('\n');


// Part one

var is_nice = function (string) {
    var vowels = new Set('aeiou');
    var string_array = Array.from(string.toLowerCase());
    var enough_vowels = string_array.filter(c => vowels.has(c)).length >= 3;

    var no_forbidden_strings = string.search(/ab|cd|pq|xy/) === -1;
    var double_character = string.search(/(.)\1/) !== -1;

    return enough_vowels && no_forbidden_strings && double_character;
};

console.log('Nice strings:', instructions.filter(is_nice).length);


// Part two

var new_nice = function (string) {
    var repeated_pair = string.search(/(.{2}).*\1/) !== -1;
    var repeated_one_apart = string.search(/(.).\1/) !== -1;
    return repeated_pair && repeated_one_apart;
};

console.log('New nice strings:', instructions.filter(new_nice).length);
