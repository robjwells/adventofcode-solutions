package com.robjwells.adventofcode2015;

import java.util.ArrayList;

public class Day01 extends Solution2015 {
    @Override
    public int getDay() {
        return 1;
    }

    @Override
    public String getTitle() {
        return "Not Quite Lisp";
    }

    @Override
    public String run(String input) {
        return formatReport(solvePartOne(input), solvePartTwo(input));
    }

    static int instructionToFloorDelta(int instruction) {
        return instruction == '(' ? 1 : -1;
    }

    static int solvePartOne(String input) {
        return input.chars().map(Day01::instructionToFloorDelta).sum();
    }

    static int solvePartTwo(String input) {
        int floor = 0;
        int instruction = 0;
        for (int delta : input.chars().map(Day01::instructionToFloorDelta).toArray()) {
            floor += delta;
            instruction += 1;
            if (floor == -1) {
                return instruction;
            }
        }
        throw new RuntimeException("Never entered basement; unreachable given puzzle input.");
    }
}
