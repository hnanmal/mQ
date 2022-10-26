using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace CodeReadability
{
    public static class HelperMethods
    {
        public static string TrimAllSpace(string str)
        {
            string retValue = "";
            foreach (char c in str)
            {
                retValue += !char.IsWhiteSpace(c) ? c.ToString() : "";
            }
            return retValue;
        }
        public static string Capitalize(string str)
        {
            string retValue = "";
            string[] allWords = str.Split(' ');
            foreach (string s in allWords)
            {
                retValue += s.First()
                    .ToString()
                    .ToUpper()
                    + s.Substring(1)
                    + " ";
            }
            return retValue.Trim();
        }
    }
}

namespace CodeReadability
{
    public static class ExtensionMethods
    {
        public static string TrimAllSpace(this string str)
        {
            string retValue = "";
            foreach (char c in str)
            {
                retValue += !char.IsWhiteSpace(c) ? c.ToString() : "";
            }
            return retValue;
        }
        public static string Capitalize(this string str)
        {
            string retValue = "";
            string[] allWords = str.Split(' ');
            foreach (string s in allWords)
            {
                retValue += s.First()
                    .ToString()
                    .ToUpper()
                    + s.Substring(1)
                    + " ";
            }
            return retValue.Trim();
        }
        static void Main(string[] args)
        {
            string sntc = "";
            foreach (string str in sentences)
            {
                string strTemp = str;
                strTemp = HelperMethods.TrimAllSpace(strTemp);
                strTemp = HelperMethods.Capitalize(strTemp);
                sntc += strTemp + " ";
            }
            Console.WriteLine(sntc.Trim());
        }
        static string[] sentences = new string[]
        {
            " h o w ",
            " t o ",
            " a p p l y ",
            " e x t e n s i o n ",
            " m e t h o d s ",
            " i n ",
            " c s h a r p ",
            " p r o g r a m m i n g "
        };
    }
}
