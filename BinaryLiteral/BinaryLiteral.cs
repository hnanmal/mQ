using System;


class BinaryLiteral
{
    static void Main()
    {
        byte b1 = 0b0010; // 이진수 0010 -> 십진수 2
        byte b2 = 0b1100; // 이진수 1100 -> 십진수 8

        Console.WriteLine($"10진수: {b1}"); // 십진수 2
        Console.WriteLine($"10진수: {b2}"); // 십진수 12
        
        Console.WriteLine($"16진수: {b1:X}"); // 16진수 2
        Console.WriteLine($"16진수: {b2:X}"); // 16진수 C

    }
}

