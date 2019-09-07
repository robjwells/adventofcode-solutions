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
            Circuit circuit = ParseInput(input);
            ushort partOneResult = circuit["a"];
            circuit.Reset();
            circuit.Add($"{partOneResult} -> b");
            ushort partTwoResult = circuit["a"];

            return FormatReport(
                partOneResult,
                partTwoResult
            );
        }

        public static Circuit ParseInput(string input)
        {
            Circuit circuit = new Circuit();
            input.Trim().Split('\n').ToList().ForEach(circuit.Add);
            return circuit;
        }
    }

    public class Circuit
    {
        private Dictionary<string, Wire> wireMap = new Dictionary<string, Wire>();

        public ushort this[string wireName] => wireMap[wireName].Resolve(this);

        public void Reset()
        {
            wireMap.Values.ToList().ForEach(wire => wire.Reset());
        }

        public void Add(string wireInstruction)
        {
            Wire wire = Wire.FromString(wireInstruction);
            wireMap[wire.Name] = wire;
        }
    }

    public abstract class Wire
    {
        public string Name { get; set; }
        private ushort? value;
        public ushort Resolve(Circuit circuit)
        {
            if (!value.HasValue)
            {
                value = ResolveHelper(circuit);
            }
            return value.Value;
        }

        public virtual ushort ResolveHelper(Circuit circuit) => throw new NotImplementedException();

        public void Reset()
        {
            value = null;
        }

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
                return new ImmediateWire(immediateRegex.Match(input));
            }
            if (wireReferenceRegex.IsMatch(input))
            {
                return new ReferenceWire(wireReferenceRegex.Match(input));
            }
            if (notRegex.IsMatch(input))
            {
                return new NotWire(notRegex.Match(input));
            }
            if (mixedAndRegex.IsMatch(input))
            {
                return new MixedAndWire(mixedAndRegex.Match(input));
            }
            if (wireAndOrRegex.IsMatch(input))
            {
                Match match = wireAndOrRegex.Match(input);
                if (input.Contains("AND"))
                {
                    return new ReferenceAndWire(match);
                }
                else
                {
                    return new ReferenceOrWire(match);
                }
            }
            if (shiftRegex.IsMatch(input))
            {
                Match match = shiftRegex.Match(input);
                if (input.Contains("LSHIFT"))
                {
                    return new LeftShiftWire(match);
                }
                else
                {
                    return new RightShiftWire(match);
                }
            }
            throw new ArgumentException($"Invalid input for wire types available. `{input}`");
        }

    }

    public class ImmediateWire : Wire
    {
        public ushort value;
        public override ushort ResolveHelper(Circuit circuit) => value;

        public ImmediateWire(Match match)
        {
            Name = match.Groups[2].Value;
            value = ushort.Parse(match.Groups[1].Value);
        }
    }

    public class ReferenceWire : Wire
    {
        public string wire;
        public override ushort ResolveHelper(Circuit circuit) => circuit[wire];

        public ReferenceWire() { }
        public ReferenceWire(Match match)
        {
            Name = match.Groups[2].Value;
            wire = match.Groups[1].Value;
        }
    }

    public class NotWire : ReferenceWire
    {
        public override ushort ResolveHelper(Circuit circuit) => (ushort)~base.ResolveHelper(circuit);

        public NotWire(Match match) : base(match) { }
    }

    public class ReferenceBinaryWire : Wire
    {
        public string left;
        public string right;

        public ReferenceBinaryWire(Match match)
        {
            Name = match.Groups[3].Value;
            left = match.Groups[1].Value;
            right = match.Groups[2].Value;
        }
    }

    public class MixedWire : ReferenceWire
    {
        public ushort number;

        public MixedWire(Match match)
        {
            Name = match.Groups[3].Value;
            try
            {
                number = ushort.Parse(match.Groups[1].Value);
                wire = match.Groups[2].Value;
            }
            catch (FormatException)
            {
                number = ushort.Parse(match.Groups[2].Value);
                wire = match.Groups[1].Value;
            }
        }
    }

    public class MixedAndWire : MixedWire
    {
        public override ushort ResolveHelper(Circuit circuit) => (ushort)(number & circuit[wire]);
        public MixedAndWire(Match match) : base(match) { }
    }

    public class ReferenceAndWire : ReferenceBinaryWire
    {
        public override ushort ResolveHelper(Circuit circuit) => (ushort)(circuit[left] & circuit[right]);
        public ReferenceAndWire(Match match) : base(match) { }
    }

    public class ReferenceOrWire : ReferenceBinaryWire
    {
        public override ushort ResolveHelper(Circuit circuit) => (ushort)(circuit[left] | circuit[right]);
        public ReferenceOrWire(Match match) : base(match) { }
    }

    public class LeftShiftWire : MixedWire
    {
        public override ushort ResolveHelper(Circuit circuit) => (ushort)(circuit[wire] << number);
        public LeftShiftWire(Match match) : base(match) { }
    }

    public class RightShiftWire : MixedWire
    {
        public override ushort ResolveHelper(Circuit circuit) => (ushort)(circuit[wire] >> number);
        public RightShiftWire(Match match) : base(match) { }
    }
}
