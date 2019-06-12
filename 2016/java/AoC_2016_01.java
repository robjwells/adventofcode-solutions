import static org.junit.Assert.assertEquals;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.junit.Test;


public class AoC_2016_01 extends Solution {
    static final String TITLE = "Advent of Code 2016, Day 1: No Time for a Taxicab";
    static final int DAY = 1;

    public static void main(String[] args) {
        List<Instruction> instructions = Solution.loadPuzzleInputLines(DAY)
            .flatMap(line -> Arrays.stream(line.split(",")))
            .map(String::trim)
            .map(Instruction::new)
            .collect(Collectors.toList());

        // Solution
        System.out.println(TITLE);
        int partOneSolution = solvePartOne(instructions);
        assert 307 == partOneSolution : "solvePartOne() has failed regression test";
        System.out.printf("Part one: %s\n", partOneSolution);

        int partTwoSolution = solvePartTwo(instructions);
        assert 165 == partTwoSolution : "solvePartTwo() has failed regression test";
        System.out.printf("Part two: %s\n", partTwoSolution);
    }

    static int solvePartOne(List<Instruction> instructions) {
        Actor position = new Actor();
        instructions.forEach(position::move);
        return position.distanceFromOrigin();
    }

    static int solvePartTwo(List<Instruction> instructions) {
        LoggingActor position = new LoggingActor();
        try {
            instructions.forEach(position::move);
        } catch (LoggingActor.VisitedTwice exc) {
            return position.distanceFromOrigin();
        }
        return 0;
    }

    private static class Actor {
        private int x = 0;
        private int y = 0;

        Direction currentDirection = Direction.NORTH;

        void move(Instruction instruction) {
            currentDirection = currentDirection.turn(instruction.getTurn());
            move(instruction.getBlocks());
        }

        void move(int steps) {
            switch (currentDirection) {
            case NORTH:
                moveNorth(steps);
                break;
            case EAST:
                moveEast(steps);
                break;
            case SOUTH:
                moveSouth(steps);
                break;
            case WEST:
                moveWest(steps);
                break;
            }
        }

        void moveNorth  (int steps) { y += steps; }
        void moveEast   (int steps) { x += steps; }
        void moveSouth  (int steps) { y -= steps; }
        void moveWest   (int steps) { x -= steps; }

        int distanceFrom(int otherX, int otherY) {
            return Math.abs(x - otherX) + Math.abs(y - otherY);
        }

        int distanceFromOrigin() {
            return distanceFrom(0, 0);
        }

        @Override
        public String toString() {
            return String.format("(%d, %d)", x, y);
        }

    }

    static class LoggingActor extends Actor {
        private ArrayList<String> visited = new ArrayList<>();

        @Override
        void move(Instruction instruction) {
            currentDirection = currentDirection.turn(instruction.getTurn());
            int steps = instruction.getBlocks();
            while (steps > 0) {
                move(1);
                if (visited.contains(toString())) {
                    throw new VisitedTwice(toString());
                }
                visited.add(toString());
                steps--;
            }
        }

        static class VisitedTwice extends RuntimeException {
            VisitedTwice(String message) {
                super(message);
            }
        };
    }

    private static class Instruction {
        private final Turn turn;
        private final int blocks;

        Instruction(String instructionString) {
            this.turn = instructionString.charAt(0) == 'L' ? Turn.LEFT : Turn.RIGHT;
            this.blocks = Integer.parseInt(instructionString.substring(1));
        }

        public Turn getTurn() {
            return turn;
        }

        public int getBlocks() {
            return blocks;
        }

        @Override
        public String toString() {
            return String.format("<%s, %d>", turn, blocks);
        }

    }

    private enum Turn {
        LEFT(-1), RIGHT(1);

        private final int indexDelta;

        Turn(int indexDelta) {
            this.indexDelta = indexDelta;
        }

        public int getIndexDelta() {
            return indexDelta;
        }
    };

    private enum Direction {
        NORTH(0), EAST(1), SOUTH(2), WEST(3);

        private static Map<Integer, Direction> map = new HashMap<>();
        static {
            map.put(0, NORTH);
            map.put(1, EAST);
            map.put(2, SOUTH);
            map.put(3, WEST);
        }

        private final int directionIndex;

        Direction(int directionIndex) {
            this.directionIndex = directionIndex;
        }

        Direction turn(Turn t) {
            return map.get(Math.floorMod((directionIndex + t.getIndexDelta()), 4));
        }
    }

    @Test
    public void testPartOneDistanceOne() {
        List<Instruction> input = List.of(
            new Instruction("R2"),
            new Instruction("L3")
        );
        Actor position = new Actor();
        input.forEach(position::move);
        assertEquals(5, position.distanceFromOrigin());
    }

    @Test
    public void testPartOneDistanceTwo() {
        List<Instruction> input = List.of(
            new Instruction("R2"),
            new Instruction("R2"),
            new Instruction("R2")
        );
        Actor position = new Actor();
        input.forEach(position::move);
        assertEquals(2, position.distanceFromOrigin());
    }

    @Test
    public void testPartOneDistanceThree() {
        List<Instruction> input = List.of(
            new Instruction("R5"),
            new Instruction("L5"),
            new Instruction("R5"),
            new Instruction("R3")
        );
        Actor position = new Actor();
        input.forEach(position::move);
        assertEquals(12, position.distanceFromOrigin());
    }

    @Test
    public void testPartTwo() {
        List<Instruction> input = List.of(
            new Instruction("R8"),
            new Instruction("R4"),
            new Instruction("R4"),
            new Instruction("R8")
        );
        assertEquals(4, solvePartTwo(input));
    }
}
