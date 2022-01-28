# Load the Python Standard and DesignScript Libraries
import sys
import clr

clr.AddReference('DSCoreNodes')
import DSCore

from DSCore import Color
clr.AddReference('GeometryColor')
from Modifiers import GeometryColor

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from itertools import chain
# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

filepath = IN[0]
다운스케일비율 = IN[1]
픽셀가로 = IN[2]
픽셀세로 = IN[3]

# Place your code below this line
myimage = DSCore.IO.FileSystem.LoadImageFromPath(filepath)
w = myimage.get_Width()
h = myimage.get_Height()
grid_w = int(w/다운스케일비율)
grid_h = int(h/다운스케일비율)
mypixlColors = DSCore.IO.Image.Pixels(myimage, grid_w, grid_h)

gridPts = [Point.ByCoordinates(i,j) for j in range(grid_h) for i in range(grid_w)]

cosyss = [CoordinateSystem.ByOrigin(i) for i in gridPts]
displaypixls = [Rectangle.ByWidthLength(i,픽셀가로,픽셀세로) for i in cosyss]
displaypixls.reverse()

mypixlColors_fl = list(chain(*mypixlColors))
idxs = range(len(displaypixls))
mypixlColors = [GeometryColor.ByGeometryColor(displaypixls[i], mypixlColors_fl[i]) for i in idxs]
# Assign your output to the OUT variable.
OUT = mypixlColors