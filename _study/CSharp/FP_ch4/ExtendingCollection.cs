using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ExtendingInterface;

namespace ExtendingInterface
{
    public static class IDataSourceExtension
    {
        public static IEnumerable<DataItem> GetItemsByGender(
            this IDataSource src,
            string gender)
        {
            foreach (DataItem item in src.GetItems())
            {
                if (item.Gender == gender)
                    yield return item;
            }
        }
    }
}
namespace FP_ch4
{
    public static partial class IDataSourceCollectionExtension
    {
        public static IEnumerable<DataItem> GetAllItemsByGender_IEnum(
            this IEnumerable src, string gender)
        {
            var items = new List<DataItem>();
            foreach (var s in src)
            {
                var refDataSource = s as IDataSource;
                if (refDataSource != null)
                {
                    items.AddRange(refDataSource.GetItemsByGender(gender));
                }
            }
            return items;
        }
    }

    public static partial class IDataSourceCollectionExtension
    {
        public static IEnumerable<DataItem>
            GetAllItemsByGender_IEnumTemplate
                (this IEnumerable<IDataSource> src, string gender)
        {
            return src.SelectMany(x => x.GetItemsByGender(gender));
        }
    }

    public class ClubMember1 : IDataSource
    {
        public IEnumerable<DataItem> GetItems()
        {
            return new List<DataItem>
            {
                new DataItem {
                    Name ="Dorian Villarreal",
                    Gender ="Male"},
                new DataItem {
                    Name ="Olivia Bradley",
                    Gender ="Female"},
                new DataItem {
                    Name ="Jocelyn Garrison",
                    Gender ="Female"},
                new DataItem {
                    Name ="Connor Hopkins",
                    Gender ="Male"},
                new DataItem {
                    Name ="Rose Moore",
                    Gender ="Female"}
            };
        }
    }
    public class ClubMember2 : IDataSource
    {
        public IEnumerable<DataItem> GetItems()
        {
            return new List<DataItem>
            {
                new DataItem {
                    Name ="Connor Avery",
                    Gender ="Male"},
                new DataItem {
                    Name ="Lexie Irwin",
                    Gender ="Female"},
                new DataItem {
                    Name ="Bobby Armstrong",
                    Gender ="Male"},
                new DataItem {
                    Name ="Stanley Wilson",
                    Gender ="Male"},
                new DataItem {
                    Name ="Chloe Steele",
                    Gender ="Female"}
            };
        }
    }
    //public class Program
    //{
    //    static void Main(string[] args)
    //    {
    //        var sources = new IDataSource[]
    //        {
    //            new ClubMember1(),
    //            new ClubMember2()
    //        };
    //        var items = sources.GetAllItemsByGender_IEnum("Female");
    //        Console.WriteLine("Invoking GetAllItemsByGender_IEnum()");
    //        foreach (var item in items)
    //        {
    //            Console.WriteLine(
    //                "Name: {0}\tGender: {1}",
    //                item.Name,
    //                item.Gender);
    //        }
    //    }
    //}
    public class Program
    {
        static void Main(string[] args)
        {
            var sources = new IDataSource[]
            {
                new ClubMember1(),
                new ClubMember2()
            };
            var items = 
                sources.GetAllItemsByGender_IEnumTemplate(
                    "Female");
            Console.WriteLine(
                "Invoking GetAllItemsByGender_IEnumTemplate()");
            foreach (var item in items)
            {
                Console.WriteLine(
                    "Name: {0}\tGender: {1}",
                    item.Name,
                    item.Gender);
            }
        }
    }
}
