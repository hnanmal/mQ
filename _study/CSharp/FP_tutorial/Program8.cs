//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;

//public partial class Program
//{
//    public static int NonCurriedAdd(int a, int b) => a + b;
//}

//public partial class Program
//{
//    static void Main(string[] args)
//    {
//        int add = NonCurriedAdd(2, 3);
//        Console.WriteLine(add);
//    }
//}

//public partial class Program
//{
//    public static Func<int, int> CurriedAdd(int a) => b => a + b;
//}

//public partial class Program
//{
//    public static void CurriedStyle()
//    {
//        int add = CurriedAdd(2)(3);
//        Console.WriteLine(add);
//    }
//}

//public partial class Program
//{
//    public static void CurriedStyle2()
//    {
//        var addition = CurriedAdd(2);

//        int x = addition(3);
//        Console.WriteLine(x);
//    }
//}