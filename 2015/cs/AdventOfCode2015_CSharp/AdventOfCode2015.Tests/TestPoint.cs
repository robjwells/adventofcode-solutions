using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests {
    class TestPoint {
        [TestCase(1, 2, 1, 2, 2, 4)]
        [TestCase(0, 0, 0, 0, 0, 0)]
        [TestCase(11, 11, 0, 0, 11, 11)]
        [TestCase(-1, -2, -1, -2, -2, -4)]
        [TestCase(1, -1, -1, 1, 0, 0)]
        [TestCase(-1, 1, 1, -1, 0, 0)]
        public void Point_Add(int x1, int y1, int x2, int y2, int ex, int ey) {
            Assert.AreEqual(
                new Point(x1, y1) + new Point(x2, y2),
                new Point(ex, ey)
            );
        }

        [TestCase(1, 2)]
        [TestCase(0, 0)]
        [TestCase(11, 11)]
        [TestCase(-1, -2)]
        [TestCase(1, -1)]
        [TestCase(-1, 1)]
        [TestCase(-2, -4)]
        public void Point_Equal_To_Self(int x, int y) {
            Point p = new Point(x, y);
            Assert.AreEqual(p, p);
        }

        [TestCase(1, 2)]
        [TestCase(0, 0)]
        [TestCase(11, 11)]
        [TestCase(-1, -2)]
        [TestCase(1, -1)]
        [TestCase(-1, 1)]
        [TestCase(-2, -4)]
        public void Point_Equal_To_Identical(int x, int y) {
            Point p = new Point(x, y);
            Point q = new Point(x, y);
            Assert.AreEqual(p, q);
        }

        [TestCase(1, 2)]
        [TestCase(-1, -2)]
        [TestCase(1, -1)]
        [TestCase(-1, 1)]
        [TestCase(-2, -4)]
        public void Point_Not_Equal_To_Reversed(int x, int y) {
            Point p = new Point(x, y);
            Point q = new Point(y, x);
            Assert.AreNotEqual(p, q);
        }

    }
}
