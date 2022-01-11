# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
inputs = IN[0]

# Place your code below this line

def solveOverlap(inputs):
    result = []
    for x in range(len(inputs)):
        if x < len(inputs)-1:
            temp = []
            apply = inputs[x]
            for y in range(x,len(inputs)):
                if apply.DoesIntersect(inputs[y]):
                    apply = apply.Split(inputs[y])[0]
                    temp.append(apply)
                else:
                    apply = apply
                    temp.append(apply)
            result.append(temp[-1])
        elif x == len(inputs)-1:
            result.append(inputs[x])

# Assign your output to the OUT variable.
OUT = solveOverlap(inputs)