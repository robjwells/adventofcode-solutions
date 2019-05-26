import java.util.ArrayDeque;
import java.util.Arrays;
import java.util.Comparator;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

class AoC_2018_05 extends Solution {
    static final int DAY = 5;
    static final String TITLE = "Advent of Code 2018 Day 5: Alchemical Reduction";

    public static void main(String[] args) {
        System.out.println(TITLE);

        // Tests
        testStringsShouldEliminate();
        testReducePolymer();
        testUniqueCharacters();
        testBestReduction();

        // Solve
        String puzzleInput = loadPuzzleInputLines(DAY).collect(Collectors.joining());
        int partOneResult = solvePartOne(puzzleInput);
        assert partOneResult == 11546;
        System.out.printf("Part one: %d\n", partOneResult);
        int partTwoResult = solvePartTwo(puzzleInput);
        assert partTwoResult == 5124;
        System.out.printf("Part two: %d\n", partTwoResult);
    }

    static int solvePartOne(String puzzleInput) {
        return reducePolymer(puzzleInput).length();
    }

    static int solvePartTwo(String puzzleInput) {
        return bestReduction(puzzleInput).length();
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

    static Stream<String> uniqueCharacters(String input) {
        return Arrays.stream(input.split(""))
            .map(s -> s.toLowerCase())
            .distinct();
    }

    static String bestReduction(String input) {
        return uniqueCharacters(input)
            .map(character -> input.replaceAll(character + "|" + character.toUpperCase(), ""))
            .map(AoC_2018_05::reducePolymer)
            .min(Comparator.comparing(String::length))
            .get();
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

    static void testUniqueCharacters() {
        assert uniqueCharacters("abcABC")
            .collect(Collectors.toSet())
            .equals(Set.of("a", "b", "c"));
        assert uniqueCharacters("A")
            .collect(Collectors.toSet())
            .equals(Set.of("a")); // lowercases
        assert uniqueCharacters("BC")
            .collect(Collectors.toSet())
            .equals(Set.of("b", "c")); // lowercases
    }

    static void testBestReduction() {
        String input = "dabAcCaCBAcCcaDA";
        String expected = "daDA";
        assert bestReduction(input).equals(expected);
    }

}
