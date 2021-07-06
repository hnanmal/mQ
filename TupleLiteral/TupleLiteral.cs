using System;

class TupleLiteral
{
    static void Main()
    {
        var fhd = (1920, 1080);
        System.Console.WriteLine($"Full HD: {fhd.Item1} * {fhd.Item2}");

        var uhd = (Width: 3840, Height: 2160);
        System.Console.WriteLine($"4K UHD: {uhd.Width} * {uhd.Height}");

        (ushort Width, ushort Height) hd = (1366, 768);
        System.Console.WriteLine($"HD: {hd.Width} * {hd.Height}");
        System.Console.WriteLine($"형식: {hd.Width.GetType()} * {hd.Height.GetType()}");
    }
}
