import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Stream;

abstract class Solution {
    static Stream<String> loadPuzzleInputLines(int day) {
        try {
            Path inputFilePath = Path.of(String.format("../input/2018-%02d.txt", day));
            return Files.lines(inputFilePath);
        } catch (IOException exc) {
            exc.printStackTrace();
            System.exit(1);
        }
        return "".lines(); // Failure case to make the compiler happy.
    }
}
