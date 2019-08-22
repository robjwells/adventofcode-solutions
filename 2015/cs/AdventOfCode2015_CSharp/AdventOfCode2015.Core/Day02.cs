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
            return FormatReport("");
        }

        public List<Present> ParseInput(string input)
        {
            return input.Split('\n').Select(Present.FromString).ToList();
        }

    }

    public class Present
    {
        public readonly int Length;
        public readonly int Width;
        public readonly int Height;

        public Present(int length, int width, int height)
        {
            this.Length = length;
            this.Width = width;
            this.Height = height;
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
    }
}
