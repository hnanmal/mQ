# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

input_elems = IN[0]
bln_exceptTarget = IN[1]
targetString = IN[2]

# Place your code below this line
if bln_exceptTarget:
    result = list(map(lambda x: x, input_elems))
else:
    result = list(filter(lambda x: targetString not in x.Name, input_elems))
# Assign your output to the OUT variable.
OUT = result