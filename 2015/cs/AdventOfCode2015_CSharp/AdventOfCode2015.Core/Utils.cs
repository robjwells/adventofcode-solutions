using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace AdventOfCode2015.Core
{
    public static class Utils
    {
        public static string LoadInput(int year, int day)
        {
            string inputDirectory = GetInputDirectory(year);
            string inputFileName = string.Format("{0}-{1:00}.txt", year, day);
            return File.ReadAllText(
                Path.Combine(inputDirectory, inputFileName)
            ).Trim();
        }

        // See: https://stackoverflow.com/a/25573832/1845155
        public static string GetInputDirectory(int year)
        {
            string baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
            List<string> pathParts = baseDirectory.Split(Path.DirectorySeparatorChar).ToList();

            int yearDirectoryIndex = pathParts.FindLastIndex(part => part == year.ToString());

            return Path.Combine(
                Path.GetPathRoot(baseDirectory),
                Path.Combine(pathParts.Take(yearDirectoryIndex + 1).ToArray()),
                "input"
            );
        }

        // Infinite IEnumerable that returns evenly spaced values, from start, by step.
        public static IEnumerable<int> Count(int start = 0, int step = 1)
        {
            int current = start;
            while (true)
            {
                yield return current;
                current += step;
            }
        }

        // Yield a stream of tuples (index, element) where each element is taken from the
        // sequence in order, and index is a counter starting from `from`.
        public static IEnumerable<(int Index, T Element)> EnumerateSequence<T>(
            this IEnumerable<T> sequence,
            int from = 0
        )
        =>  Enumerable.Zip(
                Count(start: from),
                sequence,
                ValueTuple.Create
            );
    }
}
