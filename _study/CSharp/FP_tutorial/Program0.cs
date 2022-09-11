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


//        // Func < T1, T2, T3, ..., T16, TResult >
//    }
//}

//class Program
//{
//    delegate int DoubleAction(int inp);

//    static void Main(string[] args)
//    {
//        DoubleAction da = Double;
//        int doubledValue = da(2);
//        Console.WriteLine(doubledValue);
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
//        Func<int, int> da = (i) => i * 2;

//        int doubledValue = da(2);
//        Console.WriteLine(doubledValue);
//    }
//}