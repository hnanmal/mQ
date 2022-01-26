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
def 거푸집산출함수_슬라브(input):
    inputGeo = input.Geometry()[0]
#    접촉대상 = [i for i in allAGBeamsGeo if inputGeo.DoesIntersect(i)]
    접촉대상 = input.GetJoinedElements()
    슬라브면적 = input.GetParameterValueByName("Area")
    슬라브두께 = input.ElementType.GetParameterValueByName("Default Thickness")
    접촉보 = [i for i in 접촉대상 if "BMS" in i.Name]
    
    def 보측면너비산출(슬라브두께, 보):
        보높이 = 보.ElementType.GetParameterValueByName("h")
        보유효높이 = 보높이 - 슬라브두께
        보길이 = 보.GetParameterValueByName("Length")
        보측면면적 = (보유효높이 * 보길이)*2/1000000
        
        return 보측면면적
        
    접촉보측면면적 = sum([보측면너비산출(슬라브두께, i) for i in 접촉보])

    target = 슬라브면적 + 접촉보측면면적
    targetGeo = "형상정보 미제공"
    targetValue = target
    
    return (targetGeo, targetValue, "M2")

# Assign your output to the OUT variable.
OUT = (거푸집산출함수_슬라브,tag[0],tag[1],["M2"])