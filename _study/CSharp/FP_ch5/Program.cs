using System;
using System.Collections;
using System.Diagnostics.Metrics;
using System.Linq;

namespace SequencesAndElements
{
    public partial class Program
    {
        static void Main(string[] args)
        {
            UsingStaticMethod();
        }
    }

    public partial class Program
    {
        private static void NonDeferred()
        {
            List<int> intList = new List<int>
            {
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9
            };
            IEnumerable<int> queryInt = intList.Select(i => i * 2);
            int queryIntCount = queryInt.Count();
            List<int> queryIntCached = queryInt.ToList();
            int queryIntCachedCount = queryIntCached.Count();
            intList.Clear();
            Console.WriteLine(
                String.Format(
                    "Enumerate queryInt. Count {0}.", queryIntCount));
            foreach (int i in queryInt)
            {
                Console.WriteLine(i);
            }
            Console.WriteLine(String.Format(
                "Enumerate queryIntCached. Count {0}.",
                queryIntCachedCount));
            foreach (int i in queryIntCached)
            {
                Console.WriteLine(i);
            }
        }
    }
    public partial class Program
    {
        static int[] intArray =
        {
            0,  1,  2,  3,  4,  5,  6,  7,  8,  9,
            10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39,
            40, 41, 42, 43, 44, 45, 46, 47, 48, 49
        };
    }
    public partial class Program
    {
        public static void ExtractArray()
        {
            IEnumerable<int> extractedData =
                System.Linq.Enumerable.Where
                    (intArray, i => i.IsPrime());
            Console.WriteLine("Prime Number from 0 - 49 are:");
            foreach (int i in extractedData)
                Console.WriteLine("{0} \t", i);
            Console.WriteLine();
        }
        public static void ExtractArrayWithMethodSyntax()
        {
            IEnumerable<int> extractedData =
                intArray.Where(i => i.IsPrime());
            Console.WriteLine("Prime Number from 0 - 49 are:");
            foreach (int i in extractedData)
                Console.WriteLine("{0} \t", i);
            Console.WriteLine();
        }
    }
    public static class ExtensionMethods
    {
        public static bool IsPrime(this int i)
        {
            if ((i % 2) == 0)
            {
                return i == 2;
            }
            int sqrt = (int)Math.Sqrt(i);
            for (int t = 3; t <= sqrt; t = t + 2)
            {
                if (i % 2 == 0)
                {
                    return false;
                }
            }
            return i != 1;
        }
    }

    public partial class Program
    {
        public static void DeferredExecution()
        {
            List<Member> memberList = new List<Member>()
            {
                new Member
                {
                    ID = 1,
                    Name = "Eddie Morgan",
                    Gender = "Male",
                    MemberSince = new DateTime(2016, 2, 10)
                },
                new Member
                {
                    ID = 2,
                    Name = "Millie Duncan",
                    Gender = "Female",
                    MemberSince = new DateTime(2015, 4, 3)
                },
                new Member
                {
                    ID = 3,
                    Name = "Thiago Hubbard",
                    Gender = "Male",
                    MemberSince = new DateTime(2014, 1, 8)
                },
                new Member
                {
                    ID = 4,
                    Name = "Emilia Shaw",
                    Gender = "Female",
                    MemberSince = new DateTime(2015, 11, 15)
                }
            };
            IEnumerable<Member> memberQuery =
                from m in memberList
                where m.MemberSince.Year > 2014
                orderby m.Name
                select m;
            memberList.Add(new Member
            {
                ID = 5,
                Name = "Chloe Day",
                Gender = "Female",
                MemberSince = new DateTime(2016, 5, 28)
            });
            foreach (Member m in memberQuery)
            {
                Console.WriteLine(m.Name);
            }
        }
    }
    public class Member
    {
        public int ID { get; set; }
        public string Name { get; set; }
        public string Gender { get; set; }
        public DateTime MemberSince { get; set; }
    }

    public partial class Program
    {
        private static void UsingExtensionMethod()
        {
            IEnumerable<string> query =
            names
                .Where(n => n.Length > 4)
                .OrderBy(n => n[0])
                .Select(n => n.ToUpper());

            //IEnumerable<string> query = Enumerable.Select(
            //    Enumerable.OrderBy(Enumerable.Where(names, n => n.Length > 4),
            //    n => n[0]), n => n.ToUpper());

            foreach (string s in query)
            {
                Console.WriteLine(s);
            }
        }
    }

    public partial class Program
    {
        private static void UsingStaticMethod()
        {
            IEnumerable<string> query = 
                Enumerable.Select(
                    Enumerable.OrderBy(
                        Enumerable.Where(
                            names, n => n.Length > 4),
                    n => n[0]), n => n.ToUpper());
            foreach (string s in query)
            {
                Console.WriteLine(s);
            }
        }
    }
    public partial class Program
    {
        static List<string> names = new List<string>
        {
            "Howard", "Pat",
            "Jaclyn", "Kathryn",
            "Ben", "Aaron",
            "Stacey", "Levi",
            "Patrick", "Tara",
            "Joe", "Ruby",
            "Bruce", "Cathy",
            "Jimmy", "Kim",
            "Kelsey", "Becky",
            "Scott", "Dick"
        };
    }
}
