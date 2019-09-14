package com.robjwells.adventofcode2015;

import java.util.Arrays;

import static com.robjwells.adventofcode2015.Utils.accumulate;
import static com.robjwells.adventofcode2015.Utils.enumerate;

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
        int[] parsed = parseInput(input);
        return formatReport(solvePartOne(parsed), solvePartTwo(parsed));
    }

    static int[] parseInput(String input) {
        return input.chars().map(c -> c == '(' ? 1 : -1).toArray();
    }

    static int solvePartOne(int[] deltas) {
        return Arrays.stream(deltas).sum();
    }

    static int solvePartTwo(int[] deltas) {
        var floorsReached = accumulate(Arrays.stream(deltas).iterator(), Math::addExact);
        return enumerate(floorsReached, 1)
                .filter(e -> e.element == -1)
                .map(e -> e.index)
                .findFirst()
                .get();
    }
}
