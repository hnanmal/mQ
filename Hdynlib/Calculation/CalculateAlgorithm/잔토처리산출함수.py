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

wholeExcavationBln = IN[3]
ratio = IN[4]


# Place your code below this line

def 잔토처리산출함수(input):
        
    calcTargetNum = 1
    터파기산출함수 = refFunc[0]
    exca_solid = 터파기산출함수(input)[0]
    fdn_solid = input.Geometry()[0]

    target = fdn_solid.Intersect(exca_solid)[0]
    targetGeo = target
    targetValue = sum([i.Volume for i in [target]])*ratio/calcTargetNum/1000000000

    return (targetGeo, targetValue, "M3")

# Assign your output to the OUT variable.
#OUT = getBackfillTarget(input)
OUT = (잔토처리산출함수,tag[0],tag[1],["M3"])