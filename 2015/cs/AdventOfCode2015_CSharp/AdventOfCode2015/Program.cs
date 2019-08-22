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
            [Option('i', "input-dir", Required = true, HelpText = "Directory containing puzzle input files.")]
            public string InputDirectory { get; set; }

            [Value(0, MetaName = "day", HelpText = "Day for which to run solutions.")]
            public int? Day { get; set; }
        }

        static Solution[] days = new Solution[] {
            new Day01()
        };

        static void Main(string[] args)
        {
            Parser.Default.ParseArguments<Options>(args)
                .WithParsed<Options>(RunWithOptions);
        }

        static void RunWithOptions(Options args)
        {
            string inputDirectoryPath = Path.GetFullPath(args.InputDirectory);
            if (args.Day.HasValue)
            {
                RunSingleDay(args.Day.Value, inputDirectoryPath);
            }
            else
            {
                RunAllDays(inputDirectoryPath);
            }
        }

        static void RunSingleDay(int day, string inputDirectoryPath)
        {
            Solution instance = days[day - 1];
            string result = instance.Run(
                Utils.LoadInput(inputDirectoryPath, instance.Year, instance.Day)
            );
            Console.WriteLine(result);
        }

        static void RunAllDays(string inputDirectoryPath)
        {
            foreach (Solution instance in days)
            {
                RunSingleDay(instance.Day, inputDirectoryPath);
            }
        }
    }
}
