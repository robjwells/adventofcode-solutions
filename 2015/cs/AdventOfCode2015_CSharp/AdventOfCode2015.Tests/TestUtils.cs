using NUnit.Framework;
using System.Linq;
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
            foreach ((int index, int element) tuple in seq.Enumerate(from: 43))
            {
                Assert.True(predecessor + 1 == tuple.index);
                predecessor = tuple.index;
            }
        }

        [Test]
        public void EnumerateSequence_ZeroBasedIndexesCanBeUsedToIndexIntoOriginalCollection() {
            int[] seq = new int[] {9, 8, 7};
            foreach ((int index, int element) tuple in seq.Enumerate()) {
                Assert.AreEqual(
                    tuple.element,
                    seq[tuple.index]
                );
            }
        }

        [Test]
        public void Accumulate_IntegerAdditionWorks()
        {
            int[] source = {1, 2, 3};
            int[] expected = {1, 3, 6};
            int[] result = source.Accumulate((total, next) => total + next).ToArray();
            Assert.AreEqual(expected, result);
        }

        [Test]
        public void Accumulate_IntegerMultiplicationWorks()
        {
            int[] source = {1, 2, 3};
            int[] expected = {1, 2, 6};
            int[] result = source.Accumulate((total, next) => total * next).ToArray();
            Assert.AreEqual(expected, result);
        }

        [Test]
        public void Accumulate_StringConcatenationWorks()
        {
            string[] source = {"a", "b", "c"};
            string[] expected = {"a", "ab", "abc"};
            string[] result = source.Accumulate((total, next) => total + next).ToArray();
            Assert.AreEqual(expected, result);
        }
    }
}
