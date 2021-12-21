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

# Place your code below this line

class RoomInfo:
    def __init__(self, room, inputRooms):
        name = room.GetParameterValueByName("Name")
        self.name = name
        level = room.GetParameterValueByName("Level")
        self.level = level
        department = room.GetParameterValueByName("Department")
        self.department = department
        roomelem = room
        self.roomelem = roomelem
        roomsolid = room.Geometry()[0]
        self.roomsolid = roomsolid
        basefinish = room.GetParameterValueByName("Base Finish").split(',')
        self.basefinish = basefinish
        ceilfinish = room.GetParameterValueByName("Ceiling Finish").split(',')
        self.ceilfinish = ceilfinish
        wallfinish = room.GetParameterValueByName("Wall Finish").split(',')
        self.wallfinish = wallfinish
        floorfinish = room.GetParameterValueByName("Floor Finish").split(',')
        self.floorfinish = floorfinish
        _rooffinish = room.GetParameterValueByName("Exterior Finish").split(',,')[0].split('..')
        rooffinish = list(filter(lambda x: x != "N/A", _rooffinish))
        self.rooffinish = rooffinish
        _extwallfinish = room.GetParameterValueByName("Exterior Finish").split(',,')[1].split('..')
        extwallfinish = list(filter(lambda x: x != "N/A", _extwallfinish))
        self.extwallfinish = extwallfinish
        roomsideface = list(filter(lambda x: x.NormalAtParameter(0.5,0.5).Z != -1 and x.NormalAtParameter(0.5,0.5).Z != 1,roomsolid.Explode()))
        self.roomsideface = roomsideface
        roomupperface = list(filter(lambda x: x.NormalAtParameter(0.5,0.5).Z == 1,roomsolid.Explode()))
        self.roomupperface = roomupperface
        roombottomface = list(filter(lambda x: x.NormalAtParameter(0.5,0.5).Z == -1,roomsolid.Explode()))
        self.roombottomface = roombottomface
        roomperimeter = room.FinishBoundary[0]
        self.roomperimeter = roomperimeter
        adjrooms = list(
                    filter(lambda x: len(roomsolid.Intersect(x.Geometry()[0]))>1,
                        filter(lambda y: y.GetParameterValueByName("Level")==level,
                            filter(lambda z: roomelem.GetParameterValueByName("Number")!=z.GetParameterValueByName("Number"), inputRooms)))
                            )
        self.adjrooms = adjrooms
        
        class AdjRoomInfo:
            def __init__(self, adjroom, roomperimeter, roomsideface):
                adjname = adjroom.Name
                self.adjname = adjname
                adjcurve = PolyCurve.ByJoinedCurves(roomperimeter).Intersect(adjroom.Geometry()[0])
                self.adjcurve = adjcurve
                    
                disc_line = list(map(lambda x: x.TrimByParameter(0.1,0.9), roomperimeter))
                filtered_perimeter = list(filter(lambda x: x.DoesIntersect(adjroom.Geometry()[0]), disc_line))
                self.filtered_perimeter = filtered_perimeter
                adjsurface = list(
                                chain(
                                    *map(lambda y:
                                        filter(lambda x: x.DoesIntersect(y), roomsideface), filtered_perimeter)
                                    )
                                )
                self.adjsurface = adjsurface
        
        surfacedict = {}
        allintsurfaces = []
        for adjroom in adjrooms:
            adjRoomInfo = AdjRoomInfo(adjroom, roomperimeter, roomsideface)
            surfacedict[adjRoomInfo.adjname] = adjRoomInfo.adjsurface
            allintsurfaces.append(adjRoomInfo.adjsurface)
        allintsurfaces = list(chain(*allintsurfaces))
        surfacedict["Int Surfaces"] = allintsurfaces
        extsurfaces = []
        for i in roomsideface:
            tmp1 = []
            for j in allintsurfaces:
                if i.PointAtParameter(0.5,0.5) != j.PointAtParameter(0.5,0.5):
                    tmp1.append(True)
                else:
                    tmp1.append(False)
            if all(tmp1):
                extsurfaces.append(i)
            else:
                pass
        surfacedict["Ext Surfaces"] = extsurfaces
        
        self.surfacedict = surfacedict

# Assign your output to the OUT variable.
OUT = RoomInfo