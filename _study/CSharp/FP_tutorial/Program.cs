//class Program
//{
//    static void Main(string[] args)
//    {
//        Func<int, int> f = (x) => x + 2;
//        int i = f(1);
//        Console.WriteLine(i);

//        f = (x) => 2 * x + 1;
//        i = f(1);
//        Console.WriteLine(i);
//    }
//}

//class Program
//{
//    delegate int DoubleAction(int inp);

//    static void Main(string[] args)
//    {
//        DoubleAction da = Double;
//        int doubledValue = da(2);
//    }

//    static int Double(int input)
//    {
//        return input * 2;
//    }
//}


//class Program
//{
//    static void Main(string[] args)
//    {
//        Func<int, int> da =
//            (i) => i * 2;

//        int doubledValue = da(2);

//        int i = da(1);
//    }
//}


//class Program
//{
//    //private static string strValue = "First";

//    //public static void AddSpace(string str)
//    //{
//    //    strValue += ' ' + str;
//    //}

//    //static void Main(string[] args)
//    //{
//    //    AddSpace("Second!");
//    //    AddSpace("Third!!");
//    //    Console.WriteLine(strValue);
//    //}

//    public static string AddSpace(string strSource, string str)
//    {
//        return (strSource + " " + str);
//    }

//    static void Main(string[] args)
//    {
//        string str1 = "First";
//        string str2 = AddSpace(str1, "Second");
//        string str3 = AddSpace(str2, "Third");
//        Console.WriteLine(str3);
//    }
//}




//public class Program
//{
//    public static int GetFactorial(int intNumber)
//    {
//        if (intNumber == 0)
//        {
//            return 1;
//        }

//        return intNumber * GetFactorial(intNumber - 1);
//    }

//    //static void Main(string[] args)
//    //{
//    //    Console.WriteLine(
//    //        "Enter an integer number (Imperative approach)");
//    //    int inputNumber = Convert.ToInt32(Console.ReadLine());
//    //    int factorialNumber = GetFactorial(inputNumber);
//    //    Console.WriteLine(
//    //        "{0}! is {1}",
//    //        inputNumber,
//    //        factorialNumber);
//    //}
//}

//public partial class Program
//{
//    public static int f(int x)
//    {
//        return (4 * x * x - 14 * x - 8);
//    }
//}

//public partial class Program
//{
//    static void Main(string[] args)
//    {
//        int i = f(5);
//        Console.WriteLine(i);
//    }
//}

//public partial class Program
//{
//    //public static string GetSign(int val)
//    //{
//    //    string pos0rNeg;

//    //    if (val > 0)
//    //        pos0rNeg = "positive";
//    //    else
//    //        pos0rNeg = "negative";

//    //    return pos0rNeg;
//    //}
//    public static string GetSign(int val)
//    {
//        return val > 0 ? "positive" : "negative";
//    }
//}

//public partial class Program
//{
//    static void Main(string[] args)
//    {
//        Console.WriteLine(
//            "Sign of -15 is {0}",
//            GetSign(-15));
//    }
//}

public partial class Program
{
    static List<int> NthFunctional(List<int> list, int n)
    {
        return list.Where((x, i) => i % n == 0).ToList();
    }
}

public partial class Program
{
    static void Main(string[] args)
    {
        List<int> listing =
            new List<int>()
            {
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16
            };
        var list3rd_funct = NthFunctional(listing, 3);
        PrintIntList("Nth Functional", list3rd_funct);
    }
}

public partial class Program
{
    static void PrintIntList(
        string titleHeader,
        List<int> list)
    {
        Console.WriteLine(
            String.Format("{0}",
            titleHeader));

        foreach (int i in list)
        {
            Console.Write(String.Format("{0}\t", i));
        }

        Console.WriteLine("\n");
    }
}