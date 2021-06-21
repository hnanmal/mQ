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
            var ElementCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_Walls);

            var CountedWallsNumber = ElementCollector
                .WherePasses(CategoryFilter)
                .WhereElementIsNotElementType()
                .GetElementCount();

            return CountedWallsNumber;
        }
        public static List<Revit.Elements.Element> GetAllWalls()
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var ElementCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_Walls);

            var Walls = ElementCollector
                .WherePasses(CategoryFilter)
                .WhereElementIsNotElementType()
                .Cast<Autodesk.Revit.DB.Element>();

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

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

            var StrColumns = ElementCollector
                .WherePasses(CategoryFilter)
                .WhereElementIsNotElementType()
                .Cast<Autodesk.Revit.DB.Element>();

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

            foreach (var i in StrColumns)
            {
                OutList.Add(i.ToDSType(true));
            }

            return OutList;
            //정상동작하지만, 노드가 꺼내져 있는상태에서 레빗 모델링이 추가되거나 삭제되면 자동실행 모드라도 즉시 반영되지 않는 문제가 있음
        }
        public static List<Revit.Elements.Element> GetAllStrFoundations()
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var ElementCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_StructuralFoundation);

            var StrFoundations = ElementCollector
                .WherePasses(CategoryFilter)
                .WhereElementIsNotElementType()
                .Cast<Autodesk.Revit.DB.Element>();

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

            foreach (var i in StrFoundations)
            {
                OutList.Add(i.ToDSType(true));
            }

            return OutList;
        }
        public static List<Revit.Elements.Element> GetAllStrFoundationsSOG()
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var ElementCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_StructuralFoundation);

            var StrFoundations = ElementCollector
                .WherePasses(CategoryFilter)
                .WhereElementIsNotElementType()
                .Cast<Autodesk.Revit.DB.Element>();

            var FoundationFloors = from i in StrFoundations
                                   where i.Name.ToString().Contains("SOG")
                                   select i;

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

            foreach (var i in FoundationFloors)
            {
                OutList.Add(i.ToDSType(true));
            }

            return OutList;
        }
        /// <summary>
        /// Structural Foundation Element중 해당 문자열이 패밀리 이름에 포함된 모든 객체를 찾는 노드
        /// </summary>
        /// <param name="familyName">찾고 싶은 문자열 기입</param>
        /// <returns>필터링된 revit element 반환</returns>
        public static List<Revit.Elements.Element> GetAllStrFoundationsByName(string familyName)
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var ElementCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_StructuralFoundation);

            var StrFoundations = ElementCollector
                .WherePasses(CategoryFilter)
                .WhereElementIsNotElementType()
                .Cast<Autodesk.Revit.DB.Element>();

            var FoundationFloors = from e in StrFoundations
                                   where e.Name.ToString().Contains(familyName)
                                   select e;

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

            foreach (var i in FoundationFloors)
            {
                OutList.Add(i.ToDSType(true));
            }

            return OutList;
        }
        public static List<Revit.Elements.Element> GetGroupedAllWallsElementByType()
        {
            Autodesk.Revit.DB.Document doc = DocumentManager.Instance.CurrentDBDocument;
            //setup collector and filter
            var ElementCollector = new FilteredElementCollector(doc);
            var CategoryFilter = new ElementCategoryFilter(BuiltInCategory.OST_Walls);

            var walls = ElementCollector
                .WherePasses(CategoryFilter)
                .WhereElementIsNotElementType()
                .Cast<Autodesk.Revit.DB.Element>()
                .GroupBy(x => x.GetValidTypes());

            var qWalls = from e in walls
                         select e;
            var qqWalls = qWalls
                .SelectMany(group => group)
                .ToList();

            List<Revit.Elements.Element> OutList = new List<Revit.Elements.Element>();

            foreach (var i in qqWalls)
            {
                OutList.Add(i.ToDSType(true));
            }

            return OutList;
        }
    }
}
