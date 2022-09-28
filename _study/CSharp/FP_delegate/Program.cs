using System;

namespace FP_delegate
{
    public partial class Program
    {
        private delegate void CalculatorDelegate(int a, int b);
    }

    public partial class Program
    {
        public static void Add(int x, int y)
        {
            Console.WriteLine(
                "{0) + {1} = {2}".Replace("{", "{{").Replace("}", "}}"),
                x,
                y,
                x + y);
        }

        public static void Subtract(int x, int y)
        {
            Console.WriteLine(
                "{0} - {1} = {2}".Replace("{", "{{").Replace("}", "}}"),
                x,
                y,
                x - y);
        }

        public static void Multiply(int x, int y)
        {
            Console.WriteLine(
                "{0} * {1} = {2}".Replace("{", "{{").Replace("}", "}}"),
                x,
                y,
                x * y);
        }

        public static void Division(int x, int y)
        {
            Console.WriteLine(
                "{0} / {1} = {2}".Replace("{", "{{").Replace("}", "}}"),
                x,
                y,
                x / y);
        }
    }

    public partial class Program
    {
        private static void CombineDelegate()
        {
            CalculatorDelegate calcMultiples =
                (CalculatorDelegate)Delegate.Combine(
                    new CalculatorDelegate[]
                    {
                        Add,
                        Subtract,
                        Multiply,
                        Division
                    });
            Delegate[] calcList = calcMultiples.GetInvocationList();
            Console.WriteLine(
                "Total delegates in calcMultiples: {0}",
                calcList.Length);

            calcMultiples(6, 3);
        }
        static void Main(string[] args)
        {
            CombineDelegate();
        }
    }
}
