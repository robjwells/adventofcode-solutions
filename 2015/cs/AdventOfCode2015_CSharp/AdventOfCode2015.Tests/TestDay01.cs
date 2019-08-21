using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay01
    {
        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void UltimateAnswer_Is42()
        {
            Assert.AreEqual(Day01.UltimateAnswer(), 42);
        }
    }
}
