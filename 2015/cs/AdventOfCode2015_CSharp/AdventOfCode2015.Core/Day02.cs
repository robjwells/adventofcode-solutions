using System;
using System.Collections.Generic;
using System.Linq;

namespace AdventOfCode2015.Core
{
    public class Day02 : Solution2015
    {
        public override int Day => 2;
        public override string Title => "I Was Told There Would Be No Math";

        public override string Run(string input)
        {
            List<Present> parsed = ParseInput(input);
            return FormatReport(SolvePartOne(parsed), SolvePartTwo(parsed));
        }

        public static int SolvePartOne(List<Present> presents)
        {
            return presents.Select(p => p.TotalPaper).Sum();
        }

        public static int SolvePartTwo(List<Present> presents) {
            return presents.Select(p => p.TotalRibbon).Sum();
        }

        public static List<Present> ParseInput(string input)
        {
            return input.Split('\n').Select(Present.FromString).ToList();
        }

        public struct Present
        {
            public readonly int Length;
            public readonly int Width;
            public readonly int Height;
            private readonly int[] ordered;

            public Present(int length, int width, int height)
            {
                this.Length = length;
                this.Width = width;
                this.Height = height;

                int[] dimensions = new int[] { length, width, height };
                Array.Sort(dimensions);
                ordered = dimensions;
            }

            public static Present FromString(string dimensions)
            {
                int[] parsed = dimensions.Split('x').Select(int.Parse).ToArray();
                if (parsed.Length != 3)
                {
                    throw new ArgumentException("Dimensions string should be three elements long (l, w, h).");
                }
                return new Present(length: parsed[0], width: parsed[1], height: parsed[2]);
            }

            // Part one
            public int TotalPaper => SurfaceArea + Slack;
            private int SurfaceArea => 2 * Length * Width + 2 * Width * Height + 2 * Height * Length;
            private int Slack => ordered[0] * ordered[1];

            // Part two
            public int TotalRibbon => 2 * ordered[0] + 2 * ordered[1] + Bow;
            private int Bow => ordered.Aggregate((total, dim) => total * dim);
        }

    }

}
