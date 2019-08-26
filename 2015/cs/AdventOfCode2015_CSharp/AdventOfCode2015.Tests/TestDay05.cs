using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay05
    {
        [TestCase("aei", true)]
        [TestCase("xazegov", true)]
        [TestCase("aeiouaeiouaeiou", true)]
        [TestCase("", false)]
        [TestCase("aab", false)]
        [TestCase("bab", false)]
        public void Day05_ContainsThreeVowels_MatchesGivenExamples(string input, bool expected)
        {
            Assert.AreEqual(
                expected,
                Day05.ContainsThreeVowels(input)
            );
        }

        [TestCase("", false)]
        [TestCase("a", false)]
        [TestCase("aab", true)]
        [TestCase("bab", false)]
        [TestCase("aabbccddee", true)]
        [TestCase("xx", true)]
        [TestCase("abcdde", true)]
        public void Day05_ContainsLetterTwiceInARow_MatchesGivenExamples(string input, bool expected)
        {
            Assert.AreEqual(
                expected,
                Day05.ContainsLetterTwiceInARow(input)
            );
        }

        [TestCase("", true)]
        [TestCase("a", true)]
        [TestCase("aab", false)]
        [TestCase("bab", false)]
        [TestCase("aabbccddee", false)]
        [TestCase("xx", true)]
        [TestCase("abcdde", false)]
        [TestCase("axyb", false)]
        [TestCase("xayb", true)]
        [TestCase("apqb", false)]
        [TestCase("pq", false)]
        [TestCase("paqb", true)]
        public void Day05_DoesNotContainForbiddenSubstrings_MatchesGivenExamples(string input, bool expected)
        {
            Assert.AreEqual(
                expected,
                Day05.DoesNotContainForbiddenStrings(input)
            );
        }

        [TestCase("ugknbfddgicrmopn", true)]
        [TestCase("aaa", true)]
        [TestCase("jchzalrnumimnmhp", false)]
        [TestCase("haegwjzuvuyypxyu", false)]
        [TestCase("dvszwmarrgswjxmb", false)]
        public void Day05_IsNice_MatchesGivenExamples(string input, bool expected)
        {
            Assert.AreEqual(
                expected,
                Day05.IsNice(input)
            );
        }

        [Test]
        public void Day05_PartOne_MatchesKnownCorrectResult()
        {
            Day05 instance = new Day05();
            string[] input = instance.ParseInput(Utils.LoadInput(instance.Year, instance.Day));
            Assert.AreEqual(
                236,
                instance.SolvePartOne(input)
            );
        }
    }
}
