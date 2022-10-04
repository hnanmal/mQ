//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;


//namespace CombineDelegates
//{
//    public partial class Program
//    {
//        static void Main(string[] args)
//        {
//            ReturnValueDelegateInvoke();
//        }
//    }

//    public partial class Program
//    {
//        private delegate void CalculatorDelegate(int a, int b);
//    }

//    public partial class Program
//    {
//        private static void Add(int x, int y)
//        {
//            Console.WriteLine(
//                "{0} + {1} = {2}",
//                x,
//                y,
//                (x + y));
//        }

//        private static void Subtract(int x, int y)
//        {
//            Console.WriteLine(
//                "{0} - {1} = {2}",
//                x,
//                y,
//                x - y);
//        }

//        private static void Multiply(int x, int y)
//        {
//            Console.WriteLine(
//                "{0} * {1} = {2}",
//                x,
//                y,
//                x * y);
//        }

//        private static void Division(int x, int y)
//        {
//            Console.WriteLine(
//                "{0} / {1} = {2}",
//                x,
//                y,
//                x / y);
//        }
//    }

//    public partial class Program
//    {
//        private static void CombineDelegate()
//        {
//            CalculatorDelegate calcMultiples =
//                (CalculatorDelegate)Delegate.Combine(
//                    new CalculatorDelegate[] {
//                        Add,
//                        Subtract,
//                        Multiply,
//                        Division });

//            Delegate[] calcList = calcMultiples.GetInvocationList();
//            Console.WriteLine(
//                "Total delegates in calcMultiples: {0}",
//                calcList.Length);
//            calcMultiples(6, 3);
//        }
//    }

//    public partial class Program
//    {
//        private static void RemoveDelegate()
//        {
//            CalculatorDelegate addDel = Add;
//            CalculatorDelegate subDel = Subtract;
//            CalculatorDelegate mulDel = Multiply;
//            CalculatorDelegate divDel = Division;
//            CalculatorDelegate calcDelegates1 =
//                (CalculatorDelegate)Delegate.Combine(
//                    addDel,
//                    subDel);
//            CalculatorDelegate calcDelegates2 =
//                (CalculatorDelegate)Delegate.Combine(
//                    calcDelegates1,
//                    mulDel);
//            CalculatorDelegate calcDelegates3 =
//                (CalculatorDelegate)Delegate.Combine(
//                    calcDelegates2,
//                    divDel);
//            Console.WriteLine(
//                "Total delegates in calcDelegates3: {0}",
//                calcDelegates3.GetInvocationList().Length);
//            calcDelegates3(6, 3);
//            CalculatorDelegate calcDelegates4 =
//                (CalculatorDelegate)Delegate.Remove(
//                    calcDelegates3,
//                    mulDel);
//            Console.WriteLine(
//                "Total delegates in calcDelegates4: {0}",
//                calcDelegates4.GetInvocationList().Length);
//            calcDelegates4(6, 3);
//        }
//    }

//    public partial class Program
//    {
//        private static void DuplicateEntries()
//        {
//            CalculatorDelegate addDel = Add;
//            CalculatorDelegate subDel = Subtract;
//            CalculatorDelegate MulDel = Multiply;
//            CalculatorDelegate duplicateDelegates1 =
//                (CalculatorDelegate)Delegate.Combine(
//                    addDel,
//                    subDel);
//            CalculatorDelegate duplicateDelegates2 =
//                (CalculatorDelegate)Delegate.Combine(
//                    duplicateDelegates1,
//                    MulDel);
//            CalculatorDelegate duplicateDelegates3 =
//                (CalculatorDelegate)Delegate.Combine(
//                    duplicateDelegates2,
//                    subDel);
//            CalculatorDelegate duplicateDelegates4 =
//                (CalculatorDelegate)Delegate.Combine(
//                    duplicateDelegates3,
//                    addDel);
//            Console.WriteLine(
//                "Total delegates in duplicateDelegates4: {0}",
//                duplicateDelegates4.GetInvocationList().Length);
//            duplicateDelegates4(6, 3);
//        }
//    }

//    public partial class Program
//    {
//        private static void AddSubtractDelegate()
//        {
//            CalculatorDelegate addDel = Add;
//            CalculatorDelegate subDel = Subtract;
//            CalculatorDelegate mulDel = Multiply;
//            CalculatorDelegate divDel = Division;
//            CalculatorDelegate multiDel = addDel + subDel;
//            multiDel += mulDel;
//            multiDel += divDel;
//            Console.WriteLine(
//                "Invoking multiDel delegate (four methods):");
//            multiDel(8, 2);
//            multiDel = multiDel - subDel;
//            multiDel -= mulDel;
//            Console.WriteLine(
//                "Invoking multiDel delegate (after subtraction):");
//            multiDel(8, 2);
//        }
//    }

//    public partial class Program
//    {
//        private delegate T FormulaDelegate<T>(T a, T b);
//    }
//    public partial class Program
//    {
//        private static int AddInt(int x, int y)
//        {
//            return x + y;
//        }
//        private static double AddDouble(double x, double y)
//        {
//            return x + y;
//        }
//    }
//    public partial class Program
//    {
//        private static void GenericDelegateInvoke()
//        {
//            FormulaDelegate<int> intAddition = AddInt;
//            FormulaDelegate<double> doubleAddition = AddDouble;
//            Console.WriteLine("Invoking intAddition(2, 3)");
//            Console.WriteLine(
//                "Result = {0}",
//                intAddition(2, 3));
//            Console.WriteLine("Invoking doubleAddition(2.2, 3.5)");
//            Console.WriteLine(
//                "Result = {0}",
//                doubleAddition(2.2, 3.5));
//        }
//    }
//    public partial class Program
//    {
//        private delegate void AdditionDelegate<T1, T2>(
//            T1 value1, T2 value2);
//    }
//    public partial class Program
//    {
//        private static void AddIntDouble(int x, double y)
//        {
//            Console.WriteLine(
//                "int {0} + double {1} = {2}",
//                x,
//                y,
//                x + y);
//        }
//        private static void AddFloatDouble(float x, double y)
//        {
//            Console.WriteLine(
//                "float {0} + double {1} = {2}",
//                x,
//                y,
//                x + y);
//        }
//    }
//    public partial class Program
//    {
//        private static void VoidDelegateInvoke()
//        {
//            AdditionDelegate<int, double> intDoubleAdd =
//                AddIntDouble;
//            AdditionDelegate<float, double> floatDoubleAdd =
//                AddFloatDouble;
//            Console.WriteLine("Invoking intDoubleAdd delegate");
//            intDoubleAdd(1, 2.5);
//            Console.WriteLine("Invoking floatDoubleAdd delegate");
//            floatDoubleAdd((float)1.2, 4.3);
//        }
//    }
//    public partial class Program
//    {
//        private delegate TResult AddAndConvert<T1, T2, TResult>(
//            T1 digit1, T2 digit2);
//    }
//    public partial class Program
//    {
//        private static float AddIntDoubleConvert(int x, double y)
//        {
//            float result = (float)(x + y);
//            Console.WriteLine(
//                "(int) {0} + (double) {1} = (float) {2}",
//                x,
//                y,
//                result);
//            return result;
//        }
//        private static int AddFloatDoubleConvert(float x, double y)
//        {
//            int result = (int)(x + y);
//            Console.WriteLine(
//                "(float) {0} + (double) {1} = (int) {2}",
//                x,
//                y,
//                result);
//            return result;
//        }
//    }
//    public partial class Program
//    {
//        private static void ReturnValueDelegateInvoke()
//        {
//            AddAndConvert<int, double, float>
//                intDoubleAddConvertToFloat = AddIntDoubleConvert;
//            AddAndConvert<float, double, int>
//                floatDoubleAddConvertToInt = AddFloatDoubleConvert;
//            Console.WriteLine("Invoking intDoubleAddConvertToFloat delegate");
//            float f = intDoubleAddConvertToFloat(5, 3.9);
//            Console.WriteLine("Invoking floatDoubleAddConvertToInt delegate");
//            int i = floatDoubleAddConvertToInt((float)4.3, 2.1);
//        }
//    }
//    public partial class Program
//    {
//        private static void ActionDelegateInvoke()
//        {
//            Action<int, double> intDoubleAddAction =
//                AddIntDouble;
//            Action<float, double> floatDoubleAddAction =
//                AddFloatDouble;
//            Console.WriteLine("Invoking intDoubleAddAction delegate");
//            intDoubleAddAction(1, 2.5);
//            Console.WriteLine("Invoking floatDoubleAddAction delegate");
//            floatDoubleAddAction((float)1.2, 4.3);
//        }
//    }
//    public partial class Program
//    {
//        private static void FuncDelegateInvoke()
//        {
//            Func<int, double, float>
//                intDoubleAddConvertToFloatFunc =
//                    AddIntDoubleConvert;
//            Func<float, double, int>
//                floatDoubleAddConvertToIntFunc =
//                    AddFloatDoubleConvert;
//            Console.WriteLine(
//                "Invoking intDoubleAddConvertToFloatFunc delegate");
//            float f = intDoubleAddConvertToFloatFunc(5, 3.9);
//            Console.WriteLine(
//                "Invoking floatDoubleAddConvertToIntFunc delegate");
//            int i = floatDoubleAddConvertToIntFunc((float)4.3, 2.1);
//        }
//    }
//}