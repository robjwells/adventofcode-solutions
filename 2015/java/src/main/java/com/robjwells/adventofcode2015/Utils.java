package com.robjwells.adventofcode2015;

import java.io.IOException;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.logging.Logger;

class IOFailedException extends RuntimeException {
    IOFailedException(String msg) {
        super(msg);
    }
}

class Utils {
    private final static Logger logger = Logger.getLogger(Utils.class.getName());

    private static Path getInputDirectory(int year) {
        FileSystem fs = FileSystems.getDefault();
        Path cwd = fs.getPath(System.getProperty("user.dir"));
        return getInputDirectory(year, cwd);
    }

    private static Path getInputDirectory(int year, Path currentDirectory) {
        while (!currentDirectory.endsWith(String.valueOf(year))) {
            currentDirectory = currentDirectory.getParent();
        }
        Path inputDirectory = currentDirectory.resolve("input");
        try {
            return inputDirectory.toRealPath();
        } catch (IOException exc) {
            logger.severe("Could not find input directory at expected location:");
            logger.severe(exc.toString());
            throw new IOFailedException(
                    String.format(
                            "Could not find `input` directory in `%s` directory above `%s`",
                            year, currentDirectory
                    )
            );
        }
    }

    static String loadPuzzleInput(int year, int day) {
        Path inputDir = getInputDirectory(year);
        String filename = String.format("%4d-%02d.txt", year, day);
        try {
            return Files.readString(inputDir.resolve(filename));
        } catch (IOException exc) {
            logger.severe(String.format("Could not read from file %s.", filename));
            throw new IOFailedException(String.format("Could not read from file %s", filename));
        }
    }
}
