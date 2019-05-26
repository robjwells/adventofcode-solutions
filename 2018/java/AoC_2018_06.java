import static org.junit.Assert.assertEquals;

import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.util.stream.Stream;

import org.junit.Test;

public class AoC_2018_06 extends Solution {
    static final int DAY = 6;
    static final String TITLE  = "Day 6: Chronal Coordinates";

    public static void main(String[] args) {
        System.out.println(TITLE);

        List<Coordinate> puzzleInput = loadPuzzleInputLines(DAY)
            .map(AoC_2018_06::parseInputLine)
            .collect(Collectors.toList());

        int partOneResult = largestArea(puzzleInput);
        assert partOneResult == 3604;
        System.out.printf("Part one: %d\n", partOneResult);

        int partTwoResult = safeRegionSize(puzzleInput, 10000);
        assert partTwoResult == 46563;
        System.out.printf("Part two: %d\n", partTwoResult);
    }

    static Coordinate parseInputLine(String inputLine) {
        String[] parts = inputLine.split(", ");
        return new Coordinate(Integer.parseInt(parts[0]), Integer.parseInt(parts[1]));
    }

    static Iterable<Integer> xRangeIterator(Bounds bounds) {
        return () -> IntStream.rangeClosed(bounds.xMin, bounds.xMax).iterator();
    }

    static Iterable<Integer> yRangeIterator(Bounds bounds) {
        return () -> IntStream.rangeClosed(bounds.yMin, bounds.yMax).iterator();
    }

    static int largestArea(List<Coordinate> coords) {
        HashSet<Coordinate> infinite = new HashSet<Coordinate>();
        Counter<Coordinate> closestCounter = new Counter<Coordinate>();
        Bounds bounds = new Bounds(coords);

        for (int x : xRangeIterator(bounds)) {
            for (int y : yRangeIterator(bounds)) {
                Coordinate current = new Coordinate(x, y);
                Coordinate[] closest = coords.stream()
                    .sorted(Comparator.comparing(current::distance))
                    .limit(2)
                    .toArray(Coordinate[]::new);
                if (closest[0].isEdge(bounds)) {
                    infinite.add(closest[0]);
                }
                if (closest[0].distance(current) == closest[1].distance(current)) {
                    continue;
                } else {
                    closestCounter.put(closest[0]);
                }
            }
        }
        infinite.stream().forEach(closestCounter::remove);
        return closestCounter.maxValue();
    }

    static int safeRegionSize(List<Coordinate> coords, int limit) {
        int totalSafe = 0;
        Bounds bounds = new Bounds(coords);
        for (int x : xRangeIterator(bounds)) {
            for (int y : yRangeIterator(bounds)) {
                Coordinate current = new Coordinate(x, y);
                if (coords.stream().mapToInt(current::distance).sum() < limit) {
                    totalSafe += 1;
                };
            }
        }
        return totalSafe;
    }

    @Test
    public void testLargestArea() {
        List<Coordinate> input = Stream.of("1, 1", "1, 6", "8, 3", "3, 4", "5, 5", "8, 9")
            .map(AoC_2018_06::parseInputLine)
            .collect(Collectors.toList());
        int expected = 17;
        int result = largestArea(input);
        assertEquals(expected, result);
    }

    @Test
    public void testSafeRegion() {
        List<Coordinate> input = Stream.of("1, 1", "1, 6", "8, 3", "3, 4", "5, 5", "8, 9")
            .map(AoC_2018_06::parseInputLine)
            .collect(Collectors.toList());
        int expected = 16;
        int distanceLimit = 32;
        int result = safeRegionSize(input, distanceLimit);
        assertEquals(expected, result);
    }

    @Test
    public void testCoordinateDistance() {
        Coordinate c1 = new Coordinate(1, 3);
        Coordinate c2 = new Coordinate(3, 5);
        assertEquals(4, c1.distance(c2));
        assertEquals(4, c2.distance(c1));
    }

    @Test
    public void testCounter() {
        String[] input = new String[] {"a", "b", "c", "b", "e"};
        Counter<String> counter = new Counter<String>();
        assertEquals(0, counter.get("a"));
        Stream.of(input).forEach(counter::put);
        assertEquals(2, counter.get("b"));
        assertEquals(0, counter.get("z"));
    }

}

class Bounds {
    int xMin;
    int yMin;
    int xMax;
    int yMax;

    Bounds(List<Coordinate> coordinates) {
        int[] xValues = coordinates.stream().mapToInt(Coordinate::getX).toArray();
        int[] yValues = coordinates.stream().mapToInt(Coordinate::getY).toArray();
        xMin = Arrays.stream(xValues).min().getAsInt();
        yMin = Arrays.stream(yValues).min().getAsInt();
        xMax = Arrays.stream(xValues).max().getAsInt();
        yMax = Arrays.stream(yValues).max().getAsInt();
    }
}

class Coordinate {
    int x;
    int y;

    Coordinate(int x, int y) {
        this.x = x;
        this.y = y;
    }

    int distance(Coordinate other) {
        return Math.abs(this.x - other.x) + Math.abs(this.y - other.y);
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }

    @Override
    public String toString() {
        return String.format("(%d, %d)", x, y);
    }

    int getX() {
        return x;
    }

    int getY() {
        return y;
    }

    boolean isEdge(Bounds bounds) {
        return x == bounds.xMin || x == bounds.xMax || y == bounds.yMin || y == bounds.yMax;
    }
}

class Counter<K>{
    HashMap<K, Integer> storage;

    Counter() {
        this.storage = new HashMap<K, Integer>();
    }

    void put(K key) {
        this.storage.put(key, this.storage.getOrDefault(key, 0) + 1);
    }

    int get(K key) {
        return this.storage.getOrDefault(key, 0);
    }

    int remove(K key) {
        return this.storage.remove(key);
    }

    int maxValue() {
        if (storage.values().size() == 0) {
            return 0;
        }
        return storage.values().stream().max(Comparator.naturalOrder()).get();
    }
}
