using System;
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
            throw new NotImplementedException();
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
