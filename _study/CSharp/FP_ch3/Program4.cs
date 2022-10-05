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
//            CreateAndRaiseEvent();
//        }
//    }
//    public class EventClassWithoutEvent
//    {
//        public Action OnChange { get; set; }
//        public void Raise()
//        {
//            if (OnChange != null)
//            {
//                OnChange();
//            }
//        }
//    }
//    public class EventClassWithEvent
//    {
//        public event Action OnChange = () => { };
//        public void Raise()
//        {
//            OnChange();
//        }
//    }
//    public partial class Program
//    {
//        //private static void CreateAndRaiseEvent()
//        //{
//        //    EventClassWithoutEvent ev = new EventClassWithoutEvent();
//        //    ev.OnChange += () =>
//        //        Console.WriteLine("1st: Event raised");
//        //    ev.OnChange += () =>
//        //        Console.WriteLine("2nd: Event raised");
//        //    ev.OnChange += () =>
//        //        Console.WriteLine("3rd: Event raised");
//        //    ev.OnChange += () =>
//        //        Console.WriteLine("4th: Event raised");
//        //    ev.OnChange += () =>
//        //        Console.WriteLine("5th: Event raised");
//        //    ev.Raise();
//        //}
//    }
//    public partial class Program
//    {
//        private static void CreateAndRaiseEvent2()
//        {
//            EventClassWithEvent ev = new EventClassWithEvent();
//            ev.OnChange += () =>
//                Console.WriteLine("1st: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("2nd: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("3rd: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("4th: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("5th: Event raised");
//            ev.Raise();

//        }
//    }
//    public partial class Program
//    {
//        private static void CreateAndRaiseEvent3()
//        {
//            EventClassWithoutEvent ev = new EventClassWithoutEvent();
//            ev.OnChange += () => 
//                Console.WriteLine("1st: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("2nd: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("3rd: Event raised");
//            ev.OnChange();
//            ev.OnChange += () =>
//                Console.WriteLine("4th: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("5th: Event raised");
//            ev.Raise();
//        }
//    }
//    public partial class Program
//    {
//        private static void CreateAndRaiseEvent4()
//        {
//            EventClassWithEvent ev = new EventClassWithEvent();
//            ev.OnChange += () =>
//                Console.WriteLine("1st: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("2nd: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("3rd: Event raised");
//            //ev.OnChange();
//            ev.OnChange += () =>
//                Console.WriteLine("4th: Event raised");
//            ev.OnChange += () =>
//                Console.WriteLine("5th: Event raised");
//            ev.Raise();
//        }
//    }
//    public class MyArgs : EventArgs
//    {
//        public int Value { get; set; }
//        public MyArgs(int value)
//        {
//            Value = value;
//        }
//    }
//    public class EventClassWithEventHandler
//    {
//        public event EventHandler<MyArgs> OnChange =
//            (sender, e) => { };
//        public void Raise()
//        {
//            OnChange(this, new MyArgs(100));
//        }
//    }
//    public partial class Program
//    {
//        private static void CreateAndRaiseEvent()
//        {
//            EventClassWithEventHandler ev = 
//                new EventClassWithEventHandler();
//            ev.OnChange += (sender, e)
//                => Console.WriteLine(
//                    "Event raised with args: {0}", e.Value);
//            ev.Raise();
//        }
//    }
//}
