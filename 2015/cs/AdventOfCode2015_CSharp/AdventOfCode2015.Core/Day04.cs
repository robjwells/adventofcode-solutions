using System.Text;
using System.Security.Cryptography;

namespace AdventOfCode2015.Core
{
    public class Day04 : Solution2015
    {
        public override int Day => 4;
        public override string Title => "The Ideal Stocking Stuffer";

        public override string Run(string input)
        {
            int suffixForFiveZeroes = SolvePartOne(input);
            int suffixForSixZeroes = SolvePartTwo(input, suffixForFiveZeroes);
            return FormatReport(
                suffixForFiveZeroes,
                suffixForSixZeroes
            );
        }

        public int SolvePartOne(string secretKey)
        {
            return IterateMD5UntilPrefix(secretKey, "00000");
        }

        public int SolvePartTwo(string secretKey, int fiveZeroesSuffix)
        {
            return IterateMD5UntilPrefix(secretKey, "000000", startFrom: fiveZeroesSuffix);
        }

        public int IterateMD5UntilPrefix(string secretKey, string digestPrefix, int startFrom = 0)
        {
            int suffix = startFrom;
            string digest;
            while (true)
            {
                digest = HashDigest($"{secretKey}{suffix}");
                if (digest.StartsWith(digestPrefix))
                {
                    break;
                }
                suffix += 1;
            }
            return suffix;
        }

        public static string HashDigest(string message)
        {
            using (MD5 hasher = MD5.Create())
            {
                byte[] messageBytes = Encoding.UTF8.GetBytes(message);
                byte[] hashBytes = hasher.ComputeHash(messageBytes);
                StringBuilder builder = new StringBuilder();
                foreach (byte b in hashBytes)
                {
                    builder.Append(b.ToString("x2"));
                }
                return builder.ToString();
            }
        }
    }
}
