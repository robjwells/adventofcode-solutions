#!/usr/local/bin/node

'use strict';

var fs = require('fs');

let instructions = fs.readFileSync('../day1_input.txt', 'utf-8').split(''),
    instruction_values = {'(': 1, ')': -1};

var final_floor = instructions
    .map(function (char) {
        return instruction_values[char];
    })
    .reduce(function (prev, current) {
        return prev + current;
    });

console.log('Final floor:', final_floor);


// Part two

var floor = 0,
    basement_instruction = 0;

for (let char of instructions) {
    floor += instruction_values[char];
    basement_instruction += 1;
    if (floor === -1) {
        console.log('First basement instruction:', basement_instruction);
        break;
    }
}
