namespace AdventOfCode2015.Core
{
    using System;
    using System.Collections.Generic;
    using System.IO;
    using System.Linq;

    public static class Utils
    {
        public static string LoadInput(int year, int day)
        {
            string inputDirectory = GetInputDirectory(year);
            string inputFileName = string.Format("{0}-{1:00}.txt", year, day);
            return File.ReadAllText(
                Path.Combine(inputDirectory, inputFileName)
            );
        }

        // See: https://stackoverflow.com/a/25573832/1845155
        public static string GetInputDirectory(int year)
        {
            string baseDirectory = AppDomain.CurrentDomain.BaseDirectory;
            List<string> pathParts = baseDirectory.Split(Path.DirectorySeparatorChar).ToList();

            // Note that this’ll cause problems if you have the year repeated
            // as a directory in the path to the Advent of Code repo.
            int yearDirectoryIndex = pathParts.FindIndex(part => part == year.ToString());

            return Path.Combine(
                Path.GetPathRoot(baseDirectory),
                Path.Combine(pathParts.Take(yearDirectoryIndex + 1).ToArray()),
                "input"
            );
        }
    }
}
