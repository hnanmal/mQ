//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Linq.Expressions;
//using System.Text;
//using System.Threading.Tasks;

//namespace FP_ch3
//{
//    public partial class Program
//    {
//        static void Main(string[] args)
//        {
//            Expression<Func<int, int, int>> expression =
//                (a, b) => a * b;
//            //exploreBody(expression);

//            compilingExpr(expression);
//        }
//    }
//    //public partial class Program
//    //{
//    //    static void Main(string[] args)
//    //    {
//    //        Expression<Func<int, int, int>> expression =
//    //            (a, b) => a * b;
//    //    }
//    //}
//    public partial class Program
//    {
//        private static void exploreBody(
//            Expression<Func<int, int, int>> expr)
//        {
//            BinaryExpression body =
//                (BinaryExpression)expr.Body;
//            ParameterExpression left =
//                (ParameterExpression)body.Left;
//            ParameterExpression right =
//                (ParameterExpression)body.Right;
//            Console.WriteLine(expr.Body);
//            Console.WriteLine(
//                "\tThe left part of the expression: {0}\n" +
//                "\tThe NodeType: {1}\n" +
//                "\tThe right part: {2}\n" +
//                "\tThe Type: {3}\n",
//                left.Name,
//                body.NodeType,
//                right.Name,
//                body.Type);
//        }
//    }
//    public partial class Program
//    {
//        private static void compilingExpr(
//            Expression<Func<int, int, int>> expr)
//        {
//            int a = 2;
//            int b = 3;
//            int compResult = expr.Compile()(a, b);
//            Console.WriteLine(
//                "The result of expression {0}" +
//                " with a = {1} and b = {2} is {3}",
//                expr.Body,
//                a,
//                b,
//                compResult);
//        }
//    }
//}
