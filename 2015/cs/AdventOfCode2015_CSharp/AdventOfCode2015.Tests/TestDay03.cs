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

        [TestCase(">", 2)]
        [TestCase("^>v<", 4)]
        [TestCase("^v^v^v^v^v", 2)]
        public void Day03_PartOne_CorrectResultsForGivenDirections(string directions, int uniqueVisited) {
            Assert.AreEqual(
                uniqueVisited,
                instance.SolvePartOne(Day03.ParseInput(directions))
            );
        }

        [Test]
        public void Day03_PartOne_MatchesKnownCorrectAnswer() {
            Assert.AreEqual(
                2081,
                instance.SolvePartOne(parsedInput)
            );
        }

        [TestCase("^v", 3)]
        [TestCase("^>v<", 3)]
        [TestCase("^v^v^v^v^v", 11)]
        public void Day03_PartTwo_CorrectResultsForGivenDirections(string directions, int uniqueVisited) {
            Assert.AreEqual(
                uniqueVisited,
                instance.SolvePartTwo(Day03.ParseInput(directions))
            );
        }

        [TestCase("^vv^^vv^", 3)]
        [TestCase("<<>>", 2)]
        [TestCase("", 1)]
        [TestCase("<>><><", 3)]
        public void Day03_PartTwo_LocationsNotDoubleCounted(string directions, int uniqueVisited) {
            Assert.AreEqual(
                uniqueVisited,
                instance.SolvePartTwo(Day03.ParseInput(directions))
            );
        }

        [Test]
        public void Day03_PartTwo_MatchesKnownCorrectAnswer() {
            Assert.AreEqual(
                2341,
                instance.SolvePartTwo(parsedInput)
            );
        }

    }
}
