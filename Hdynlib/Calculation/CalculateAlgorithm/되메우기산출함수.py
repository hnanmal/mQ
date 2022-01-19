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
allTGs = [i.ToDSType(False) for i in allBeams if "UG" in i.Name] #[i.ToDSType(False) for i in allBeams if "TG" in i.Name]
allTGsGeo = list(chain(*[i.Geometry() for i in allTGs]))
allSOGs = [i.ToDSType(False) for i in allFdns if "SOG" in i.Name and "GS" in i.Name]
allSOGsGeo = [i.Geometry()[0] for i in allSOGs]

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
refFunc = IN[0][0]
input = IN[1]
wholeExcavationBln = IN[2]
bttmOffset = IN[3]
버림thk = IN[4]
slopeExcav = IN[5]


# Place your code below this line

def 되메우기산출함수(input):
    targets = []
    
    if wholeExcavationBln:
        calcTargetNum = len(allIsoFdns)
        exca_solid = refFunc(input)[0]
        fdn_solid = list(chain(*[i.Geometry() for i in allIsoFdns]))
        _diff_target = fdn_solid + allPedsGeo + allTGsGeo + allSOGsGeo
        diff_target = Solid.ByUnion(_diff_target)

        target = exca_solid.Difference(diff_target)
        

    else:
        calcTargetNum = 1
        exca_solid = refFunc(input)[0]
        fdn_solid = input.Geometry()[0]
        _joinedPeds = [i for i in allPedsGeo if i.DoesIntersect(exca_solid)]
        _joinedTGs = [i for i in allTGsGeo if i.DoesIntersect(exca_solid)]
        _joinedSOGs = [i for i in allSOGsGeo if i.DoesIntersect(exca_solid)]
        _diff_target = [fdn_solid] + _joinedPeds + _joinedTGs + _joinedSOGs
        diff_target = Solid.ByUnion(_diff_target)
        
        target = exca_solid.Difference(diff_target)

    return (target, sum([i.Volume for i in [target]])/calcTargetNum/1000000000, "M3")

# Assign your output to the OUT variable.
#OUT = getBackfillTarget(input)
OUT = (되메우기산출함수,["Footing-Rectangular"],["Backfill"],["M3"])