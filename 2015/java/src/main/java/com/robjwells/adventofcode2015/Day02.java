package com.robjwells.adventofcode2015;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class Day02 extends Solution2015 {
    @Override
    public int getDay() {
        return 2;
    }

    @Override
    public String getTitle() {
        return "I Was Told There Would Be No Math";
    }

    @Override
    public String run(String input) {
        List<Present> parsed = parseInput(input);
        return formatReport(solvePartOne(parsed), solvePartTwo(parsed));
    }

    static class Present {
        private int length, width, height;
        private int[] ordered;

        Present(int length, int width, int height) {
            this.length = length;
            this.width = width;
            this.height = height;
            int[] dims = {length, width, height};
            Arrays.sort(dims);
            this.ordered = dims;
        }

        int surfaceArea() {
            return (2 * length * width +
                    2 * width * height +
                    2 * height * length
            );
        }

        int areaOfSmallestSide() {
            return ordered[0] * ordered[1];
        }

        int totalWrappingPaperNeeded() {
            return surfaceArea() + areaOfSmallestSide();
        }

        int smallestPerimeter() {
            return 2 * ordered[0] + 2 * ordered[1];
        }

        int volume() {
            return ordered[0] * ordered[1] * ordered[2];
        }

        int totalRibbonNeeded() {
            return smallestPerimeter() + volume();
        }

    }

    static Present parseInputLine(String line) {
        int[] dims = Arrays.stream(line.split("x")).mapToInt(Integer::parseInt).toArray();
        assert dims.length == 3;
        return new Present(dims[0], dims[1], dims[2]);
    }

    static List<Present> parseInput(String input) {
        return Arrays.stream(input.trim().split("\n"))
                .map(Day02::parseInputLine)
                .collect(Collectors.toList());
    }

    static int solvePartOne(List<Present> presents) {
        return presents.stream().mapToInt(Present::totalWrappingPaperNeeded).sum();
    }

    static int solvePartTwo(List<Present> presents) {
        return presents.stream().mapToInt(Present::totalRibbonNeeded).sum();
    }
}
