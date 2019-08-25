using System;

namespace AdventOfCode2015.Core
{
    public struct Point : IEquatable<Point>
    {
        public readonly int X;
        public readonly int Y;

        public Point(int x, int y)
        {
            this.X = x;
            this.Y = y;
        }

        public static Point Origin() {
            return new Point(0, 0);
        }

        public override string ToString() {
            return $"({X}, {Y})";
        }

        public static Point operator +(Point left, Point right)
        {
            return new Point(left.X + right.X, left.Y + right.Y);
        }

        public bool Equals(Point other)
        {
            return this.X == other.X && this.Y == other.Y;
        }

        public static bool operator ==(Point left, Point right)
        {
            return left.Equals(right);
        }

        public static bool operator !=(Point left, Point right)
        {
            return !(left == right);
        }

        // override object.Equals
        public override bool Equals(object obj)
        {
            //
            // See the full list of guidelines at
            //   http://go.microsoft.com/fwlink/?LinkID=85237
            // and also the guidance for operator== at
            //   http://go.microsoft.com/fwlink/?LinkId=85238
            //

            if (obj == null || GetType() != obj.GetType())
            {
                return false;
            }

            return this == (Point) obj;
        }

        // override object.GetHashCode
        public override int GetHashCode()
        {
            return (X, Y).GetHashCode();
        }
    }
}
