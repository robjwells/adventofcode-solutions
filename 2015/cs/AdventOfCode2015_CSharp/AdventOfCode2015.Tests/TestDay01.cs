using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay01
    {
        Day01 instance = new Day01();

        [SetUp]
        public void Setup()
        {
        }

        [Test]
        public void Day01_Day_Is1() {
            Assert.AreEqual(instance.Day, 1);
        }

        [Test]
        public void Day01_Year_Is2015() {
            Assert.AreEqual(instance.Year, 2015);
        }
    }
}
