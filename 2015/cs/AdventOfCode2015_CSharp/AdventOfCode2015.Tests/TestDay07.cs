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
            var pairs = Enumerable.Zip(
                new ushort[] { 72, 507, 492, 114, 65412, 65079, 123, 456},
                new string[] { "d", "e", "f", "g", "h", "i", "x", "y"},
                (expected, wire) => (expected, actual: circuit[wire])
            );
            foreach (var pair in pairs)
            {
                Assert.AreEqual(pair.expected, pair.actual);
            }
        }
    }
}
