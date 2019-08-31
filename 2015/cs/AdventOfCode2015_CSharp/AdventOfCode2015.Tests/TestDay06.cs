using NUnit.Framework;
using AdventOfCode2015.Core;

namespace Tests
{
    public class TestDay06
    {
        [TestCase("turn on 0,0 through 999,999", LightAction.TurnOn, 0, 0, 999, 999)]
        [TestCase("toggle 0,0 through 999,0", LightAction.Toggle, 0, 0, 999, 0)]
        [TestCase("turn off 499,499 through 500,500", LightAction.TurnOff, 499, 499, 500, 500)]
        public void Day06_TestParsing(
            string input, LightAction action, int startRow, int startCol, int endRow, int endCol
        )
        {
            LightInstruction result = LightInstruction.FromString(input);
            Assert.AreEqual(
                (action, startRow, startCol, endRow, endCol),
                (result.Action, result.StartRow, result.StartCol, result.EndRow, result.EndCol)
            );
        }
    }
}
