package com.robjwells.adventofcode2015;

interface Solution {
    int getYear();
    int getDay();
    String getTitle();

    private String titleLine() {
        String firstLine = String.format("Day %d: %s", getDay(), getTitle());
        return String.format("%s\n%s", firstLine, "=".repeat(firstLine.length()));
    }

    default String formatReport(Object partOneResult) {
        return String.format("%s\nPart one: %s", titleLine(), partOneResult);
    }

    default String formatReport(Object partOneResult, Object partTwoResult) {
        return String.format("%s\nPart two: %s", formatReport(partOneResult), partTwoResult);
    }

    String run(String input);
}
