using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


public static class Disposable
{
    public static TResult Using<TDisposable, TResult>
    (
    Func<TDisposable> factory,
    Func<TDisposable, TResult> fn)
    where TDisposable : IDisposable
    {
        using (var disposable = factory())
        {
            return fn(disposable);
        }
    }
}

public static partial class FuntionalExtentions
{
    public static TResult Map<TSource, TResult>(
        this TSource @this,
        Func<TSource, TResult> fn) =>
        fn(@this);
}

class Program
{
    static void Main(string[] args)
    {
        //byte[] buffer;
        //using (var stream = Utility.GeneratePlanetsStream())
        //{
        //    buffer = new byte[stream.Length];
        //    stream.Read(buffer, 0, (int)stream.Length);
        //}

        //var buffer =
        //    Disposable
        //        .Using(
        //        Utility.GeneratePlanetsStream,
        //        stream =>
        //        {
        //            var buff = new byte[stream.Length];
        //            stream.Read(buff, 0, (int)stream.Length);
        //            return buff;
        //        });
        var orderedList =
            Disposable
            .Using(
                Utility.GeneratePlanetsStream,
                stream => new byte[stream.Length]
                    .Tee(b => stream.Read(
                        b, 0, (int)stream.Length)))
                .Map(Encoding.UTF8.GetString)
                .Split(new[] {Environment.NewLine, },
                    StringSplitOptions.RemoveEmptyEntries)
                .Select((s, ix) => Tuple.Create(ix, s))
                .ToDictionary(k => k.Item1, v => v.Item2)
                .Map(options => Utility.GenerateOrderedList(
                    options, "thePlanets", true))
                .Tee(Console.WriteLine);


        //var options = Encoding.UTF8
        //    .GetString(buffer)
        //    .Split(new[] { Environment.NewLine, },
        //        StringSplitOptions.RemoveEmptyEntries)
        //    .Select((s, ix) => Tuple.Create(ix, s))
        //    .ToDictionary(k => k.Item1, v => v.Item2);

        //var orderedList = Utility.GenerateOrderedList(
        //    options, "thePlanets", true);

        //Console.WriteLine(orderedList);
    }
}

public static partial class FuntionalExtentions
{
    public static T Tee<T>(
        this T @this,
        Action<T> action)
    {
        action(@this);
        return @this;
    }
}

public static partial class Utility
{
    public static Stream GeneratePlanetsStream()
    {
        var planets =
            string.Join(
                Environment.NewLine,
                new[]
                {
                    "Mercury", "Venus", "Earth",
                    "Mars", "Jupiter", "Saturn",
                    "Uranus", "Neptune"
                });

        var buffer = Encoding.UTF8.GetBytes(planets);
        var stream = new MemoryStream();
        stream.Write(buffer, 0, buffer.Length);
        stream.Position = 0L;

        return stream;
    }
}

public static partial class StringBuilderExtension
{
    public static StringBuilder AppendFormattedLine(
        this StringBuilder @this,
        string format,
        params object[] args) =>
            @this.AppendFormat(format, args).AppendLine();
}

public static partial class StringBuilderExtension
{
    public static StringBuilder AppendLineWhen(
        this StringBuilder @this,
        Func<bool> predicate,
        string value) =>
            predicate()
            ? @this.AppendLine(value)
            : @this;
}

public static partial class StringBuilderExtension
{
    public static StringBuilder AppendWhen(
        this StringBuilder @this,
        Func<bool> predicate,
        Func<StringBuilder, StringBuilder> fn) =>
        predicate()
        ? fn(@this)
        : @this;
}

public static partial class StringBuilderExtension
{
    public static StringBuilder AppendSequence<T>(
        this StringBuilder @this,
        IEnumerable<T> sequence,
        Func<StringBuilder, T, StringBuilder> fn) =>
            sequence.Aggregate(@this, fn);
}


//public static partial class Utility
//{
//    public static string GenerateOrderedList(
//        IDictionary<int, string> options,
//        string id,
//        bool includeSun)
//    {
//        //var html = new StringBuilder();
//        //html.AppendFormat("<ol id=\"{0}\">", id);
//        //html.AppendLine();

//        //var html =
//        //    new StringBuilder()
//        //    .AppendFormat("<ol id=\"{0}\">", id)
//        //    .AppendLine();

//        //var html =
//        //    new StringBuilder()
//        //    .AppendFormattedLine("<ol id=\"{0}\">", id);

//        //var html =
//        //    new StringBuilder()
//        //    .AppendFormattedLine("<ol id=\"{0}\">", id)
//        //    .AppendLineWhen(() => includeSun, "\t<li>The Sun</li>");

//        var html =
//            new StringBuilder()
//            .AppendFormattedLine("<ol id=\"{0}\">", id)
//            .AppendWhen(
//                () => includeSun,
//                (sb) => sb.AppendLine("\t<li>The Sun</li>"))
//            .AppendSequence(
//                options,
//                (sb, opt) => sb.AppendFormattedLine(
//                    "\t<li value=\"{0}\">{1}</li>",
//                    opt.Key,
//                    opt.Value))
//            .AppendLine("</ol>")
//            .ToString();

//        //if (includeSun)
//        //{
//        //    html.AppendLine("\t<li>The Sun</li>");
//        //}

//        //foreach (var opt in options)
//        //{
//        //    html.AppendFormat("\t<li value=\"{0}\">{1}</li>",
//        //        opt.Key,
//        //        opt.Value);
//        //    html.AppendLine();
//        //}

//        //foreach (var opt in options)
//        //{
//        //    html.AppendFormattedLine("\t<li value=\"{0}\">{1}</li>",
//        //        opt.Key,
//        //        opt.Value);
//        //}

//        //html.AppendLine("</ol>");

//        //return html.ToString();
//    }
//}

public static partial class Utility
{
    public static string GenerateOrderedList(
        IDictionary<int, string> options,
        string id,
        bool includeSun) =>
            new StringBuilder()
                .AppendFormattedLine("<ol id=\"{0}\">", id)
                .AppendWhen(
                    () => includeSun,
                    (sb) => sb.AppendLine("\t<li>The Sun</li>"))
                .AppendSequence(
                    options,
                    (sb, opt) => sb.AppendFormattedLine(
                        "\t<li value=\"{0}\">{1}</li>",
                        opt.Key,
                        opt.Value))
                .AppendLine("</ol>")
                .ToString();
}