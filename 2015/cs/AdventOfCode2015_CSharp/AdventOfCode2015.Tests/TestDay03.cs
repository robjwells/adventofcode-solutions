using System.Collections.Generic;

using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay03
    {
        Day03 instance;
        string input;
        List<(int, int)> parsedInput;

        [SetUp]
        public void Setup()
        {
            instance = new Day03();
            input = Utils.LoadInput(instance.Year, instance.Day);
            parsedInput = Day03.ParseInput(input);
        }

        [Test]
        public void Day03_ParseInput_AllFourCases() {
            Assert.AreEqual(
                new List<(int, int)>(new (int, int)[] {
                    (0, 1), (0, -1), (-1, 0), (1, 0)
                }),
                Day03.ParseInput("^v<>")
            );
        }

    }
}
