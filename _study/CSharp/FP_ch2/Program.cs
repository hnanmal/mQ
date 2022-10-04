using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FP_ch2
{
    public partial class Program
    {
        static void Main(string[] args)
        {
            ContravarianceTextWriterInvoke();
        }
    }
    public partial class Program
    {
        private delegate void ContravarianceDelegate(StreamWriter sw);
    }
    public partial class Program
    {
        private static void TextWriterMethod(TextWriter tw)
        {
            string[] arrString = new string[]
            {
                "Contravariance",
                "example",
                "using",
                "TextWriter",
                "object"
            };
            tw = new StreamWriter(Console.OpenStandardOutput());
            foreach (string str in arrString)
            {
                tw.Write(str);
                tw.Write(' ');
            }
            tw.WriteLine();
            Console.SetOut(tw);
            tw.Flush();
        }
    }
    public partial class Program
    {
        private static void ContravarianceTextWriterInvoke()
        {
            ContravarianceDelegate contravDelgate = TextWriterMethod;
            TextWriter tw = null;
            Console.WriteLine(
                "Invoking ContravarianceTextWriterInvoke method:");
            contravDelgate((StreamWriter)tw);
        }
    }
}
