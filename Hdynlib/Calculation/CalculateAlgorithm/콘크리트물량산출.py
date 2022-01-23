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
allTGs = [i.ToDSType(False) for i in allBeams if "UG" in i.Name]
allTGsGeo = [i.Geometry()[0] for i in allTGs]
allSOGs = [i.ToDSType(False) for i in allFdns if "SOG" in i.Name and "GS" in i.Name]
allSOGsGeo = [i.Geometry()[0] for i in allSOGs]
allEdges = [i.ToDSType(False) for i in _allEdges] + [i.ToDSType(False) for i in allFdns if "HAUNCH" in i.Name and "GS" in i.Name]
allEdgesGeo = [i.Geometry()[0] for i in allEdges]
allFdnAndHaunch = [i.ToDSType(False) for i in allFdns+_allEdges]
allFdnAndHaunchGeo = list(chain(*[i.Geometry() for i in allFdnAndHaunch]))
#allFdnAndHaunchGeo = [i.Geometry()[0] for i in allFdnAndHaunch]
# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

refFunc = IN[0]
tag = IN[1]
input = IN[2]

# Place your code below this line
def 콘크리트물량산출함수(input):
    if "Footing-Rectangular" in input.Name:
        target = input
        
        return (target.Geometry()[0], target.GetParameterValueByName("Volume"), "M3")
#    elif "FTPS" in input.Name:
#        target = input
#        
#        return (target, 0, "M3")
    else:
        inputGeo = input.Geometry()[0]
        분해요소들 = inputGeo.Explode()
        접촉판별면 = [i for i in 분해요소들 if round(i.NormalAtParameter(0.5,0.5).Z)==-1][0]
        접촉대상 = [i for i in allEdgesGeo if 접촉판별면.DoesIntersect(i)]
        산출대상 = [inputGeo] + 접촉대상
        
        target = Solid.ByUnion(산출대상)
        
        return (target, target.Volume/1000000000, "M3")

    # elif "SOG" in input.Name:
    #     inputGeo = input.Geometry()[0]
    #     간섭판별선 = PolyCurve.ByJoinedCurves([i for i in inputGeo.Explode() if round(i.NormalAtParameter(0.5,0.5).Z)==-1][0].PerimeterCurves()).Offset(-1)
    #     간섭판별면 = 간섭판별선.Patch()
    #     overlaps = [i for i in allEdgesGeo if 간섭판별면.DoesIntersect(i)]+[inputGeo]
    #     unionSolid = Solid.ByUnion(overlaps)
    #     target = unionSolid
        
    #     return (target, target.Volume/1000000000, "M3")

# Assign your output to the OUT variable.
OUT = (콘크리트물량산출함수,tag[0],tag[1],["M3"])