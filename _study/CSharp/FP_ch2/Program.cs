

public partial class Program
{
    public delegate void SingleStringDelegate(string dataString);

    private static void AssignData(string dataString)
    {
        var globalString = dataString;
    }

    private static void WriteToConsole(string dataText)
    {
        Console.WriteLine(dataText);
    }
}

