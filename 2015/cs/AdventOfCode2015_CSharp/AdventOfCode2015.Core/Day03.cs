using System;
using System.Collections.Generic;
using System.Linq;

namespace AdventOfCode2015.Core
{
    public class Day03 : Solution2015
    {
        public override int Day => 3;
        public override string Title => "Perfectly Spherical Houses in a Vacuum";

        public override string Run(string input)
        {
            List<Point> parsed = ParseInput(input);
            return FormatReport(SolvePartOne(parsed));
        }

        public static List<Point> ParseInput(string input)
        {
            return input.Select(c =>
            {
                switch (c)
                {
                    case '^':
                        return new Point(0, 1);
                    case 'v':
                        return new Point(0, -1);
                    case '<':
                        return new Point(-1, 0);
                    case '>':
                        return new Point(1, 0);
                    default:
                        throw new ArgumentException($"Invalid direction character: {c}");
                }
            }).ToList();
        }

        public int SolvePartOne(List<Point> directions)
        {
            return VisitedLocations(directions).Count;
        }

        HashSet<Point> VisitedLocations(List<Point> directions)
        {
            HashSet<Point> visited = new HashSet<Point>();
            Point origin = Point.Origin();
            visited.Add(origin);

            // We don’t use the result of the aggregate (reduce), which is the final location
            // visited by Santa. However, the reduce procedure is a natural way to express the
            // current location as a result of accumulating individual movement deltas.
            directions.Aggregate(origin, (currentPosition, movementDelta) =>
            {
                Point newLocation = currentPosition + movementDelta;
                visited.Add(newLocation);
                return newLocation;
            });

            return visited;
        }

        public int SolvePartTwo(List<Point> directions)
        {
            return new int[] { 0, 1 }
                .Select(remainder =>
                    Utils.EnumerateSequence(directions)
                        .Where(t => t.Index % 2 == remainder)
                        .Select(t => t.Element)
                        .ToList()
                )
                .Select(VisitedLocations)
                .Aggregate((combined, locations) =>
                {
                    combined.UnionWith(locations);
                    return combined;
                })
                .Count;
        }
    }
}
