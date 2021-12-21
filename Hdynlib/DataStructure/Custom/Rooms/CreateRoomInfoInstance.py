# Load the Python Standard and DesignScript Libraries
import sys
import clr

clr.AddReference("RevitNodes")
import Revit

from Revit.Elements import *

clr.AddReference("DSCoreNodes")
from DSCore import *

from itertools import *

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
inputLevels = IN[0]
inputRooms = IN[1]
RoomInfo = IN[2]

# Place your code below this line

result = list(map(lambda x: RoomInfo(x, inputRooms), inputRooms))

# Assign your output to the OUT variable.
OUT = [result[0].__dict__, result]