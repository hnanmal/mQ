using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace System
{
    public static class ExtensionMethodsClass
    {
        public static byte[] ConvertToHex (this string str)
        {
            int i = 0;
            byte[] HexArray = new byte[str.Length];

            foreach (char ch in str)
            {
                HexArray[i++] = Convert.ToByte(ch);
            }

            return HexArray;
        }
    }
}

//namespace PiggybackingNamespace
//{
//    class Program
//    {
//        static void Main(string[] args)
//        {
//            int i = 0;
//            string strData = "Piggybacking";
//            byte[] byteData = strData.ConvertToHex();
//            foreach (char c in byteData)
//            {
//                Console.WriteLine("{0} = 0x{1:X2} ({2})",
//                    c.ToString(),
//                    byteData[i],
//                    byteData[i++]);
//            }
//        }
//    }
//}