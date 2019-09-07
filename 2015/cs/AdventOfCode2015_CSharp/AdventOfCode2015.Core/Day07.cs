using System;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AdventOfCode2015.Core
{
    public class Day07 : Solution2015
    {
        public override int Day => 7;
        public override string Title => "Some Assembly Required";
        public override string Run(string input)
        {
            return FormatReport("");
        }

        public static List<Wire> ParseInput(string input)
        {
            return input.Trim().Split('\n').Select(Wire.FromString).ToList();
        }

    }

    public class Circuit
    {
        private Dictionary<string, Wire> wireMap = new Dictionary<string, Wire>();

        public ushort this[string wireName] => wireMap[wireName].Resolve(this);

        public static Circuit FromInstructions(List<Wire> instructions)
        {
            Circuit circuit = new Circuit();
            instructions.ForEach(wire => circuit.wireMap.Add(wire.Name, wire));
            return circuit;
        }
    }

    public abstract class Wire
    {
        public string Name { get; set; }
        public virtual ushort Resolve(Circuit circuit) => throw new NotImplementedException();

        private static Regex immediateRegex = new Regex(
            @"^(\d+) -> ([a-z]+)$"
        );
        private static Regex wireReferenceRegex = new Regex(
            @"^([a-z]+) -> ([a-z]+)$"
        );
        private static Regex notRegex = new Regex(
            @"^NOT ([a-z]+) -> ([a-z]+)$"
        );
        private static Regex mixedAndRegex = new Regex(
            @"^(\d+) AND ([a-z]+) -> ([a-z]+)$"
        );
        private static Regex wireAndOrRegex = new Regex(
            @"^([a-z]+) (?:AND|OR) ([a-z]+) -> ([a-z]+)$"
        );
        private static Regex shiftRegex = new Regex(
            @"^([a-z]+) (?:[LR]SHIFT) (\d+) -> ([a-z]+)$"
        );

        public static Wire FromString(string input)
        {
            if (immediateRegex.IsMatch(input))
            {
                return ImmediateWire.FromMatch(immediateRegex.Match(input));
            }
            if (wireReferenceRegex.IsMatch(input))
            {
                return ReferenceWire.FromMatch(wireReferenceRegex.Match(input));
            }
            if (notRegex.IsMatch(input))
            {
                return NotWire.FromMatch(notRegex.Match(input));
            }
            if (mixedAndRegex.IsMatch(input))
            {
                return MixedAndWire.FromMatch(mixedAndRegex.Match(input));
            }
            if (wireAndOrRegex.IsMatch(input))
            {
                Match match = wireAndOrRegex.Match(input);
                if (input.Contains("AND"))
                {
                    return ReferenceAndWire.FromMatch(match);
                }
                else
                {
                    return ReferenceOrWire.FromMatch(match);
                }
            }
            if (shiftRegex.IsMatch(input))
            {
                Match match = shiftRegex.Match(input);
                if (input.Contains("LSHIFT"))
                {
                    return LeftShiftWire.FromMatch(match);
                }
                else
                {
                    return RightShiftWire.FromMatch(match);
                }
            }
            throw new ArgumentException($"Invalid input for wire types available. `{input}`");
        }

    }

    public class ImmediateWire : Wire
    {
        public ushort value;
        public override ushort Resolve(Circuit circuit) => value;

        public static ImmediateWire FromMatch(Match match)
        {
            return new ImmediateWire()
            {
                Name = match.Groups[2].Value,
                value = ushort.Parse(match.Groups[1].Value)
            };
        }
    }

    public class ReferenceWire : Wire
    {
        public string wire;
        public override ushort Resolve(Circuit circuit) => circuit[wire];

        public static ReferenceWire FromMatch(Match match)
        {
            return new ReferenceWire()
            {
                Name = match.Groups[2].Value,
                wire = match.Groups[1].Value
            };
        }
    }

    public class NotWire : ReferenceWire
    {
        public override ushort Resolve(Circuit circuit) => (ushort)~base.Resolve(circuit);
    }

    public class ReferenceBinaryWire : Wire
    {
        public string left;
        public string right;

        public static ReferenceBinaryWire FromMatch(Match match)
        {
            return new ReferenceBinaryWire()
            {
                Name = match.Groups[3].Value,
                left = match.Groups[1].Value,
                right = match.Groups[2].Value
            };
        }
    }

    public class MixedWire : ReferenceWire
    {
        public ushort number;

        public new static MixedWire FromMatch(Match match)
        {
            ushort number;
            string wireReference;
            try
            {
                number = ushort.Parse(match.Groups[1].Value);
                wireReference = match.Groups[2].Value;
            }
            catch (FormatException)
            {
                number = ushort.Parse(match.Groups[2].Value);
                wireReference = match.Groups[1].Value;
            }
            return new MixedWire()
            {
                Name = match.Groups[3].Value,
                number = number,
                wire = wireReference
            };
        }
    }

    public class MixedAndWire : MixedWire
    {
        public override ushort Resolve(Circuit circuit) => (ushort)(number & circuit[wire]);
    }

    public class ReferenceAndWire : ReferenceBinaryWire
    {
        public override ushort Resolve(Circuit circuit) => (ushort)(circuit[left] & circuit[right]);
    }

    public class ReferenceOrWire : ReferenceBinaryWire
    {
        public override ushort Resolve(Circuit circuit) => (ushort)(circuit[left] | circuit[right]);
    }

    public class LeftShiftWire : MixedWire
    {
        public override ushort Resolve(Circuit circuit) => (ushort)(circuit[wire] << number);
    }

    public class RightShiftWire : MixedWire
    {
        public override ushort Resolve(Circuit circuit) => (ushort)(circuit[wire] >> number);
    }
}
