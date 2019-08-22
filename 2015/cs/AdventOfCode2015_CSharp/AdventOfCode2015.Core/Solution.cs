namespace AdventOfCode2015.Core
{
    public abstract class Solution
    {
        public abstract int Year { get; }
        public abstract int Day { get; }
        public abstract string Title { get; }
        public abstract string Run(string input);

        protected string TitleLine
        {
            get
            {
                string titleLine = $"Day {Day}: {Title}";
                string underline = new string('=', titleLine.Length);
                return $"{titleLine}\n{underline}\n";
            }
        }
    }
}
