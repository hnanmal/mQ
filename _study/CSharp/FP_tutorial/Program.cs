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




public class Program
{
    public static int GetFactorial(int intNumber)
    {
        if (intNumber == 0)
        {
            return 1;
        }

        return intNumber * GetFactorial(intNumber - 1);
    }

    //static void Main(string[] args)
    //{
    //    Console.WriteLine(
    //        "Enter an integer number (Imperative approach)");
    //    int inputNumber = Convert.ToInt32(Console.ReadLine());
    //    int factorialNumber = GetFactorial(inputNumber);
    //    Console.WriteLine(
    //        "{0}! is {1}",
    //        inputNumber,
    //        factorialNumber);
    //}
}