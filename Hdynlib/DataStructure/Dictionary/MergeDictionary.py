# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

inputdicts = IN[0]

# Place your code below this line

result = inputdicts[0]
for i in range(len(inputdicts)):
    if i < len(inputdicts)-1:
        result = dict(result, **inputdicts[i+1])
    else:
        pass

# Assign your output to the OUT variable.
OUT = result