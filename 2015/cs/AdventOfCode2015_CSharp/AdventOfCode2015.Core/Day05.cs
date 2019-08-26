using System;
using System.Collections.Generic;
using System.Linq;

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

        public override string Run(string input)
        {
            string[] parsed = input.Split('\n');
            return FormatReport(SolvePartOne(parsed));
        }

        public string[] ParseInput(string input)
        {
            return input.Split('\n');
        }

        public int SolvePartOne(string[] input)
        {
            return input.Where(IsNice).Count();
        }

        public static bool ContainsThreeVowels(string input)
        {
            return input.Where(vowels.Contains).Count() >= 3;
        }

        public static bool ContainsLetterTwiceInARow(string input)
        {
            if (input.Length == 0) { return false; }
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
    }
}
