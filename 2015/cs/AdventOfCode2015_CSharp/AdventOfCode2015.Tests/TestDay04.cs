using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay04
    {
        [TestCase("abcdef", "e80b5017098950fc58aad83c8c14978e")]
        [TestCase("abcdef609043", "000001dbbfa3a5c83a2d506429c7b00e")]
        [TestCase("pqrstuv1048970", "000006136ef2ff3b291c85725f17325c")]
        public void Day04_HashDigest_GivesExpectedResultsForKnownCases(string message, string expectedDigest) {
            Assert.AreEqual(
                expectedDigest.ToLower(),
                Day04.HashDigest(message).ToLower()
            );
        }
    }
}
