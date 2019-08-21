using System;
using System.Linq;

namespace AdventOfCode2015.Core
{
    public class Day01 : ISolution
    {
        public int Year => 2015;
        public int Day => 1;

        public string Run(string input)
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
