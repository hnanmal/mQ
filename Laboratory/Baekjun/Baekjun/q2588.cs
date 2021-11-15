//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;

//namespace Baekjun
//{
//    class q2588
//    {

//        static void Main(string[] args)
//        {
//            string v1 = Console.ReadLine();
//            string v2 = Console.ReadLine();
//            char[] cv2 = v2.ToCharArray();

//            string sv2_0 = cv2[0].ToString();
//            string sv2_1 = cv2[1].ToString();
//            string sv2_2 = cv2[2].ToString();

//            int v3 = int.Parse(v1) * int.Parse(sv2_2);
//            int v4 = int.Parse(v1) * int.Parse(sv2_1);
//            int v5 = int.Parse(v1) * int.Parse(sv2_0);

//            int v6 = (v3 * 1) + (v4 * 10) + (v5 * 100);

//            Console.WriteLine(v3);
//            Console.WriteLine(v4);
//            Console.WriteLine(v5);
//            Console.WriteLine(v6);

//        }
//    }
//}
