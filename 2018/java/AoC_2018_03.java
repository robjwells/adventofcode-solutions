import java.util.Arrays;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Map;
import static java.util.Map.entry;

class AoC_2018_03 extends Solution {
    static int DAY = 3;
    static String TITLE = "Day 3: No Matter How You Slice It";

    public static void main(String[] args) {
        // Tests
        Test_2018_03.testClaimParses();
        Test_2018_03.testOverlapMap();
    }

    static String pairToString(int x, int y) {
        return String.format("%d,%d", x, y);
    }

    static HashMap<String, Integer> makeOverlapMap(String[] claimStrings) {
        HashMap<String, Integer> overlap = new HashMap<>();
        Claim[] claims = Arrays.stream(claimStrings).map(Claim::new).toArray(Claim[]::new);
        for (Claim claim : claims) {
            int rightLimit = claim.fromLeft + claim.width;
            int bottomLimit = claim.fromTop + claim.height;
            for (int x = claim.fromLeft; x < rightLimit; x++) {
                for (int y = claim.fromTop; y < bottomLimit; y++) {
                    String key = pairToString(x, y);
                    overlap.put(
                        key,
                        overlap.getOrDefault(key, 0) + 1
                    );
                }
            }
        }
        return overlap;
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

    Claim(int id, int fromLeft, int fromTop, int width, int height) {
        this.id = id;
        this.fromLeft = fromLeft;
        this.fromTop = fromTop;
        this.width = width;
        this.height = height;
    }

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
        String[] claims = new String[] {
            "#1 @ 1,3: 4x4",
            "#2 @ 3,1: 4x4",
            "#3 @ 5,5: 2x2",
        };
        HashMap<String, Integer> result = AoC_2018_03.makeOverlapMap(claims);
        Map<String, Integer> expected = Map.ofEntries(
            entry("1,3", 1), entry("1,4", 1), entry("1,5", 1), entry("1,6", 1),
            entry("2,3", 1), entry("2,4", 1), entry("2,5", 1), entry("2,6", 1),
            entry("3,1", 1), entry("3,2", 1), entry("3,3", 2), entry("3,4", 2), entry("3,5", 1), entry("3,6", 1),
            entry("4,1", 1), entry("4,2", 1), entry("4,3", 2), entry("4,4", 2), entry("4,5", 1), entry("4,6", 1),
            entry("5,1", 1), entry("5,2", 1), entry("5,3", 1), entry("5,4", 1), entry("5,5", 1), entry("5,6", 1),
            entry("6,1", 1), entry("6,2", 1), entry("6,3", 1), entry("6,4", 1), entry("6,5", 1), entry("6,6", 1)
        );
        assert expected.equals(result);
    }
}
