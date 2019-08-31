using NUnit.Framework;
using AdventOfCode2015.Core;
using static AdventOfCode2015.Core.Day06;

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

        [Test]
        public void Day06_TestGrid()
        {
            string input = string.Join('\n', new string[] {
            "turn on 0,0 through 999,999",
            "toggle 0,0 through 999,0",
            "turn off 499,499 through 500,500"
            });
            LightInstruction[] parsed = Day06.ParseInput(input);
            LightGrid g = new LightGrid();

            g.Perform(parsed[0]);
            Assert.AreEqual(1_000_000, g.TotalLightsOn);

            g.Perform(parsed[1]);
            Assert.AreEqual(1_000_000 - 1_000, g.TotalLightsOn);

            g.Perform(parsed[2]);
            Assert.AreEqual(1_000_000 - 1_000 - 4, g.TotalLightsOn);
        }

        [Test]
        public void Day06_PartOne_MatchesKnownCorrectResult()
        {
            LightInstruction[] input = Day06.ParseInput(Utils.LoadInput(2015, 6));
            Assert.AreEqual(
                543903,
                Day06.SolvePartOne(input)
            );
        }

        [Test]
        public void Day06_TestBrightnessGrid()
        {
            string input = string.Join('\n', new string[] {
            "turn on 0,0 through 999,999",
            "toggle 0,0 through 999,0",
            "turn off 499,499 through 500,500"
            });
            LightInstruction[] parsed = Day06.ParseInput(input);
            BrightnessGrid g = new BrightnessGrid();

            g.Perform(parsed[0]);
            Assert.AreEqual(1_000_000, g.TotalBrightness);

            g.Perform(parsed[1]);
            Assert.AreEqual(1_000_000 + 2_000, g.TotalBrightness);

            g.Perform(parsed[2]);
            Assert.AreEqual(1_000_000 + 2_000 - 4, g.TotalBrightness);
        }

        [Test]
        public void Day06_PartTwo_MatchesKnownCorrectResult()
        {
            LightInstruction[] input = Day06.ParseInput(Utils.LoadInput(2015, 6));
            Assert.AreEqual(
                14687245,
                Day06.SolvePartTwo(input)
            );
        }
    }
}
