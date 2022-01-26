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
시스템동바리기준레벨 = IN[3]

# Place your code below this line
def 시스템동바리산출함수(input):
    inputGeo = input.Geometry()[0]
    슬라브표면들 = inputGeo.Explode()
    하부면 = [i for i in 슬라브표면들 if round(i.NormalAtParameter(0.5,0.5).Z, 2) == -1][0]
    접촉대상 = input.GetJoinedElements()
    접촉보 = [i for i in 접촉대상 if "BMS" in i.Name]
    접촉기둥 = [i for i in 접촉대상 if "CLS" in i.Name]
    유효접촉대상 = 접촉보 + 접촉기둥
    유효접촉형상 = Solid.ByUnion([i.Geometry()[0] for i in 유효접촉대상])
    동바리적용면 = 하부면.SubtractFrom(유효접촉형상)[0]
    동바리적용면적 = 동바리적용면.Area
    if 시스템동바리기준레벨 == None:
        기준레벨 = 0
    else:
        기준레벨 = 시스템동바리기준레벨
    동바리높이 = 동바리적용면.PointAtParameter(0.5,0.5).Z - 기준레벨

    target = 동바리적용면
    targetGeo = target
    targetValue = 동바리적용면적*동바리높이/1000000000
    
    return (targetGeo, targetValue, "M2")

# Assign your output to the OUT variable.
OUT = (시스템동바리산출함수,tag[0],tag[1],["M2"])