import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.HashSet;

public class AoC_2018_01 {
    public static void main(String[] args) {
        Path inputFilePath = Path.of("../input/2018-01.txt");
        try {
            int[] deltas = Files.lines(inputFilePath).mapToInt(Integer::parseInt).toArray();
            solvePartOne(deltas);
            solvePartTwo(deltas);
        } catch (IOException exc) {
            exc.printStackTrace();
        }
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
