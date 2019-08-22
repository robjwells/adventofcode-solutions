using System.Collections.Generic;

using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay02
    {
        List<Day02.Present> parsedInput;

        [SetUp]
        public void Setup()
        {
            parsedInput = Day02.ParseInput(Utils.LoadInput(2015, 2));
        }

        [TestCase("1x2x3", 1, 2, 3)]
        [TestCase("0x0x0", 0, 0, 0)]
        [TestCase("10x20x30", 10, 20, 30)]
        public void Day02_Present_CanConstructFromString(string input, int length, int width, int height)
        {
            Day02.Present p = Day02.Present.FromString(input);
            Assert.AreEqual(
                expected: (length, width, height),
                actual: (p.Length, p.Width, p.Height)
            );
        }

        [TestCase("2x3x4", 58)]
        [TestCase("1x1x10", 43)]
        public void Day02_Present_TotalPaperMatchesGivenExamples(string input, int expected)
        {
            Assert.AreEqual(
                expected,
                Day02.Present.FromString(input).TotalPaper
            );
        }

        [Test]
        public void Day02_PartOne_MatchesKnownCorrectAnswer()
        {
            Assert.AreEqual(
                1588178,
                Day02.SolvePartOne(parsedInput)
            );
        }
    }
}
