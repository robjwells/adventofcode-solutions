package com.robjwells.adventofcode2015;

interface Solution {
    int getYear();
    int getDay();
    String getTitle();

    private String titleLine() {
        return String.format("%s\n%s", getTitle(), "a".repeat(getTitle().length()));
    }

    private String formatReport(Object partOneResult) {
        return String.format("%s\nPart one: %s", titleLine(), partOneResult);
    }

    private String formatReport(Object partOneResult, Object partTwoResult) {
        return String.format("%s\nPart two: %s", formatReport(partOneResult), partTwoResult);
    }

    String run(String input);
}
