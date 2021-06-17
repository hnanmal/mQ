using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Autodesk.DesignScript.Runtime;
using Autodesk.DesignScript.Interfaces;
using Autodesk.DesignScript.Geometry;
using Autodesk.Revit.DB;
using Revit.Elements;

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
        public static Autodesk.DesignScript.Geometry.Line ByTwoDoubles(double x = 0, double y = 0, double z = 0)
        {
            Autodesk.DesignScript.Geometry.Point p1 = Autodesk.DesignScript.Geometry.Point.ByCoordinates(x, y, z);
            Autodesk.DesignScript.Geometry.Point p2 = Autodesk.DesignScript.Geometry.Point.ByCoordinates(x + 10, y + 10, z + 10);
            Autodesk.DesignScript.Geometry.Line line = Autodesk.DesignScript.Geometry.Line.ByStartPointEndPoint(p1, p2);
            p1.Dispose();
            p2.Dispose();
            return line;
        }
        public static Autodesk.DesignScript.Geometry.Point MakeQpoint(Double x = 1, Double y = 1, Double z = 1)
        {
            Autodesk.DesignScript.Geometry.Point QPoint = Autodesk.DesignScript.Geometry.Point.ByCoordinates(x, y, z);
            return QPoint;
        }
        public static Autodesk.DesignScript.Geometry.Line MakeQline(Autodesk.DesignScript.Geometry.Point StartPoint, Autodesk.DesignScript.Geometry.Point EndPoint)
        {
            Autodesk.DesignScript.Geometry.Line QLine = Autodesk.DesignScript.Geometry.Line.ByStartPointEndPoint(StartPoint, EndPoint);
            return QLine;
        }
        public static Autodesk.DesignScript.Geometry.Point GetMidPoint(Autodesk.DesignScript.Geometry.Line InputLine)
        {
            Autodesk.DesignScript.Geometry.Point MidPoint;
            MidPoint = InputLine.PointAtParameter(0.5);
            return MidPoint;
        }

        [MultiReturn(new[] {"Line","MiddlePoint"})]
        public static Dictionary<string, object> MakeLine_MidPoint(Autodesk.DesignScript.Geometry.Point StartPoint, Autodesk.DesignScript.Geometry.Point EndPoint)
        {
            Autodesk.DesignScript.Geometry.Line line;
            line = Autodesk.DesignScript.Geometry.Line.ByStartPointEndPoint(StartPoint, EndPoint);

            Autodesk.DesignScript.Geometry.Point MidPoint;
            MidPoint = line.PointAtParameter(0.5);

            Dictionary<string, object> MultiOutPutPort;
            MultiOutPutPort = new Dictionary<string, object>
            {
                {"Line", line },
                {"MiddlePoint", MidPoint }
            };
            return MultiOutPutPort;
        }
    }

    public class Revit_Elements
    {
        private Revit_Elements()
        {
        }
        public static Revit.Elements.Category GetCategory(Revit.Elements.Element InputElement)
        {
            Revit.Elements.Category CatFromInput;
            CatFromInput = InputElement.GetCategory;
            return CatFromInput;
        }

        public static Autodesk.Revit.DB.ElementId GetElementId(Revit.Elements.Element InputElement)
        {
            // Unwrapping part for InputElement
            Autodesk.Revit.DB.Element UnwrappedElements;
            UnwrappedElements = InputElement.InternalElement;
            //

            Autodesk.Revit.DB.ElementId UnwrappedElementId;
            UnwrappedElementId = UnwrappedElements.Id;

            return UnwrappedElementId;
        }
        //public static Autodesk.Revit.DB.CompoundStructureLayer GetWallLayers(Revit.Elements.Element InputWall)
        //{
        //    Autodesk.Revit.DB.Element UnwrappedWall;
        //    UnwrappedWall = InputWall.InternalElement

        //    Revit.Elements.Category.

            
            

        //}
    }
}
