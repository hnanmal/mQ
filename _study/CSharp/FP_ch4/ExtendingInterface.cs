using ExtendingInterface;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ExtendingInterface
{
    public class DataItem
    {
        public string Name { get; set; }
        public string Gender { get; set; }
    }
}

namespace ExtendingInterface
{
    public interface IDataSource
    {
        IEnumerable<DataItem> GetItems();
    }
}

public class Program
{
    static void Main(string[] args)
    {
        ClubMember cm = new ClubMember();
        foreach (var item in cm.GetItems())
        {
            Console.WriteLine(
                "Name: {0}\tGender: {1}",
                item.Name,
                item.Gender);
        }
    }
}

public partial class ClubMember : IDataSource
{
    public IEnumerable<DataItem> GetItems()
    {
        foreach (var item in DataItemList)
        {
            yield return item;
        }
    }
}

public partial class ClubMember : IDataSource
{
    List<DataItem> DataItemList =
        new List<DataItem>()
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
                Gender ="Female"},
            new DataItem {
                Name ="Conner Avery",
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