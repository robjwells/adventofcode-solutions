using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace AdventOfCode2015.Core
{
    public class Day05 : Solution2015
    {
        public override int Day => 5;
        public override string Title => "Doesn't He Have Intern-Elves For This?";

        private static readonly HashSet<char> vowels = new HashSet<char>(new char[] {
            'a', 'e', 'i', 'o', 'u'
        });
        private static readonly HashSet<string> forbiddenStrings = new HashSet<string>(new string[] {
            "ab", "cd", "pq", "xy"
        });
        private static readonly Regex letterPairAppearsTwiceRegex = new Regex(@"(..).*\1");
        private static readonly Regex letterRepeatsAfterOneCharRegex = new Regex(@"(.).\1");

        public override string Run(string input)
        {
            string[] parsed = ParseInput(input);
            return FormatReport(
                SolvePartOne(parsed),
                SolvePartTwo(parsed)
            );
        }

        public string[] ParseInput(string input)
        {
            return input.Split('\n');
        }

        public int SolvePartOne(string[] input)
        {
            return input.Where(IsNice).Count();
        }

        public int SolvePartTwo(string[] input)
        {
            return input.Where(IsNewNice).Count();
        }

        public static bool ContainsThreeVowels(string input)
        {
            return input.Where(vowels.Contains).Count() >= 3;
        }

        public static bool ContainsLetterTwiceInARow(string input)
        {
            if (input.Length < 2) { return false; }
            return input
                .Zip(input.Substring(1), ValueTuple.Create)
                .Where(tuple => tuple.Item1 == tuple.Item2)
                .Count() > 0;
        }

        public static bool DoesNotContainForbiddenStrings(string input)
        {
            return forbiddenStrings
                .Where(input.Contains)
                .Count() == 0;
        }

        public static bool IsNice(string input)
        {
            return (
                ContainsThreeVowels(input) &&
                ContainsLetterTwiceInARow(input) &&
                DoesNotContainForbiddenStrings(input)
            );
        }

        public static bool LetterPairAppearsTwice(string input)
        {
            return letterPairAppearsTwiceRegex.IsMatch(input);
        }

        public static bool LetterRepeatsAfterOneChar(string input)
        {
            return letterRepeatsAfterOneCharRegex.IsMatch(input);
        }

        public static bool IsNewNice(string input)
        {
            return LetterPairAppearsTwice(input) && LetterRepeatsAfterOneChar(input);
        }
    }
}
