using System;
using System.Collections.Generic;
using System.Linq;

namespace AdventOfCode2015.Core
{
    public class Day03 : Solution2015
    {
        public override int Day => 3;
        public override string Title => "Perfectly Spherical Houses in a Vacuum";

        public override string Run(string input)
        {
            throw new NotImplementedException();
        }

        public static List<Point> ParseInput(string input)
        {
            return input.Select(c =>
            {
                switch (c)
                {
                    case '^':
                        return new Point(0, 1);
                    case 'v':
                        return new Point(0, -1);
                    case '<':
                        return new Point(-1, 0);
                    case '>':
                        return new Point(1, 0);
                    default:
                        throw new ArgumentException($"Invalid direction character: {c}");
                }
            }).ToList();
        }
    }
}
