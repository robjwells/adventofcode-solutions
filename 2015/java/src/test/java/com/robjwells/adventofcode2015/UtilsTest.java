package com.robjwells.adventofcode2015;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static org.junit.jupiter.api.Assertions.*;

class UtilsTest {

    @Test
    void test_accumulate() {
        int[] source = {1, 2, 3};
        int[] expected = {1, 3, 6};
        int[] result = Utils.accumulate(Arrays.stream(source).iterator(), (t, n) -> t + n)
                .mapToInt(x -> x)
                .toArray();
        assertArrayEquals(expected, result);
    }

    @Test
    void test_iteratorToStream_roundTrip() {
        int[] source = {1, 2, 3};
        int[] result = Utils.iteratorToStream(Arrays.stream(source).iterator())
                .mapToInt(x -> x)
                .toArray();
        assertArrayEquals(source, result);
    }

    @Test
    void test_enumerate_startGivenExplicitly() {
        int[] source = {0, 1, 2};
        Utils.enumerate(Arrays.stream(source).iterator(), 42)
                .forEach(e -> assertEquals(42 + e.element, e.index));
    }

    @Test
    void test_enumerate_startImplicit() {
        int[] source = {0, 1, 2};
        Utils.enumerate(Arrays.stream(source).iterator())
                .forEach(e -> assertEquals(source[e.index], e.index));
    }
}
