# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
srfs = IN[0]
offsetValue = -100
# Place your code below this line
def makeOffsetSrfs(srfs, offsetValue):
    periCrvs = map(Surface.PerimeterCurves, srfs)
    offsetPolyCrvs = map(lambda x: Curve.Offset(PolyCurve.ByJoinedCurves(x), offsetValue), periCrvs)
    offsetSrfs = map(Surface.ByPatch, offsetPolyCrvs)
    
    return offsetSrfs

# Assign your output to the OUT variable.
OUT = makeOffsetSrfs(srfs, offsetValue)