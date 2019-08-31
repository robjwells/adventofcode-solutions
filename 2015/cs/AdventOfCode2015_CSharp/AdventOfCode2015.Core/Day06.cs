using System;
using System.Linq;
using System.Text.RegularExpressions;

namespace AdventOfCode2015.Core
{
    public class Day06 : Solution2015
    {
        public override int Day => 6;
        public override string Title => "Probably a Fire Hazard";

        public override string Run(string input)
        {
            LightInstruction[] parsed = ParseInput(input);
            return FormatReport(
                SolvePartOne(parsed)
            );
        }

        public static LightInstruction[] ParseInput(string input)
        {
            return input
                .Split('\n')
                .Select(LightInstruction.FromString)
                .ToArray();
        }

        public static int SolvePartOne(LightInstruction[] instructions)
        {
            LightGrid grid = new LightGrid();
            foreach(LightInstruction instruction in instructions)
            {
                grid.Perform(instruction);
            }
            return grid.TotalLightsOn;
        }
    }

    public enum LightAction
    {
        TurnOn,
        TurnOff,
        Toggle
    }

    public struct LightInstruction
    {
        public LightAction Action { get; }
        public int StartRow { get; }
        public int StartCol { get; }
        public int EndRow { get; }
        public int EndCol { get; }

        public LightInstruction(LightAction action, int startRow, int startCol, int endRow, int endCol)
        {
            Action = action;
            StartRow = startRow;
            StartCol = startCol;
            EndRow = endRow;
            EndCol = endCol;
        }

        public static LightInstruction FromString(string inputLine)
        {
            Regex instructionRegex = new Regex(@"
                (?<action> turn\ on | turn\ off | toggle )
                \s
                (?<startRow> \d{1,3} ) , (?<startCol> \d{1,3} )
                \s
                through
                \s
                (?<endRow> \d{1,3} ) , (?<endCol> \d{1,3} )
                ",
                RegexOptions.IgnorePatternWhitespace
            );
            Match result = instructionRegex.Match(inputLine);
            if (!result.Success)
            {
                throw new ArgumentException($"input line did not match expected pattern: {inputLine}");
            }

            LightAction action;
            switch (result.Groups["action"].Value)
            {
                case "toggle":
                    action = LightAction.Toggle;
                    break;
                case "turn on":
                    action = LightAction.TurnOn;
                    break;
                case "turn off":
                    action = LightAction.TurnOff;
                    break;
                default:
                    throw new ArgumentException("Unreachable.");
            }

            return new LightInstruction(
                action,
                int.Parse(result.Groups["startRow"].Value),
                int.Parse(result.Groups["startCol"].Value),
                int.Parse(result.Groups["endRow"].Value),
                int.Parse(result.Groups["endCol"].Value)
            );
        }
    }

    public class LightGrid
    {
        private int[,] lights = new int[1000, 1000];
        public int TotalLightsOn
        {
            get
            {
                // Use query syntax here to convert the int[,]
                // into a flattened IEnumerable<int>
                return (from int light in lights
                        where light == 1
                        select light).Count();
            }
        }

        private delegate int LightFunction(int row, int col);

        private LightFunction TurnOn = (int row, int col) => 1;
        private LightFunction TurnOff = (int row, int col) => 0;
        private int Toggle(int row, int col)
        {
            return 1 - lights[row, col];
        }

        public void Perform(LightInstruction instruction)
        {
            switch (instruction.Action)
            {
                case LightAction.TurnOn:
                    Perform(TurnOn, instruction);
                    break;
                case LightAction.TurnOff:
                    Perform(TurnOff, instruction);
                    break;
                case LightAction.Toggle:
                    Perform(Toggle, instruction);
                    break;
            }
        }

        private void Perform(LightFunction function, LightInstruction instruction)
        {
            for (int row = instruction.StartRow; row <= instruction.EndRow; row += 1)
            {
                for (int col = instruction.StartCol; col <= instruction.EndCol; col += 1)
                {
                    lights[row, col] = function(row, col);
                }
            }
        }
    }
}