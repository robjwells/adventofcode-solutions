import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

class AoC_2018_04 extends Solution {
    static int DAY = 4;
    static String TITLE = "Advent of Code 2018 Day 4: Repose Record";

    public static void main(String[] args) {
        // Tests
        Test_2018_04.testEventConstructorShiftStart();
        Test_2018_04.testEventConstructorSleepWake();
        Test_2018_04.testEventConstructorStoresDate();
    }

}

enum EventType {
    START,
    SLEEP,
    WAKE
}

class Event {
    LocalDateTime datetime;
    int guardNumber;
    EventType type;

    private static DateTimeFormatter dateParser = (
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")
    );

    private static String datePatternPart = (
        "^\\[(\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2})\\] "
    );
    private static String guardStartPatternPart = (
        "Guard #(\\d+) begins shift"
    );
    private static String sleepWakePatternPart = (
        "(wakes up|falls asleep)"
    );
    private static Pattern guardStartPattern = Pattern.compile(
        datePatternPart + guardStartPatternPart + "$"
    );
    private static Pattern guardSleepWakePattern = Pattern.compile(
        datePatternPart + sleepWakePatternPart + "$"
    );

    Event(String logLine) {
        Matcher logMatcher = guardStartPattern.matcher(logLine);
        if (!logMatcher.matches()) {
            throw new IllegalArgumentException("Invalid log line.");
        }
        this.datetime = parseDate(logMatcher.group(1));
        this.guardNumber = Integer.parseInt(logMatcher.group(2));
        this.type = EventType.START;
    }

    Event(String logLine, int guardNumber) {
        this.guardNumber = guardNumber;
        Matcher logMatcher = guardSleepWakePattern.matcher(logLine);
        if (!logMatcher.matches()) {
            throw new IllegalArgumentException("Invalid log line.");
        }
        this.datetime = parseDate(logMatcher.group(1));
        if (logMatcher.group(2).equals("falls asleep")) {
            this.type = EventType.SLEEP;
        } else {
            this.type = EventType.WAKE;
        }
    }

    private static LocalDateTime parseDate(String dateString) {
        try {
            return dateParser.parse(dateString, LocalDateTime::from);
        } catch (DateTimeParseException exc) {
            throw new IllegalArgumentException("Invalid date format", exc);
        }
    }

    @Override
    public String toString() {
        return String.format("Event(%s, Guard #%d, %s)", datetime, guardNumber, type);
    }
}

class Test_2018_04 {
    static List<String> shiftStartLines = Arrays.asList(
        "[1518-11-01 00:00] Guard #10 begins shift",
        "[1518-11-01 23:58] Guard #99 begins shift",
        "[1518-11-03 00:05] Guard #10 begins shift",
        "[1518-11-04 00:02] Guard #99 begins shift",
        "[1518-11-05 00:03] Guard #99 begins shift"
    );

    static List<String> sleepWakeLines = Arrays.asList(
        "[1518-11-01 00:05] falls asleep",
        "[1518-11-01 00:25] wakes up",
        "[1518-11-01 00:30] falls asleep",
        "[1518-11-01 00:55] wakes up",
        "[1518-11-02 00:40] falls asleep",
        "[1518-11-02 00:50] wakes up",
        "[1518-11-03 00:24] falls asleep",
        "[1518-11-03 00:29] wakes up",
        "[1518-11-04 00:36] falls asleep",
        "[1518-11-04 00:46] wakes up",
        "[1518-11-05 00:45] falls asleep",
        "[1518-11-05 00:55] wakes up"
    );

    /**
     * Event can parse shift-start lines from the log input.
     */
    static void testEventConstructorShiftStart() {
        List<Event> events = shiftStartLines.stream()
            .map(logLine -> new Event(logLine))
            .collect(Collectors.toList());
        assert events.size() == shiftStartLines.size();
        assert events.stream()
            .allMatch(event -> event.guardNumber == 10 || event.guardNumber == 99);
        assert events.stream().allMatch(event -> event.type.equals(EventType.START));
    }

    /**
     * Event can parse sleep/wake lines from the log input.
     */
    static void testEventConstructorSleepWake() {
        List<Event> events = sleepWakeLines.stream()
            .map(logLine -> new Event(logLine, 1))
            .collect(Collectors.toList());
        assert events.size() == sleepWakeLines.size();
        assert events.stream().allMatch(event -> event.guardNumber == 1);
        assert events.stream()
            .allMatch(event -> event.type == EventType.WAKE || event.type == EventType.SLEEP);
    }

    /**
     * Event stores the date as a string.
     */
    static void testEventConstructorStoresDate() {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");
        for (String logLine : shiftStartLines) {
            Event e = new Event(logLine);
            assert e.datetime.format(formatter).equals(logLine.substring(1, 17));
        }
        for (String logLine : sleepWakeLines) {
            Event e = new Event(logLine, 1);
            assert e.datetime.format(formatter).equals(logLine.substring(1, 17));
        }
    }
}
