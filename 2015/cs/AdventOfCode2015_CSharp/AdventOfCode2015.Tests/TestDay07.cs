using System.Collections.Generic;
using System.Linq;
using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay07
    {
        [Test]
        public void WhenInputIsGivenExample_WiresHaveExpectedSignalOnceResolved()
        {
            string input = @"
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
";
            Circuit circuit = Day07.ParseInput(input);
            Enumerable.Zip(
                new ushort[] { 72, 507, 492, 114, 65412, 65079, 123, 456},
                new string[] { "d", "e", "f", "g", "h", "i", "x", "y"},
                (expected, wire) => (expected, actual: circuit[wire])
            )
            .ToList()
            .ForEach(
                pair => Assert.AreEqual(pair.expected, pair.actual)
            );
        }

        [Test]
        public void WhenGivenMyInput_ThenGivesKnownCorrectResults()
        {
            string input = Utils.LoadInput(2015, 7);
            Assert.AreEqual(
                (16076, 2797),
                Day07.SolveBothParts(input)
            );
        }
    }
}
