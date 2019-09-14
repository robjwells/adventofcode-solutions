package com.robjwells.adventofcode2015;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;

class Day01Test {

    @Test
    void testParseInput() {
        assertArrayEquals(
                new int[]{1, -1},
                Day01.parseInput("()")
        );
    }

    @ParameterizedTest
    @CsvSource({
            "(()), 0",
            "()(), 0",
            "(((,  3",
            "(()(()(, 3",
            "))(((((, 3",
            "()), -1",
            "))(, -1",
            "))), -3",
            ")())()), -3"
    })
    void solvePartOne_SampleInput(String input, int floorReached) {
        assertEquals(floorReached, Day01.solvePartOne(Day01.parseInput(input)));
    }

    @ParameterizedTest
    @CsvSource({
            "), 1",
            "()()), 5"
    })
    void solvePartTwo_SampleInput(String input, int instructionThatEntersBasement) {
        assertEquals(instructionThatEntersBasement, Day01.solvePartTwo(Day01.parseInput(input)));
    }

    @Test
    void solvePartOne_CorrectWithMyInput() {
        int[] parsed = Day01.parseInput(Utils.loadPuzzleInput(2015, 1));
        assertEquals(280, Day01.solvePartOne(parsed));
    }

    @Test
    void solvePartTwo_CorrectWithMyInput() {
        int[] parsed = Day01.parseInput(Utils.loadPuzzleInput(2015, 1));
        assertEquals(1797, Day01.solvePartTwo(parsed));
    }

}
