using NUnit.Framework;
using static AdventOfCode2015.Core.Utils;

namespace Tests
{
    public class TestUtils
    {
        [Test]
        public void EnumerateSequence_IncreasingIndexes()
        {
            int[] seq = new int[] {9, 8, 7};
            int predecessor = 42;
            foreach ((int index, int element) tuple in seq.EnumerateSequence(from: 43))
            {
                Assert.True(predecessor + 1 == tuple.index);
                predecessor = tuple.index;
            }
        }

        [Test]
        public void EnumerateSequence_ZeroBasedIndexesCanBeUsedToIndexIntoOriginalCollection() {
            int[] seq = new int[] {9, 8, 7};
            foreach ((int index, int element) tuple in seq.EnumerateSequence()) {
                Assert.AreEqual(
                    tuple.element,
                    seq[tuple.index]
                );
            }
        }
    }
}
