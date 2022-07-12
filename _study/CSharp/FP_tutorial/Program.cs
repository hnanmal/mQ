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

class Program
{
    delegate int DoubleAction(int inp);

    static void Main(string[] args)
    {
        DoubleAction da = Double;
        int doubledValue = da(2);
    }

    static int Double(int input)
    {
        return input * 2;
    }
}