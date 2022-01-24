# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
lists = IN[0]
# Place your code below this line

def arrangeDataForExcel(lists):
    result = []
    for elem in lists:
        for wm in elem:
            tmp1 = []
            if "-!!" in str(wm[2]) or "!" in str(wm[3][0]):
                pass
            else:
                tmp1 = []
                tmp1.append(wm[0])
                tmp1.append(wm[1].split(': ')[0])
                tmp1.append(wm[1].split(': ')[1])
                tmp1.append(round(wm[3][1],2))
                tmp1.append(wm[3][2])
            if tmp1:
                result.append(tmp1)
            else:
                pass
    return result

result = arrangeDataForExcel(lists)
# Assign your output to the OUT variable.
OUT = result