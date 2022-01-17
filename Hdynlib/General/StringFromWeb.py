# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
import urllib.request

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
inputURL = ""
ref = IN[0]

# Place your code below this line
req = urllib.request
data = req.urlopen(inputURL)

result = data.read().decode("utf-8")

# Assign your output to the OUT variable.
OUT = [result,ref]