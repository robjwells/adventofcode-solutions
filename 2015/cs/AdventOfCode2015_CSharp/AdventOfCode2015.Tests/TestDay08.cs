using System.Collections.Generic;
using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay08
    {
        [TestCase("\"\"", 0)]
        [TestCase("\"abc\"", 3)]
        [TestCase("\"aaa\\\"aaa\"", 7)]
        [TestCase("\"\\x27\"", 1)]
        public void Unescape_WhenGivenKnownExample_GivesUnescapedCharacterCount(string input, int expected)
        {
            Assert.AreEqual(
                expected,
                Day08.Unescape(input).Length
            );
        }

        [Test]
        public void SolvePartOne_WhenGivenSampleInput_GivesSampleOutput()
        {
            string allInputWords = "\"\"\n\"abc\"\n\"aaa\\\"aaa\"\n\"\\x27\"";
            List<string> inputList = Day08.ParseInput(allInputWords);
            Assert.AreEqual(
                12,
                Day08.SolvePartOne(inputList)
            );
        }

        [Test]
        public void SolvePartOne_WhenGivenMyInput_GivesKnownCorrectResult()
        {
            List<string> inputList = Day08.ParseInput(Utils.LoadInput(2015, 8));
            Assert.AreEqual(
                1350,
                Day08.SolvePartOne(inputList)
            );
        }
    }
}
