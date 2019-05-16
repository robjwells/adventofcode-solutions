import java.util.Arrays;
import java.util.HashSet;

public class AoC_2018_01 extends Solution {
    static int DAY = 1;
    static String TITLE = "Advent of Code 2018 Day 1: Chronal Calibration";

    public static void main(String[] args) {
        System.out.println(TITLE);
        int[] deltas = loadPuzzleInputLines(DAY).mapToInt(Integer::parseInt).toArray();
        solvePartOne(deltas);
        solvePartTwo(deltas);
    }

    private static void solvePartOne(int[] deltas) {
        int sum = Arrays.stream(deltas).sum();
        System.out.printf("Part one: %d\n", sum);
    }

    private static void solvePartTwo(int[] deltas) {
        HashSet<Integer> frequencies = new HashSet<>();
        int sum = 0;
        while (true) {
            for (int change : deltas) {
                sum += change;
                if (frequencies.contains(sum)) {
                    System.out.printf("Part two: %d\n", sum);
                    return;
                }
                frequencies.add(sum);
            }
        }
    }

}
