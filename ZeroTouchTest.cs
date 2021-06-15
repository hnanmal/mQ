using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Autodesk.DesignScript.Runtime;
using Autodesk.DesignScript.Interfaces;
using Autodesk.DesignScript.Geometry;

namespace mQ
{
    public class ZeroTouchTest
    {
        private double _x;
        private double _y;
        private double _z;

        internal ZeroTouchTest(double x, double y, double z)
        {
            _x = x;
            _y = y;
            _z = z;
        }
        public static Line ByTwoDoubles(double x = 0, double y = 0, double z = 0)
        {
            Point p1 = Point.ByCoordinates(x, y, z);
            Point p2 = Point.ByCoordinates(x + 10, y + 10, z + 10);
            Line line = Line.ByStartPointEndPoint(p1, p2);
            p1.Dispose();
            p2.Dispose();
            return line;
        }
        public static Point GetMidPoint(Line InputLine)
        {
            Point MidPoint;
            MidPoint = InputLine.PointAtParameter(0.5);
            return MidPoint;
        }
    }
}
