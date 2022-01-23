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

# Place your code below this line

def 파일산출함수(input):
    
    calcTargetNum = 1
    
#    target = input.Geometry()
    value1 = input.ElementType.GetParameterValueByName("Depth")
    value2 = input.ElementType.GetParameterValueByName("최소 내포")
    targetValue = value1 + value2


    return ("형상정보 미제공", targetValue/calcTargetNum/1000, "M")

# Assign your output to the OUT variable.
#OUT = fdnsGeo
OUT = (파일산출함수,tag[0],tag[1],["M"])