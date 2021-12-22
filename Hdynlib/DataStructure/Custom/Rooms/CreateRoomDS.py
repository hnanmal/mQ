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

def Create_RoomDS(room, inputRooms):
    name = room.GetParameterValueByName("Name")
    level = room.GetParameterValueByName("Level")
    department = room.GetParameterValueByName("Department")
    roomelem = room
    roomsolid = room.Geometry()[0]
    basefinish = room.GetParameterValueByName("Base Finish").split(',')
    ceilfinish = room.GetParameterValueByName("Ceiling Finish").split(',')
    wallfinish = room.GetParameterValueByName("Wall Finish").split(',')
    floorfinish = room.GetParameterValueByName("Floor Finish").split(',')
    _rooffinish = room.GetParameterValueByName("Exterior Finish").split(',,')[0].split('..')
    rooffinish = list(filter(lambda x: x != "N/A", _rooffinish))
    _extwallfinish = room.GetParameterValueByName("Exterior Finish").split(',,')[1].split('..')
    extwallfinish = list(filter(lambda x: x != "N/A", _extwallfinish))
    roomsideface = list(filter(lambda x: x.NormalAtParameter(0.5,0.5).Z != -1 and x.NormalAtParameter(0.5,0.5).Z != 1,roomsolid.Explode()))
    roomupperface = list(filter(lambda x: x.NormalAtParameter(0.5,0.5).Z == 1,roomsolid.Explode()))
    roombottomface = list(filter(lambda x: x.NormalAtParameter(0.5,0.5).Z == -1,roomsolid.Explode()))
    roomperimeter = room.FinishBoundary[0]
    adjrooms = list(
                    filter(lambda x: len(roomsolid.Intersect(x.Geometry()[0]))>1,
                        filter(lambda y: y.GetParameterValueByName("Level")==level,
                            filter(lambda z: roomelem.GetParameterValueByName("Number")!=z.GetParameterValueByName("Number"), inputRooms)))
                    )
    def AdjRoomInfo(adjroom, roomperimeter, roomsideface):
        adjname = adjroom.Name
        adjcurve = PolyCurve.ByJoinedCurves(roomperimeter).Intersect(adjroom.Geometry()[0])
        disc_line = list(map(lambda x: x.TrimByParameter(0.1,0.9), roomperimeter))
        filtered_perimeter = list(filter(lambda x: x.DoesIntersect(adjroom.Geometry()[0]), disc_line))
        adjsurface = list(
                        chain(
                            *map(lambda y:
                                filter(lambda x: x.DoesIntersect(y), roomsideface), filtered_perimeter)
                            )
                        )

        result = {
            "adjname": adjname,
            "adjcurve": adjcurve,
            "filtered_perimeter": filtered_perimeter,
            "adjsurface": adjsurface
        }
        return result

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

    result = {
        "name": name,
        "level": level,
        "department": department,
        "roomelem": roomelem,
        "roomsolid": roomsolid,
        "basefinish": basefinish,
        "ceilfinish": ceilfinish,
        "wallfinish": wallfinish,
        "floorfinish": floorfinish,
        "rooffinish": rooffinish,
        "extwallfinish": extwallfinish,
        "roomsideface": roomsideface,
        "roomupperface": roomupperface,
        "roombottomface": roombottomface,
        "roomperimeter": roomperimeter,
        "adjrooms": adjrooms,
        "surfacedict": surfacedict
    }
    return result


result = list(map(lambda x: Create_RoomDS(x, inputRooms), inputRooms))
# Assign your output to the OUT variable.
OUT = result