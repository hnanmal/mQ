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
wholeExcavationBln = IN[2]
기층thk = IN[3]
bttmOffset = IN[4]
버림thk = IN[5]



# Place your code below this line

def 기층물량산출함수(input):
    targets = []
    
    if wholeExcavationBln:
        calcTargetNum = len(allIsoFdns)
        exca_solid = refFunc(input)[0]
        srfs_exca_blw = [i for i in exca_solid.Explode() if round(i.NormalAtParameter(0.5,0.5).Z)==-1]
        

        target = srfs_exca_blw[0].Translate(0,0,-기층thk)
        pass

    else:
        calcTargetNum = 1
        exca_solid = refFunc(input)[0]
        srfs_exca_blw = [i for i in exca_solid.Explode() if round(i.NormalAtParameter(0.5,0.5).Z)==-1]

        target = srfs_exca_blw[0].Translate(0,0,-기층thk)


    return (target, sum([i.Area for i in [target]])/calcTargetNum/1000000, "M2")

# Assign your output to the OUT variable.
#OUT = getBackfillTarget(input)
OUT = (기층물량산출함수,["Footing-Rectangular"],["Base Course"],["M2"])