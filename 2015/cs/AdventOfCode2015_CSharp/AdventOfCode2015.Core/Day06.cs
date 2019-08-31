using System;
using System.Linq;
using System.Text.RegularExpressions;

namespace AdventOfCode2015.Core
{
    public class Day06
    {
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
}
