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
def 철골물량산출함수_Medium(input):
    if "Medium" in input.ElementType.GetParameterValueByName("SteelWeight"):
        단위길이당중량 = input.ElementType.GetParameterValueByName("Mass per Unit Length")
        상단높이 = input.GetParameterValueByName("Top Level").Elevation + input.GetParameterValueByName("Top Offset")
        하단높이 = input.GetParameterValueByName("Base Level").Elevation + input.GetParameterValueByName("Base Offset")
#        철골길이 = (상단높이 - 하단높이)/1000
        철골체적 = input.GetParameterValueByName("Volume") #m3
        철골단면적 = input.ElementType.GetParameterValueByName("Section Area")/10000 #cm2 => m2
        철골길이 = 철골체적/철골단면적
        target = input
        targetGeo = target.Geometry()[0]
        targetValue = 단위길이당중량 * 철골길이/1000

    else:
        target = "-!!적용대상이 아님!!-"
        targetGeo = "-!!적용대상이 아님!!-"
        targetValue = "-!!적용대상이 아님!!-"
        
    return (targetGeo, targetValue, "TON")

# Assign your output to the OUT variable.
OUT = (철골물량산출함수_Medium,tag[0],tag[1],["TON"])