import java.util.regex.Matcher;
import java.util.regex.Pattern;

class AoC_2018_03 extends Solution {
    static int DAY = 3;
    static String TITLE = "Day 3: No Matter How You Slice It";

    public static void main(String[] args) {
        // Tests
        testClaimParses();
    }

    static void testClaimParses() {
        String input = "#123 @ 3,2: 5x4";
        Claim claim = new Claim(input);
        assert claim.id == 123;
        assert claim.fromLeft == 3;
        assert claim.fromTop == 2;
        assert claim.width == 5;
        assert claim.height == 4;
    }

    static class Claim {
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
}
