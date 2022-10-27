using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ModifyingExistingMethod
{
    public class Program
    {
        static void Main(string[] args)
        {
            string str = "This is string";
            Console.WriteLine(str.ToString());
        }
    }
    public static class ExtentionMethods
    {
        public static string ToString(this string str)
        {
            return "ToString() extension method";
        }
    }
}
