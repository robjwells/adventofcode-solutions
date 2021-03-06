package com.robjwells.adventofcode2015;

import java.io.IOException;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.function.BinaryOperator;
import java.util.logging.Logger;
import java.util.stream.Stream;
import java.util.stream.StreamSupport;

class IOFailedException extends RuntimeException {
    /**
     * Dummy serial version ID to make the linter happy.
     */
    private static final long serialVersionUID = 1L;

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

    static <T> Stream<T> accumulate(Iterator<T> input, BinaryOperator<T> reducer) {
        return iteratorToStream(new AccumulationIterator<>(input, reducer));
    }

    private static class AccumulationIterator<T> implements Iterator<T> {
        private final Iterator<T> source;
        private final BinaryOperator<T> reducer;
        private T total;

        AccumulationIterator(Iterator<T> source, BinaryOperator<T> reducer) {
            this.source = source;
            this.reducer = reducer;
        }

        @Override
        public boolean hasNext() {
            return source.hasNext();
        }

        @Override
        public T next() {
            total = total == null
                    ? source.next()
                    : reducer.apply(total, source.next());
            return total;
        }
    }

    static <T> Stream<T> iteratorToStream(Iterator<T> source) {
        Iterable<T> iterableWrapper = () -> source;
        return StreamSupport.stream(iterableWrapper.spliterator(), false);
    }

    static <T> Stream<Enumerated<T>> enumerate(Iterator<T> source) {
        return enumerate(source, 0);
    }

    static <T> Stream<Enumerated<T>> enumerate(Iterator<T> source, int start) {
        return iteratorToStream(new EnumerationIterator<>(source, start));
    }

    private static class EnumerationIterator<T> implements Iterator<Enumerated<T>> {
        private final Iterator<T> source;
        private int currentIndex;

        EnumerationIterator(Iterator<T> source, int startIndex) {
            this.source = source;
            this.currentIndex = startIndex;
        }

        @Override
        public boolean hasNext() {
            return source.hasNext();
        }

        @Override
        public Enumerated<T> next() {
            Enumerated<T> e = new Enumerated<>(currentIndex, source.next());
            currentIndex += 1;
            return e;
        }
    }

    static class Enumerated<T> {
        public final int index;
        public final T element;

        Enumerated(int index, T element) {
            this.index = index;
            this.element = element;
        }
    }
}
