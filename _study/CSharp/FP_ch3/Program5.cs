//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;

//namespace FP_ch3
//{
//    public partial class Program
//    {
//        static void Main(string[] args)
//        {
//            //firstClassConcept();

//            firstClassConcept2(
//                displayMessageDelegate,
//                "Pass lambda expression to argument");
//        }
//    }
//    public partial class Program
//    {
//        static Func<string, string> displayMessageDelegate =
//            str => String.Format("Message: {0}", str);
//    }
//    public partial class Program
//    {
//        static private void firstClassConcept()
//        {
//            string str = displayMessageDelegate(
//                "Assign displayMessageDelegate( ) to variable");
//            Console.WriteLine(str);
//        }
//    }
//    public partial class Program
//    {
//        static private void firstClassConcept2(
//            Func<string, string> funct,
//            string message)
//        {
//            Console.WriteLine(funct(message));
//        }
//    }
//}
