namespace AdventOfCode2015.Core
{
    public interface ISolution
    {
        int Year { get; }
        int Day { get; }
        string Run(string input);
    }
}
