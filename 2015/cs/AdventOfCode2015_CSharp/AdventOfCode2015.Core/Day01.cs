using System;
using System.Collections.Generic;
using System.Linq;

namespace AdventOfCode2015.Core
{
    public class Day01 : Solution2015
    {
        public override int Day => 1;
        public override string Title => "Not Quite Lisp";

        public override string Run(string input)
        {
            IEnumerable<int> parsed = parseInput(input);
            return FormatReport(SolvePartOne(parsed), SolvePartTwo(parsed));
        }

        public static IEnumerable<int> parseInput(string input)
            => input.Select(c => c == '(' ? 1 : -1);

        public int SolvePartOne(IEnumerable<int> input)
            => input.Sum();

        public int SolvePartTwo(IEnumerable<int> input)
        {
            return input.Accumulate((total, next) => total + next)
                .TakeWhile(floor => floor != -1)
                .Count() + 1;
        }
    }
}
