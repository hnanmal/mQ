using System;
namespace ReferencingNamespaceLib
{
    public static class ExtensionMethodsClass
    {
        public static byte[] ConvertToHex(this string str)
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

public static class ExtensionMethods
{
    //static void Main(string[] args)
    //{
    //    string[] strArray =
    //    {
    //        "room",
    //        "level",
    //        "channel",
    //        "heat",
    //        "burn",
    //        "madam",
    //        "machine",
    //        "jump",
    //        "radar",
    //        "brain"
    //    };
    //    foreach (string s in strArray)
    //    {
    //        Console.WriteLine("{0} = {1}", s, s.IsPalindrome());
    //    }
    //}
    public static bool IsPalindrome(this string str)
    {
        char[] array = str.ToCharArray();
        Array.Reverse(array);
        string backwards = new string(array);
        return str == backwards;
    }
}