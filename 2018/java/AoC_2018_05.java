import java.util.ArrayDeque;
import java.util.Iterator;
import java.util.stream.Collectors;

class AoC_2018_05 extends Solution {
    static final int DAY = 5;
    static final String TITLE = "Advent of Code 2018 Day 5: Alchemical Reduction";

    public static void main(String[] args) {
        System.out.println(TITLE);

        // Tests
        testStringsShouldEliminate();
        testReducePolymer();

        // Solve
        String puzzleInput = loadPuzzleInputLines(DAY).collect(Collectors.joining());
        int partOneResult = solvePartOne(puzzleInput);
        assert partOneResult == 11546;
        System.out.printf("Part one: %d\n", partOneResult);
    }

    static int solvePartOne(String puzzleInput) {
        return reducePolymer(puzzleInput).length();
    }

    static String reducePolymer(String polymer) {
        ArrayDeque<String> stack = new ArrayDeque<>(polymer.length());
        for (String c : polymer.split("")) {
            String stackTop = stack.peekLast();
            if (stackTop != null && stringsShouldEliminate(c, stackTop)) {
                stack.removeLast();
            } else {
                stack.add(c);
            }
        }
        StringBuilder builder = new StringBuilder();
        for (String c : stack) {
            builder.append(c);
        }
        return builder.toString();
    }

    static boolean stringsShouldEliminate(String first, String second) {
        return first.equalsIgnoreCase(second) && !first.equals(second);
    }

    static void testReducePolymer() {
        String input = "dabAcCaCBAcCcaDA";
        String expected = "dabCBAcaDA";
        String result = reducePolymer(input);
        assert result.equals(expected) : result;
    }

    static void testStringsShouldEliminate() {
        assert stringsShouldEliminate("a", "A");
        assert !stringsShouldEliminate("a", "a");
        assert stringsShouldEliminate("C", "c");
        assert !stringsShouldEliminate("C", "C");
    }

}
