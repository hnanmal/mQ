# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
collector1 = FilteredElementCollector(doc)
collector2 = FilteredElementCollector(doc)
collector3 = FilteredElementCollector(doc)
collector4 = FilteredElementCollector(doc)
collector5 = FilteredElementCollector(doc)

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from itertools import chain

_allCols = collector2.OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
_allBeams = collector3.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
_allFloors = collector4.OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()

allAGBeams = [i.ToDSType(False) for i in _allBeams if "AG" in i.Name]
#allAGBeamsGeo = [i.Faces for i in allAGBeams]


# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

refFunc = IN[0]
tag = IN[1]
input = IN[2]

# Place your code below this line
def 거푸집산출함수_매스시스템폼(input):
    inputGeo = input.Geometry()[0]
    슬라브표면들 = inputGeo.Explode()
    슬라브측면들 = [i for i in 슬라브표면들 if round(i.NormalAtParameter(0.5,0.5).Z, 2) == 0]
    슬라브측면들면적합 = sum([i.Area for i in 슬라브측면들])

    target = 슬라브측면들
    targetValue = 슬라브측면들면적합/1000000
    
    return (target, targetValue, "M2")

# Assign your output to the OUT variable.
OUT = (거푸집산출함수_매스시스템폼,tag[0],tag[1],["M2"])