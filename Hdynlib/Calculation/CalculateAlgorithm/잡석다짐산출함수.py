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
refFunc = IN[0][0]
input = IN[1]
잡석thk = IN[2]
bttmOffset = IN[3]
버림thk = IN[4]
#slopeExcav = IN[5]


# Place your code below this line

def 잡석다짐산출함수(input):
    버림콘크리트산출함수 = refFunc
    if "Footing-Rectangular" in input.Name:
        calcTargetNum = 1
        solid_lean = 버림콘크리트산출함수(input)[0]
        srf_lean_blw = PolySurface.ByJoinedSurfaces([i for i in solid_lean.Explode() if round(i.NormalAtParameter(0.5,0.5).Z)==-1])
    
        vectorZ = srf_lean_blw.NormalAtParameter(0.5,0.5).Z
        if vectorZ>0:
            target = srf_lean_blw.Thicken(-잡석thk, False)
        elif vectorZ<0:
            target = srf_lean_blw.Thicken(잡석thk, False)
    elif "SOG" in input.Name:
        calcTargetNum = 1
        solid_lean = 버림콘크리트산출함수(input)[0]
        srf_lean_blw = [i for i in solid_lean.Explode() if i.NormalAtParameter(0.5,0.5).Z==-1]
    
        vectorZ = PolySurface.ByJoinedSurfaces(srf_lean_blw).NormalAtParameter(0.5,0.5).Z
        if vectorZ>0:
            target = Solid.ByUnion([i.Thicken(-잡석thk, False) for i in srf_lean_blw])
        elif vectorZ<0:
            target = Solid.ByUnion([i.Thicken(잡석thk, False) for i in srf_lean_blw])
        
#    return target
    return (target, sum([i.Volume for i in [target]])/calcTargetNum/1000000000, "M3")

# Assign your output to the OUT variable.
#OUT = 잡석다짐산출함수(input)
OUT = (잡석다짐산출함수,["Footing-Rectangular","SOG"],["Crushed Stone"],["M3"])