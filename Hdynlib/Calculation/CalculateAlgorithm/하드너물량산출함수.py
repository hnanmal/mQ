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
inputs = IN[0]
# Place your code below this line
def 하드너물량산출함수(input):
    if "PAD" in input.Name:
        pass
    
    else:
        inputGeo = input.Geometry()[0]
        상부면 = [i for i in inputGeo.Explode() if round(i.NormalAtParameter(0.5,0.5).Z)==1][0]
        
        target = 상부면
        
        return (target, target.Area/1000000, "M2")

# Assign your output to the OUT variable.
OUT = (하드너물량산출함수,["GS"],[": Hardener"],["M2"])