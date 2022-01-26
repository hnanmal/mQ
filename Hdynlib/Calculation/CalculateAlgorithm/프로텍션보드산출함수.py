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

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from itertools import chain

allFdns = collector1.OfCategory(BuiltInCategory.OST_StructuralFoundation).WhereElementIsNotElementType().ToElements()
allCols = collector2.OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
allBeams = collector3.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
allFloors = collector4.OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
allIsoFdns = [i.ToDSType(False) for i in allFdns if "Footing-" in i.Name]
allIsoFdnsGeo = [i.Geometry()[0] for i in allIsoFdns]
allPeds = [i.ToDSType(False) for i in allCols if "UG" in i.Name]
allPedsGeo = [i.Geometry()[0] for i in allPeds]
allTGs = [i.ToDSType(False) for i in allBeams if "TG" in i.Name]
allTGsGeo = [i.Geometry()[0] for i in allTGs]
allSOGs = [i.ToDSType(False) for i in allFdns if "SOG" in i.Name and "GS" in i.Name]
allSOGsGeo = [i.Geometry()[0] for i in allSOGs]

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

refFunc = IN[0]
tag = IN[1]
input = IN[2]

# Place your code below this line

def 프로텍션보드산출함수(input):
    
    if "CL" in input.Name:
        calcTargetNum = 1
        inputGeo = input.Geometry()[0]
        표면들 = inputGeo.Explode()
        측면들 = [i for i in 표면들 if round(i.NormalAtParameter(0.5,0.5).Z,2)==0]
        target = 측면들
        targetGeo = target
        targetValue = sum([i.Area for i in target])/calcTargetNum/1000000
        
    else:
        calcTargetNum = 1
        inputGeo = input.Geometry()[0]
        표면들 = inputGeo.Explode()
        기초상부면 = [i for i in 표면들 if round(i.NormalAtParameter(0.5,0.5).Z,2) == 1][0]
        기초측면들 = [i for i in 표면들 if round(i.NormalAtParameter(0.5,0.5).Z,2)==0]
        _접촉페데스탈 = [i for i in allPedsGeo if i.DoesIntersect(inputGeo)]
        접촉페데스탈 = Solid.ByUnion(_접촉페데스탈)
        상부면_공제 = 기초상부면.SubtractFrom(접촉페데스탈)[0]
        target = 기초측면들 + [상부면_공제]
        targetGeo = target
        targetValue = sum([i.Area for i in target])/calcTargetNum/1000000
    
        #return target
    return (targetGeo, targetValue, "M2")

# Assign your output to the OUT variable.
#OUT = 프로텍션보드산출함수(input)
OUT = (프로텍션보드산출함수,tag[0],tag[1],["M2"])