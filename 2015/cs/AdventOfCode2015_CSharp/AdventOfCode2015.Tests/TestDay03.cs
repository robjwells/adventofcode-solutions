using System.Collections.Generic;
using System.Linq;

using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay03
    {
        Day03 instance;
        string input;
        List<Point> parsedInput;

        [SetUp]
        public void Setup()
        {
            instance = new Day03();
            input = Utils.LoadInput(instance.Year, instance.Day);
            parsedInput = Day03.ParseInput(input);
        }

        [Test]
        public void Day03_ParseInput_AllFourCases()
        {
            List<Point> expected = new (int, int)[] {
                (0, 1), (0, -1), (-1, 0), (1, 0)
            }.Select(
                p => new Point(p.Item1, p.Item2)
            ).ToList();
            Assert.AreEqual(
                expected,
                Day03.ParseInput("^v<>")
            );
        }

    }
}
