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
        public static List<Revit.Elements.Element> GetAllWalls()
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
        public static List<Revit.Elements.Element> GetAllStrColumns()
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var ElementCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_StructuralColumns);

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

            var StrColumns = ElementCollector.WherePasses(CategoryFilter).WhereElementIsNotElementType().Cast<Autodesk.Revit.DB.Element>();

            foreach (var i in StrColumns)
            {
                OutList.Add(i.ToDSType(true));
            }

            return OutList; //정상동작하지만, 노드가 꺼내져 있는상태에서 레빗 모델링이 추가되거나 삭제되면 자동실행 모드라도 즉시 반영되지 않는 문제가 있음
        }
        public static List<Revit.Elements.Element> GetAllStrFoundations()
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var ElementCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_StructuralFoundation);

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

            var StrFoundations = ElementCollector.WherePasses(CategoryFilter).WhereElementIsNotElementType().Cast<Autodesk.Revit.DB.Element>();

            foreach (var i in StrFoundations)
            {
                OutList.Add(i.ToDSType(true));
            }

            return OutList;
        }
    }
}
