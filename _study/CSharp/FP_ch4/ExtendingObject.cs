using ExtendingInterface;
using FP_ch4;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

public static class ObjectExtention
{
    public class DataItem
    {
        public string Name { get; set; }
        public string Gender { get; set; }
    }
    public static void WriteToConsole(this object o,  string objectName)
    {
        Console.WriteLine(
            String.Format(
                "{0}: {1}\n",
                objectName,
                o.ToString()));
    }

    //public class Program
    //{
    //    static void Main(string[] args)
    //    {
    //        var obj1 = UInt64.MaxValue;
    //        obj1.WriteToConsole(nameof(obj1));

    //        var obj2 = new DateTime(2016, 1, 1);
    //        obj2.WriteToConsole(nameof(obj2));

    //        var obj3 = new DataItem
    //        {
    //            Name = "Macros Raymond",
    //            Gender = "Male"
    //        };
    //        obj3.WriteToConsole(nameof(obj3));

    //        IEnumerable<IDataSource> obj4 =
    //            new List<IDataSource>
    //            {
    //                new ClubMember1(),
    //                new ClubMember2()
    //            };
    //        obj4.WriteToConsole(nameof(obj4));
    //    }
    //}
}
