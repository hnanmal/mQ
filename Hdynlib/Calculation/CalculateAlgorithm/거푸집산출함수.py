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
collector = FilteredElementCollector(doc)#Autodesk.Revit.DB.FilteredElementCollector(doc)

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from itertools import chain

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

refFunc = IN[0]
tag = IN[1]
input = IN[2]

# Place your code below this line
def 거푸집산출함수(input):
    inputGeo = input.Geometry()[0]
    표면들 = inputGeo.Explode()
    측면들 = [i for i in 표면들 if round(i.NormalAtParameter(0.5,0.5).Z, 2)==0]
    
    target = 측면들
    targetGeo = target
    targetValue = sum([i.Area for i in target])/1000000
    
    return (targetGeo, targetValue, "M2")

# Assign your output to the OUT variable.
OUT = (거푸집산출함수,tag[0],tag[1],["M2"])