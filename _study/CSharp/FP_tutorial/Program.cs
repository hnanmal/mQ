using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

//public partial class Program
//{
//    private static  int GetFactorial(int intNumber)
//    {
//        if (intNumber == 0)
//        {
//            return 1;
//        }

//        return intNumber * GetFactorial(intNumber - 1);
//    }
//}

//public partial class Program
//{
//    static void Main_(string[] args)
//    {
//        Console.WriteLine(
//            "Enter an interger number (Imperative approach)");
//        int inputNumber = Convert.ToInt32(Console.ReadLine());
//        int factorialNumber = GetFactorial(inputNumber);
//        Console.WriteLine(
//            "{0}! is {1}",
//            inputNumber,
//            factorialNumber);
//    }
//}

public partial class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine(
            "Enter an interger number (Functional approach)");
        int inputNumber = Convert.ToInt32(Console.ReadLine());
        IEnumerable<int> ints = Enumerable.Range(1, inputNumber);
        int factorialNumber = ints.Aggregate((f, s) => f * s);
        Console.WriteLine(
            "{0}! is {1}",
            inputNumber,
            factorialNumber);
    }
}