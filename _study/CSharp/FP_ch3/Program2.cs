﻿//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Linq.Expressions;
//using System.Text;
//using System.Threading.Tasks;

//namespace FP_ch3
//{
//    //public partial class Program
//    //{
//    //    static void Main(string[] args)
//    //    {
//    //        int i = AreaRectangleDelegate(1, 2);
//    //        int j = AreaSquareDelegate(2, 3);

//    //        Console.WriteLine("i = " + i);
//    //        Console.WriteLine("j = " + j);

//    //        //PrintResultLambda();

//    //        //Console.WriteLine(
//    //        //    displayMessageDelegate(
//    //        //        "A simple lambda expression sample."));

//    //    }
//    //}
//    public partial class Program
//    {
//        static void Main(string[] args)
//        {
//            Expression<Func<int, int, int>> expression =
//                (a, b) => a * b;
//        }
//    }
//    public partial class Program
//    {
//        //private static Func<int, int, int> AreaRectangleDelegate =
//        //    delegate (int a, int b)
//        //    {
//        //        return a * b;
//        //    };
//        //private static Func<int, int, int> AreaSquareDelegate =
//        //    delegate (int x, int y)
//        //    {
//        //        return x * y;
//        //    };
//        private static Func<int, int, int> AreaRectangleDelegate =
//            (a, b) => a * b;
        
//        private static Func<int, int, int> AreaSquareDelegate =
//            (x, y) => x * y;
//    }


//    public partial class Program
//    {
//        private static bool IsMultipleOfSeven(int i)
//        {
//            return i % 7 == 0;
//        }
//    }
//    public partial class Program
//    {
//        private static int FindMultipleOfSeven(List<int> numList)
//        {
//            return numList.Find(IsMultipleOfSeven);
//        }
//    }
//    public partial class Program
//    {
//        private static void PrintResult()
//        {
//            Console.WriteLine(
//                "The Multiple of 7 from the number list is {0}",
//                FindMultipleOfSeven(numbers));
//        }
//    }
//    public partial class Program
//    {
//        static List<int> numbers = new List<int>()
//        {
//            54, 24, 91, 70, 72, 44, 61, 93,
//            73, 3, 56, 5, 38, 60, 29, 32,
//            86, 44, 34, 25, 22, 44, 66, 7,
//            9, 59, 70,47, 55, 95, 6, 42
//        };
//    }
//    public partial class Program
//    {
//        private static int FindMultipleOfSevenLambda(
//            List<int> numList)
//        {
//            return numList.Find(
//                    delegate (int i)
//                    {
//                        return i % 7 == 0;
//                    }
//                );
//        }
//    }
//    public partial class Program
//    {
//        private static void PrintResultLambda()
//        {
//            Console.WriteLine(
//                "({0}) The Multiple of 7 from the number list is {1}",
//                "Lambda",
//                FindMultipleOfSevenLambda(numbers));
//        }
//    }

//    public partial class Program
//    {
//        static Func<string, string> displayMessageDelegate =
//            str => String.Format("Message: {0}", str);
//    }
//}
