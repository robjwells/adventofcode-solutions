using System.IO;

namespace AdventOfCode
{

    abstract class Solution
    {
        protected abstract int YEAR { get; }
        protected abstract int DAY { get; }

        protected string ReadInputLines()
        {
            return Path.Combine(
                Directory.GetParent(Directory.GetCurrentDirectory()).ToString(),
                "input",
                YEAR.ToString(),
                DAY.ToString()
            );
        }
    }

    abstract class Solution2015 : Solution
    {
        protected override int YEAR { get { return 2015; } }
    }

    class Solution201501 : Solution2015 {
        protected override int DAY { get { return 1; } }
        static void Main(string[] args) {
            Solution201501 day = new Solution201501();
            System.Console.WriteLine(
                day.ReadInputLines().ToString()
            );
        }
    }

}