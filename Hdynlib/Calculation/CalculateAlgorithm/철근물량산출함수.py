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

allFdns = collector1.OfCategory(BuiltInCategory.OST_StructuralFoundation).WhereElementIsNotElementType().ToElements()
allCols = collector2.OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
allBeams = collector3.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
allFloors = collector4.OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
_allEdges = collector5.OfCategory(BuiltInCategory.OST_EdgeSlab).WhereElementIsNotElementType().ToElements()
allIsoFdns = [i.ToDSType(False) for i in allFdns if "Footing-" in i.Name]
allPeds = [i.ToDSType(False) for i in allCols if "UG" in i.Name]
allPedsGeo = [i.Geometry()[0] for i in allPeds]
allTGs = [i.ToDSType(False) for i in allBeams if "TG" in i.Name]
allTGsGeo = [i.Geometry()[0] for i in allTGs]
allSOGs = [i.ToDSType(False) for i in allFdns if "SOG" in i.Name and "GS" in i.Name]
allSOGsGeo = [i.Geometry()[0] for i in allSOGs]
allEdges = [i.ToDSType(False) for i in _allEdges]
allEdgesGeo = [i.Geometry()[0] for i in allEdges]
allFdnAndHaunch = [i.ToDSType(False) for i in allFdns+_allEdges]
allFdnAndHaunchGeo = list(chain(*[i.Geometry() for i in allFdnAndHaunch]))
#allFdnAndHaunchGeo = [i.Geometry()[0] for i in allFdnAndHaunch]
# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

refFunc = IN[0]
tag = IN[1]
input = IN[2]

독립기초철근비 = IN[3]
슬라브철근비 = IN[4]
패드철근비 = IN[5]
매스콘크리트철근비 = IN[6]

# Place your code below this line
def 철근물량산출함수(input):
    콘크리트물량산출함수 = refFunc[0]
    if "Footing-Rectangular" in input.Name:
        ratio = 독립기초철근비
        
        target = 콘크리트물량산출함수(input)[0]
        targetGeo = "형상정보 미제공"
        targetValue = target.Volume*ratio/1000000000
    
    elif "SOG" in input.Name or "SL" in input.Name:
        ratio = 슬라브철근비
        
        target = 콘크리트물량산출함수(input)[0]
        targetGeo = "형상정보 미제공"
        targetValue = target.Volume*ratio/1000000000
        
    elif "PAD" in input.Name or "EF" in input.Name:
        ratio = 패드철근비
        
        target = 콘크리트물량산출함수(input)[0]
        targetGeo = "형상정보 미제공"
        targetValue = target.Volume*ratio/1000000000
        
    elif "MASS" in input.Name or "MAT" in input.Name:
        ratio = 매스콘크리트철근비
        
        target = 콘크리트물량산출함수(input)[0]
        targetGeo = "형상정보 미제공"
        targetValue = target.Volume*ratio/1000000000

    else:
        ratio = 패드철근비
        
        target = 콘크리트물량산출함수(input)[0]
        targetGeo = "형상정보 미제공"
        targetValue = target.Volume*ratio/1000000000
    
    return (targetGeo, targetValue, "TON")

# Assign your output to the OUT variable.
OUT = (철근물량산출함수,tag[0],tag[1],["TON"])