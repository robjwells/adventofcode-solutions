import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Objects;
import java.util.stream.Stream;

import org.junit.Test;

public class AoC_2018_06 extends Solution {
    static final int DAY = 6;
    static final String TITLE  = "Day 6: Chronal Coordinates";

    public static void main(String[] args) {
        System.out.println(TITLE);

        Stream<String> puzzleInput = loadPuzzleInputLines(DAY);
        int partOneResult = largestArea(puzzleInput);
        System.out.printf("Part one: %d\n", partOneResult);
    }

    static Coordinate parseInputLine(String inputLine) {
        String[] parts = inputLine.split(", ");
        return new Coordinate(Integer.parseInt(parts[0]), Integer.parseInt(parts[1]));
    }

    static int largestArea(Stream<String> input) {
        ArrayList<Coordinate> coords = new ArrayList<>();
        input.map(AoC_2018_06::parseInputLine).forEach(coords::add);
        HashSet<Coordinate> infinite = new HashSet<Coordinate>();

        int minX = coords.stream().map(Coordinate::getX).min(Comparator.naturalOrder()).get();
        int maxX = coords.stream().map(Coordinate::getX).max(Comparator.naturalOrder()).get();
        int minY = coords.stream().map(Coordinate::getY).min(Comparator.naturalOrder()).get();
        int maxY = coords.stream().map(Coordinate::getY).max(Comparator.naturalOrder()).get();

        Counter<Coordinate> closestCounter = new Counter<Coordinate>();

        for (int x = minX; x <= maxX; x++) {
            for (int y = minY; y <= maxY; y++) {
                Coordinate current = new Coordinate(x, y);
                Coordinate[] closest = coords.stream()
                    .sorted(Comparator.comparing(other -> current.distance(other)))
                    .limit(2)
                    .toArray(Coordinate[]::new);

                if (closest[0].isEdge(minX, maxX, minY, maxY)) {
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

    @Test
    public void testLargestArea() {
        Stream<String> input = Stream.of("1, 1", "1, 6", "8, 3", "3, 4", "5, 5", "8, 9");
        int expected = 17;
        int result = largestArea(input);
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

    boolean isEdge(int xMin, int xMax, int yMin, int yMax) {
        return x == xMin || x == xMax || y == yMin || y == yMax;
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
