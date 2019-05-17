import java.util.HashMap;
import java.util.stream.IntStream;

public class AoC_2018_02 extends Solution {
    static int DAY = 2;
    static String TITLE = "Advent of Code 2018 Day 2: Inventory Management System";

    public static void main(String[] args) {
        System.out.println(TITLE);
        String[] boxIDs = loadPuzzleInputLines(DAY).toArray(String[]::new);

        int partOneResult = solvePartOne(boxIDs);
        assert partOneResult == 9633 : partOneResult;
        String partTwoResult = solvePartTwo(boxIDs);
        assert partTwoResult.equals("lujnogabetpmsydyfcovzixaw") : partTwoResult;

        System.out.printf("Part one: %d\n", partOneResult);
        System.out.printf("Part two: %s\n", partTwoResult);
    }

    static int solvePartOne(String[] boxIDs) {
        int countTwo = 0;
        int countThree = 0;
        for (String id : boxIDs) {
            HashMap<String, Integer> counter = countLetters(id);
            if (counter.values().contains(2)) {
                countTwo += 1;
            }
            if (counter.values().contains(3)) {
                countThree += 1;
            }
        }
        return countTwo * countThree;
    }

    static String solvePartTwo(String[] boxIDs) {
        int idLength = boxIDs[0].length();
        for (int fIdx = 0; fIdx < boxIDs.length; fIdx++) {
            String first = boxIDs[fIdx];
            for (int sIdx = fIdx + 1; sIdx < boxIDs.length; sIdx++) {
                String second = boxIDs[sIdx];
                int[] mismatched = IntStream.range(0, idLength)
                        .filter(idx -> first.charAt(idx) != second.charAt(idx))
                        .toArray();
                if (mismatched.length == 1) {
                    int avoidIdx = mismatched[0];
                    StringBuilder common = new StringBuilder();
                    for (int idx = 0; idx < idLength; idx++) {
                        if (idx != avoidIdx) {
                            common.append(first.charAt(idx));
                        }
                    }
                    return common.toString();
                }
            }
        }
        return "";  // Failure case to keep the compiler happy
    }

    static HashMap<String, Integer> countLetters(String candidate) {
        HashMap<String, Integer> counter = new HashMap<>();
        for (String character : candidate.split("")) {
            counter.put(character, counter.getOrDefault(character, 0) + 1);
        }
        return counter;
    }
}
