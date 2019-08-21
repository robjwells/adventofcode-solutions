using System;
using System.Collections.Generic;
using AdventOfCode2015.Core;

namespace AdventOfCode2015
{
    class Program
    {
        static ISolution[] days = new ISolution[] {
            new Day01()
        };

        static void Main(string[] args)
        {
            foreach (ISolution day in days)
            {
                Console.WriteLine("Day {0}, year {1}", day.Day, day.Year);
            }
        }
    }
}
