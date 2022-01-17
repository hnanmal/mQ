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
_inputs = IN[0]
# Place your code below this line
def 거푸집산출함수(input):
    geo = input.Geometry()[0]
    allSrf = geo.Explode()
    sideSrf = [i for i in allSrf if round(i.NormalAtParameter(0.5,0.5).Z)==0]
    
    return (sideSrf, sum([i.Area for i in sideSrf])/1000000, "M2")

# Assign your output to the OUT variable.
OUT = (거푸집산출함수,["Footing-Rectangular"],[": Form"],["M2"])