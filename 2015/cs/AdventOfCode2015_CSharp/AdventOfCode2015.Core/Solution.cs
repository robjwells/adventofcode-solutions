namespace AdventOfCode2015.Core
{
    public abstract class Solution
    {
        public abstract int Year { get; }
        public abstract int Day { get; }
        public abstract string Run(string input);
    }
}
