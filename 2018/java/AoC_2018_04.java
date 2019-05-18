import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map.Entry;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

class AoC_2018_04 extends Solution {
    static int DAY = 4;
    static String TITLE = "Advent of Code 2018 Day 4: Repose Record";

    public static void main(String[] args) {
        System.out.println(TITLE);

        // Tests
        Test_2018_04.testEventConstructorShiftStart();
        Test_2018_04.testEventConstructorSleepWake();
        Test_2018_04.testEventConstructorStoresDate();
        Test_2018_04.testMode();

        // Solution
        List<String> logLines = loadPuzzleInputLines(DAY)
            .sorted()
            .collect(Collectors.toList());
        HashMap<Integer, ArrayList<Integer>> sleepMap = makeSleepMap(logLines);

        int partOneResult = solvePartOne(sleepMap);
        assert partOneResult == 38813 : "Result does not match known result.";
        System.out.printf("Part one: %d\n", partOneResult);
    }

    static int solvePartOne(HashMap<Integer, ArrayList<Integer>> sleepTracker) {
        Entry<Integer, ArrayList<Integer>> e = sleepTracker.entrySet().stream()
            .max(Comparator.comparing(entry -> entry.getValue().size()))
            .get(); // Unwrap the optional
        int guardNumber = e.getKey();
        ArrayList<Integer> sleepList = e.getValue();
        Collections.sort(sleepList);
        int modalSleepMinute = getMode(sleepList);
        return guardNumber * modalSleepMinute;
    }

    static HashMap<Integer, ArrayList<Integer>> makeSleepMap(List<String> logLines) {
        ArrayList<Event> events = new ArrayList<Event>(logLines.size());
        int currentGuardNumber = -1;
        for (String line : logLines) {
            Event e;
            if (line.contains("#")) {
                e = new Event(line);
                currentGuardNumber = e.guardNumber;
            } else {
                e = new Event(line, currentGuardNumber);
            }
            events.add(e);
        }

        HashMap<Integer, ArrayList<Integer>> sleepTracker = new HashMap<>();
        for (int idx = 0; idx < events.size() - 1; idx++) {
            Event currentEvent = events.get(idx);
            if (currentEvent.type == EventType.START) {
                if (!sleepTracker.containsKey(currentEvent.guardNumber)) {
                    sleepTracker.put(currentEvent.guardNumber, new ArrayList<Integer>());
                }
                continue;
            }
            if (currentEvent.type == EventType.SLEEP) {
                Event wakeEvent = events.get(idx + 1);
                int sleepTime = currentEvent.datetime.getMinute();
                int wakeTime = wakeEvent.datetime.getMinute();
                ArrayList<Integer> sleepList = sleepTracker.get(currentEvent.guardNumber);
                IntStream.range(sleepTime, wakeTime).forEach(sleepList::add);
            }
        }

        return sleepTracker;
    }

    static <E> E getMode(List<E> list) {
        if (list.size() == 0) {
            return null;
        }
        E modalValue = list.get(0);
        int modalCount = 1;
        E currentValue = modalValue;
        int currentCount = 0;
        for (E value : list) {
            if (currentValue.equals(value)) {
                currentCount += 1;
            } else {
                if (currentCount > modalCount) {
                    modalCount = currentCount;
                    modalValue = currentValue;
                }
                currentValue = value;
                currentCount = 1;
            }
        }
        if (currentCount > modalCount) {
            return currentValue;
        } else {
            return modalValue;
        }
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

    static void testMode() {
        List<Integer> list = List.of(1, 2, 3, 3, 4, 5);
        Integer result = AoC_2018_04.getMode(list);
        assert result.equals(3) : result;
    }
}
