# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from itertools import chain

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
inlist = IN[0]
# Place your code below this line
def listFlatten(inlist):
    result = []
    for i in inlist:
        if isinstance(i, list):
            result += (listFlatten(i))
        else:
            result.append(i)
    return result

# Assign your output to the OUT variable.
OUT = listFlatten(inlist)