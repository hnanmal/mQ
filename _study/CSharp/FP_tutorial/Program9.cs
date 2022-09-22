//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;

////class Program
////{
////    static void Main(string[] args)
////    {
////        Console.WriteLine(
////            Encoding.UTF8.GetString(
////                new byte[]
////                {
////                    0x70, 0x69, 0x70, 0x65, 0x6C,
////                    0x69, 0x6E, 0x69, 0x6E, 0x67
////                })
////            );
////    }
////}

////class Program
////{
////    static void Main(string[] args)
////    {
////        var bytes = new byte[]
////        {
////                    0x70, 0x69, 0x70, 0x65, 0x6C,
////                    0x69, 0x6E, 0x69, 0x6E, 0x67
////        };
////        var stringFromBytes = Encoding.UTF8.GetString(bytes);
////        Console.WriteLine(stringFromBytes);
////    }
////}

////class Program
////{
////    static void Main(string[] args)
////    {
////        var sb = new StringBuilder("0123", 10);
////        sb.Append(new char[] { '4', '5', '6' });
////        sb.AppendFormat("{0}{1}{2}", 7, 8, 9);
////        sb.Insert(0, "number: ");
////        sb.Replace('n', 'N');
////        var str = sb.ToString();
////        Console.WriteLine(str);
////    }
////}

//class Program
//{
//    static void Main(string[] args)
//    {
//        var str =
//            new StringBuilder("0123", 10)
//            .Append(new char[] { '4', '5', '6' })
//            .AppendFormat("{0}{1}{2}", 7, 8, 9)
//            .Insert(0, "number: ")
//            .Replace('n', 'N')
//            .ToString();
//        Console.WriteLine(str);
//    }
//}