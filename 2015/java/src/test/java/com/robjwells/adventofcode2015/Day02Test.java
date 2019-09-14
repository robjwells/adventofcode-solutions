package com.robjwells.adventofcode2015;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

class Day02Test {

    @ParameterizedTest
    @CsvSource({
            "2x3x4, 52, 6, 58",
            "1x1x10, 42, 1, 43"
    })
    void testPartOnePresentProperties(String input, int surfaceArea, int smallestSideArea, int total) {
        Day02.Present p = Day02.parseInputLine(input);
        assertEquals(surfaceArea, p.surfaceArea());
        assertEquals(smallestSideArea, p.areaOfSmallestSide());
        assertEquals(total, p.totalWrappingPaperNeeded());
    }

    @Test
    void test_solvePartOne_knownResult() {
        assertEquals(
                1588178,
                Day02.solvePartOne(Day02.parseInput(Utils.loadPuzzleInput(2015, 2)))
        );
    }

    @ParameterizedTest
    @CsvSource({
            "2x3x4, 10, 24, 34",
            "1x1x10, 4, 10, 14"
    })
    void testPartTwoPresentProperties(String input, int smallestPerimeter, int volume, int total) {
        Day02.Present p = Day02.parseInputLine(input);
        assertEquals(smallestPerimeter, p.smallestPerimeter());
        assertEquals(volume, p.volume());
        assertEquals(total, p.totalRibbonNeeded());
    }

    @Test
    void test_solvePartTwo() {
        assertEquals(
                3783758,
                Day02.solvePartTwo(Day02.parseInput(Utils.loadPuzzleInput(2015, 2)))
        );
    }
}
