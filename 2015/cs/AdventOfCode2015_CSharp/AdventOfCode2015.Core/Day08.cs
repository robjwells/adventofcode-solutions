using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace AdventOfCode2015.Core
{
    public class Day08 : Solution2015
    {
        public override int Day => 8;
        public override string Title => "Matchsticks";
        public override string Run(string input)
        {
            List<string> inputLines = ParseInput(input);
            return FormatReport(
                SolvePartOne(inputLines)
            );
        }

        public static int SolvePartOne(List<string> lines)
        {
            return (
                from line in lines
                select (original: line, unescaped: Unescape(line))
            ).Sum(results => results.original.Length - results.unescaped.Length);
        }

        public static List<string> ParseInput(string input) => input.Split('\n').ToList();

        public static string Unescape(string input)
            => Regex.Replace(
                input.Substring(1, input.Length - 2) // Remove surrounding double quotes
                     .Replace("\\\"", "\"")          // Unescape double quotes
                     .Replace("\\\\", "?"),          // Replace escaped backslashes with dummy character
                @"\\x[0-9a-f]{2}",                   // Replace hex-escapes with dummy character
                "?"
            );
    }
}
