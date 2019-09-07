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
            var results = SolveBothParts(input);
            return FormatReport(
                results.partOne,
                results.partTwo
            );
        }

        public static Circuit ParseInput(string input)
        {
            Circuit circuit = new Circuit();
            input.Trim().Split('\n').ToList().ForEach(circuit.Add);
            return circuit;
        }

        public static (ushort partOne, ushort partTwo) SolveBothParts(string input)
        {
            Circuit circuit = ParseInput(input);
            ushort partOneResult = circuit["a"];
            circuit.Reset();
            circuit.Add($"{partOneResult} -> b");
            ushort partTwoResult = circuit["a"];
            return (partOneResult, partTwoResult);
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

    public class Wire
    {
        public string Name { get; }
        private string[] parts;

        private ushort? cached;
        public ushort Resolve(Circuit circuit)
        {
            if (!cached.HasValue)
            {
                cached = ResolveHelper(circuit, parts);
            }
            return cached.Value;
        }

        private delegate ushort WireFunction(Circuit circuit, string[] parts);
        private WireFunction ResolveHelper;

        public void Reset()
        {
            cached = null;
        }

        private Wire(string[] parts, WireFunction resolver)
        {
            this.parts = parts;
            this.Name = parts.Last();
            this.ResolveHelper = resolver;
        }

        public static Wire FromString(string input)
        {
            WireFunction immediate =
                (circuit, parts) => ushort.Parse(parts[0]);
            WireFunction wire =
                (circuit, parts) => circuit[parts[0]];
            WireFunction not =
                (circuit, parts) => (ushort)~circuit[parts[1]];
            WireFunction mixedAnd =
                (circuit, parts) => (ushort)(ushort.Parse(parts[0]) & circuit[parts[2]]);
            WireFunction wireAnd =
                (circuit, parts) => (ushort)(circuit[parts[0]] & circuit[parts[2]]);
            WireFunction wireOr =
                (circuit, parts) => (ushort)(circuit[parts[0]] | circuit[parts[2]]);
            WireFunction leftShift =
                (circuit, parts) => (ushort)(circuit[parts[0]] << ushort.Parse(parts[2]));
            WireFunction rightShift =
                (circuit, parts) => (ushort)(circuit[parts[0]] >> ushort.Parse(parts[2]));

            string[] inputParts = input.Split();
            bool startsWithDigit = Char.IsDigit(inputParts[0][0]);
            Regex operatorRegex = new Regex(@"\b(NOT|AND|OR|LSHIFT|RSHIFT)\b");

            switch (operatorRegex.Match(input).Groups[1].Value)
            {
                case "NOT":
                    return new Wire(inputParts, not);
                case "AND":
                    return new Wire(inputParts, startsWithDigit ? mixedAnd : wireAnd);
                case "OR":
                    return new Wire(inputParts, wireOr);
                case "LSHIFT":
                    return new Wire(inputParts, leftShift);
                case "RSHIFT":
                    return new Wire(inputParts, rightShift);
                default:
                    return new Wire(inputParts, startsWithDigit ? immediate : wire);
            }
            throw new ArgumentException($"No wire operation for input: `{input}`");
        }
    }
}
