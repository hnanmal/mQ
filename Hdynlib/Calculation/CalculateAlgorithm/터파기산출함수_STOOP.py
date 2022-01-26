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
collector1 = FilteredElementCollector(doc)#Autodesk.Revit.DB.FilteredElementCollector(doc)

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

allFdns = collector1.OfCategory(BuiltInCategory.OST_StructuralFoundation).WhereElementIsNotElementType().ToElements()
allIsoFdns = [i.ToDSType(False) for i in allFdns if "Footing-" in i.Name]

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

refFunc = IN[0]
tag = IN[1]
input = IN[2]

wholeExcavationBln = IN[3]
bttmOffset = IN[4]
버림thk = IN[5]
slopeExcav = IN[6]

# Place your code below this line

def 터파기산출함수_STOOP(input):
    
    calcTargetNum = 1
    
    땅묻힘비율 = 0.5
    inputGeo = input.Geometry()[0]
    target = input
    targetGeo = "형상정보 미제공"
    targetValue = inputGeo.Volume*땅묻힘비율/calcTargetNum/1000000000
    
    return (targetGeo, targetValue, "M3")

# Assign your output to the OUT variable.
#OUT = fdnsGeo
OUT = (터파기산출함수_STOOP,tag[0],tag[1],["M3"])