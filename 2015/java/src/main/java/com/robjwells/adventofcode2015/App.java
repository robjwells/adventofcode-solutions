/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package com.robjwells.adventofcode2015;

import java.util.List;

public class App {
    private final static List<Solution> days = List.of(
            new Day01(),
            new Day02()
    );

    private static void runOne(Solution day) {
        String input = Utils.loadPuzzleInput(day.getYear(), day.getDay());
        System.out.println(day.run(input));
    }

    private static void runAll() {
        days.forEach(App::runOne);
    }

    public static void main(String[] args) {
        if (args.length == 0) {
            runAll();
        } else if (args.length == 1) {
            int day = Integer.parseInt(args[0]) - 1;
            runOne(days.get(day));
        }
    }
}
