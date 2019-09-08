using System;
using System.IO;

using CommandLine;

using AdventOfCode2015.Core;

namespace AdventOfCode2015
{
    class Program
    {
        public class Options
        {
            [Value(0, MetaName = "day", HelpText = "Day for which to run solutions.")]
            public int? Day { get; set; }
        }

        static Solution[] days = new Solution[] {
            new Day01(),
            new Day02(),
            new Day03(),
            new Day04(),
            new Day05(),
            new Day06(),
            new Day07(),
            new Day08(),
            new Day09(),
        };

        static void Main(string[] args)
        {
            Parser.Default.ParseArguments<Options>(args)
                .WithParsed<Options>(RunWithOptions);
        }

        static void RunWithOptions(Options args)
        {
            if (args.Day.HasValue)
            {
                RunSingleDay(args.Day.Value);
            }
            else
            {
                RunAllDays();
            }
        }

        static void RunSingleDay(int day)
        {
            Solution instance = days[day - 1];
            string result = instance.Run(
                Utils.LoadInput(instance.Year, instance.Day)
            );
            Console.WriteLine(result);
        }

        static void RunAllDays()
        {
            foreach (Solution instance in days)
            {
                RunSingleDay(instance.Day);
                Console.WriteLine();
            }
        }
    }
}
