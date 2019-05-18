import static java.util.Map.entry;

import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

class AoC_2018_03 extends Solution {
    static int DAY = 3;
    static String TITLE = "Advent of Code 2018 Day 3: No Matter How You Slice It";

    public static void main(String[] args) {
        System.out.println(TITLE);

        // Tests
        Test_2018_03.testClaimParses();
        Test_2018_03.testOverlapMap();
        Test_2018_03.testFindUncontested();

        // Solutions
        String[] claimStrings = loadPuzzleInputLines(DAY).toArray(String[]::new);
        Claim[] claims = Arrays.stream(claimStrings).map(Claim::new).toArray(Claim[]::new);
        HashMap<String, HashSet<Integer>> overlapMap = makeOverlapMap(claims);

        long partOneResult = solvePartOne(overlapMap);
        assert partOneResult == 100261;
        System.out.printf("Part one: %d\n", partOneResult);

        int partTwoResult = solvePartTwo(claims, overlapMap);
        assert partTwoResult == 251;
        System.out.printf("Part two: %d\n", partTwoResult);
    }

    static long solvePartOne(HashMap<String, HashSet<Integer>> overlapMap) {
        return overlapMap.values().stream()
            .filter(claimSet -> claimSet.size() > 1)
            .count();
    }

    static int solvePartTwo(Claim[] claims, HashMap<String, HashSet<Integer>> overlapMap) {
        int[] uncontested = findUncontestedClaims(claims, overlapMap);
        assert uncontested.length == 1;
        return uncontested[0];
    }

    static String pairToString(int x, int y) {
        return String.format("%d,%d", x, y);
    }

    static HashMap<String, HashSet<Integer>> makeOverlapMap(Claim[] claims) {
        HashMap<String, HashSet<Integer>> overlap = new HashMap<>();
        for (Claim claim : claims) {
            int rightLimit = claim.fromLeft + claim.width;
            int bottomLimit = claim.fromTop + claim.height;
            for (int x = claim.fromLeft; x < rightLimit; x++) {
                for (int y = claim.fromTop; y < bottomLimit; y++) {
                    String key = pairToString(x, y);
                    if (overlap.containsKey(key)) {
                        overlap.get(key).add(claim.id);
                    } else {
                        HashSet<Integer> newSet = new HashSet<Integer>();
                        newSet.add(claim.id);
                        overlap.put(key, newSet);
                    }
                }
            }
        }
        return overlap;
    }

    static int[] findUncontestedClaims(Claim[] claims, HashMap<String, HashSet<Integer>> overlapMap) {
        Set<Integer> claimIds = Arrays.stream(claims)
            .map(claim -> claim.id)
            .collect(Collectors.toSet());
        overlapMap.values().stream()
            .filter(claimSet -> claimSet.size() > 1)
            .forEach(claimSet -> claimSet.forEach(claimIds::remove));
        return claimIds.stream().mapToInt(i -> i).toArray();
    }

}

class Claim {
    private static Pattern claimPattern = Pattern.compile(
        "^#(\\d+) @ (\\d+),(\\d+): (\\d+)x(\\d+)$"
    );

    int id;
    int fromLeft;
    int fromTop;
    int width;
    int height;

    Claim(String claimString) {
        Matcher claimMatcher = claimPattern.matcher(claimString);
        if (!claimMatcher.matches()) {
            throw new IllegalArgumentException("Invalid claim string.");
        }
        this.id = Integer.parseInt(claimMatcher.group(1));
        this.fromLeft = Integer.parseInt(claimMatcher.group(2));
        this.fromTop = Integer.parseInt(claimMatcher.group(3));
        this.width = Integer.parseInt(claimMatcher.group(4));
        this.height = Integer.parseInt(claimMatcher.group(5));
    }
}

class Test_2018_03 {
    static void testClaimParses() {
        String input = "#123 @ 3,2: 5x4";
        Claim claim = new Claim(input);
        assert claim.id == 123;
        assert claim.fromLeft == 3;
        assert claim.fromTop == 2;
        assert claim.width == 5;
        assert claim.height == 4;
    }

    /**
     * Check provided test case, where the overlap grid is as follows:
     *
     * <pre>
     * ........
     * ...2222.
     * ...2222.
     * .11XX22.
     * .11XX22.
     * .111133.
     * .111133.
     * ........
     * </pre>
     */
    static void testOverlapMap() {
        String[] claimStrings = new String[] {
            "#1 @ 1,3: 4x4",
            "#2 @ 3,1: 4x4",
            "#3 @ 5,5: 2x2",
        };
        Claim[] claims = Arrays.stream(claimStrings).map(Claim::new).toArray(Claim[]::new);
        HashMap<String, HashSet<Integer>> result = AoC_2018_03.makeOverlapMap(claims);
        Set<Map.Entry<String, HashSet<Integer>>> resultEntries = result.entrySet();
        Set<Map.Entry<String, Integer>> counted = resultEntries.stream()
            .map(resultEntry -> entry(resultEntry.getKey(), resultEntry.getValue().size()))
            .collect(Collectors.toSet());

        Map<String, Integer> expected = Map.ofEntries(
            entry("1,3", 1), entry("1,4", 1), entry("1,5", 1), entry("1,6", 1),
            entry("2,3", 1), entry("2,4", 1), entry("2,5", 1), entry("2,6", 1),
            entry("3,1", 1), entry("3,2", 1), entry("3,3", 2), entry("3,4", 2), entry("3,5", 1), entry("3,6", 1),
            entry("4,1", 1), entry("4,2", 1), entry("4,3", 2), entry("4,4", 2), entry("4,5", 1), entry("4,6", 1),
            entry("5,1", 1), entry("5,2", 1), entry("5,3", 1), entry("5,4", 1), entry("5,5", 1), entry("5,6", 1),
            entry("6,1", 1), entry("6,2", 1), entry("6,3", 1), entry("6,4", 1), entry("6,5", 1), entry("6,6", 1)
        );
        assert counted.equals(expected.entrySet());
    }

    static void testFindUncontested() {
        String[] claimStrings = new String[] {
            "#1 @ 1,3: 4x4",
            "#2 @ 3,1: 4x4",
            "#3 @ 5,5: 2x2",
        };
        Claim[] claims = Arrays.stream(claimStrings).map(Claim::new).toArray(Claim[]::new);
        HashMap<String, HashSet<Integer>> overlapMap = AoC_2018_03.makeOverlapMap(claims);
        int[] result = AoC_2018_03.findUncontestedClaims(claims, overlapMap);
        assert Arrays.equals(result, new int[] { 3 });
    }
}
