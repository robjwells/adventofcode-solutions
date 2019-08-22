using System;
using System.Linq;

namespace AdventOfCode2015.Core
{
    public class Day01 : Solution2015
    {
        public override int Day => 1;
        public override string Title => "Not Quite Lisp";

        public override string Run(string input)
        {
            return FormatReport(SolvePartOne(input), SolvePartTwo(input));
        }

        public int SolvePartOne(string input)
        {
            return input.Select(c => c == '(' ? 1 : -1).Sum();
        }

        public int SolvePartTwo(string input)
        {
            int floor = 0;
            for (int index = 0; index < input.Length; index++)
            {
                floor += input[index] == '(' ? 1 : -1;
                if (floor == -1)
                {
                    return index + 1;   // Puzzle indexes instructions from 1
                }
            }
            throw new ArgumentException("Instructions do not place Santa in the basement.");
        }
    }
}
