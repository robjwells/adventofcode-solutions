using System;
using System.IO;

using CommandLine;

using AdventOfCode2015.Core;

namespace AdventOfCode2015
{
    class Program
    {
        static readonly int YEAR = 2015;

        public class Options
        {
            [Option('i', "input-dir", Required = true, HelpText = "Directory containing puzzle input files.")]
            public string InputDirectory { get; set; }

            [Value(0, MetaName = "day", HelpText = "Day for which to run solutions.")]
            public int? Day { get; set; }
        }

        static ISolution[] days = new ISolution[] {
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

        static string LoadInputForDay(int year, int day, string inputDirectoryPath)
        {
            string inputFileName = string.Format("{0}-{1:00}.txt", year, day);
            return File.ReadAllText(
                Path.Combine(inputDirectoryPath, inputFileName)
            );
        }

        static void RunSingleDay(int day, string inputDirectoryPath)
        {
            ISolution instance = days[day - 1];
            string result = instance.Run(
                LoadInputForDay(instance.Year, instance.Day, inputDirectoryPath)
            );
            Console.WriteLine(result);
        }

        static void RunAllDays(string inputDirectoryPath)
        {
            foreach (ISolution instance in days)
            {
                RunSingleDay(instance.Day, inputDirectoryPath);
            }
        }
    }
}
