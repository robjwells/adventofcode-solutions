namespace AdventOfCode2015.Core {
    using System.IO;

    public static class Utils {
        public static string LoadInput(string inputDirectory, int year, int day)
        {
            string inputFileName = string.Format("{0}-{1:00}.txt", year, day);
            return File.ReadAllText(
                Path.Combine(inputDirectory, inputFileName)
            );
        }
    }
}
