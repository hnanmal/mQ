using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Autodesk.Revit;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;
using Autodesk.Revit.ApplicationServices;

namespace House
{
    [Autodesk.Revit.Attributes.Transaction(Autodesk.Revit.Attributes.TransactionMode.Manual)]
    public class Command : IExternalCommand
    {
        public Autodesk.Revit.UI.Result Execute(ExternalCommandData commandData,
            ref string message, Autodesk.Revit.DB.ElementSet elements)
        {
            Application app = commandData.Application.Application;
            Document doc = commandData.Application.ActiveUIDocument.Document;

            //TaskDialog.Show("확인", "준비되었을까나?");

            FilteredElementCollector collector = new FilteredElementCollector(doc);
            ICollection<Element> collection = collector.OfClass(typeof(Level)).ToElements();

            //foreach (Element element in collection) ;
            //{
            //    Level level = element as Level;
            //}

            Level level = collection.First<Element>() as Level;
            //ElementId levelId = level.LevelId;

            double x = 20000;
            double y = 10000;

            x = MmToFeet(x);
            y = MmToFeet(y);

            XYZ pt0 = new XYZ(0, 0, 0);
            XYZ pt1 = new XYZ(x, 0, 0);
            XYZ pt2 = new XYZ(x, y, 0);
            XYZ pt3 = new XYZ(0, y, 0);

            //XYZ[] pts = {pt0, pt1, pt2, pt3};

            Line line0 = Line.CreateBound(pt0, pt1);
            Line line1 = Line.CreateBound(pt1, pt2);
            Line line2 = Line.CreateBound(pt2, pt3);
            Line line3 = Line.CreateBound(pt3, pt0);

            Line[] lines = {line0, line1, line2, line3};

            using (Transaction transaction = new Transaction(doc))
            {
                transaction.Start("Start");

                foreach (Line i in lines) {
                    var j = i.CreateReversed();
                    Wall.Create(doc, j, level.Id, true); 
                }

                transaction.Commit();
            }


            return Autodesk.Revit.UI.Result.Succeeded;
        }

        public double MmToFeet(double mmValue)
        {
            double _mmToFeet = 0.0032808399;
            return mmValue * _mmToFeet;
        }
    }
}
