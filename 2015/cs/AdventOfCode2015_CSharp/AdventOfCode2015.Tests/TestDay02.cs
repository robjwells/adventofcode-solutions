using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay02
    {
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
    }
}
