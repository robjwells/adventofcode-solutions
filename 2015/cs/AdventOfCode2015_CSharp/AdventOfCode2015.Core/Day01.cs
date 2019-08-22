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
            throw new NotImplementedException();
        }

        public int SolvePartOne(string input)
        {
            return input.Select(c => c == '(' ? 1 : -1).Sum();
        }

        // public uint SolvePartTwo(string input) {
        //     throw new NotImplementedException();
        // }
    }
}
