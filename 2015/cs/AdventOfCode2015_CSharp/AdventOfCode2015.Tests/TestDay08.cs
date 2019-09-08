// using System.Linq;
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
    }
}
