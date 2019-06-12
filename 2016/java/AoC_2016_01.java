import static org.junit.Assert.*;

import java.util.Arrays;
import java.util.List;
import java.util.function.Consumer;
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
    }

    static int solvePartOne(List<Instruction> instructions) {
        Actor position = new Actor();
        instructions.forEach(position::move);
        return position.distanceFromOrigin();
    }

    private static class Actor {
        private int x = 0;
        private int y = 0;

        private int currentDirectionFunctionIndex = 0;

        final List<Consumer<Integer>> functions = List.of(
            (steps) -> y += steps,
            (steps) -> x += steps,
            (steps) -> y -= steps,
            (steps) -> x -= steps
        );

        void move(Instruction instruction) {
            int newIndex = Math.floorMod(
                (currentDirectionFunctionIndex + instruction.getDirection().getIndexDelta()),
                functions.size()
            );
            currentDirectionFunctionIndex = newIndex;
            functions.get(newIndex).accept(instruction.getBlocks());
        }

        int distanceFrom(int otherX, int otherY) {
            return Math.abs(x - otherX) + Math.abs(y - otherY);
        }

        int distanceFromOrigin() {
            return distanceFrom(0, 0);
        }

    }

    private static class Instruction {
        private final Turn turn;
        private final int blocks;

        Instruction(String instructionString) {
            this.turn = instructionString.charAt(0) == 'L' ? Turn.LEFT : Turn.RIGHT;
            this.blocks = Integer.parseInt(instructionString.substring(1));
        }

        public Turn getDirection() {
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
}
