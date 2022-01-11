# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
collector = FilteredElementCollector(doc)

allFdns = collector.OfCategory(BuiltInCategory.OST_StructuralFoundation).WhereElementIsNotElementType().ToElements()