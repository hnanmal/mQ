using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Autodesk.DesignScript.Runtime;
using Autodesk.DesignScript.Interfaces;
using Autodesk.DesignScript.Geometry;
using Autodesk.Revit.DB;
using RevitServices.Persistence;
using Autodesk.Revit.ApplicationServices;
using Revit.Elements;
using Autodesk.Revit.UI;

namespace mQ
{
    public class GetElement
    {
        private GetElement()
        {
        }
        public static Revit.Elements.Category GetCategory(Revit.Elements.Element InputElements)
        {
            Revit.Elements.Category CatFromInput;
            CatFromInput = InputElements.GetCategory;
            return CatFromInput;
        }

        public static Autodesk.Revit.DB.ElementId GetElementId(Revit.Elements.Element InputElements)
        {
            // Unwrapping part for InputElement
            Autodesk.Revit.DB.Element UnwrappedElements;
            UnwrappedElements = InputElements.InternalElement;
            //

            Autodesk.Revit.DB.ElementId UnwrappedElementId;
            UnwrappedElementId = UnwrappedElements.Id;

            return UnwrappedElementId;
        }
        public static Autodesk.Revit.DB.ElementId GetWallsId(Revit.Elements.Wall InputWalls)
        {
            Autodesk.Revit.DB.Element UnwrappedWalls;
            UnwrappedWalls = InputWalls.InternalElement;

            Autodesk.Revit.DB.ElementId UnwrappedElementId;
            UnwrappedElementId = UnwrappedWalls.Id;

            return UnwrappedElementId;
        }
        public static Revit.Elements.Element GetWalls(Revit.Elements.Wall InputWalls)
        {
            Autodesk.Revit.DB.Element UnwrappedWalls;
            UnwrappedWalls = InputWalls.InternalElement;

            Revit.Elements.Element Qwall;
            Qwall = UnwrappedWalls.ToDSType(true);

            return Qwall;
        }
        public static int CountAllWalls()
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var WallCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_Walls);
            //collect all mechanical equipment
            var CountedWallsNumber = WallCollector.WherePasses(CategoryFilter).GetElementCount();


            return CountedWallsNumber;
        }
        public static List<Revit.Elements.Element> GetAllWallElements()
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var ElementCollector = new FilteredElementCollector(doc);

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

            var Walls = ElementCollector.OfClass(typeof(Autodesk.Revit.DB.Wall)).ToElements();

            foreach (var i in Walls)
            {
                OutList.Add(i.ToDSType(true));
            }

            return OutList;
        }
    }
}
