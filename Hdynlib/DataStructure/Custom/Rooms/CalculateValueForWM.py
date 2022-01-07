# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference("RevitNodes")
import Revit

from Revit.Elements import *

clr.AddReference("DSCoreNodes")
from DSCore import *

from itertools import chain

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
inputs = IN[0]
refs = IN[1]
funcs = IN[2]
#masonWall = IN[3]

getTargetforBase = funcs[0]
getTargetforCeil = funcs[1]
getTargetforWall = funcs[2] ##funtion instance
getTargetforFloor = funcs[3]
getTargetforRoof = funcs[4]
getTargetforExtWall = funcs[5] ##funtion instance


walltype = set(map(lambda x: x.Name, refs))
#intWall = set(filter(lambda x: "Interior" in x.Name, refs))
extWall = list(filter(lambda x: "Exterior" in x.Name, refs))
extWallGeo = list(map(lambda y: y.Geometry()[0], filter(lambda x: "Exterior" in x.Name, refs)))
masonWallGeo = list(map(lambda y: y.Geometry()[0], filter(lambda x: "Block" in x.Name or "Brick" in x.Name, refs)))
#nonMasonWall = set(filter(lambda x: not "Block" in x.Name and not "Brick" in x.Name, refs))

def checkValid(value):
    try:
        return value
    except:
        pass

def CalcualteValueForWM(SettingsDS, funcs):

    name = SettingsDS["roomDS"]["name"]
    roomDS = SettingsDS["roomDS"]
    baseWM = SettingsDS["baseWM"]
    ceilWM = SettingsDS["ceilWM"]
    wallWM = SettingsDS["wallWM"]
    floorWM = SettingsDS["floorWM"]
    roofWM = SettingsDS["roofWM"]
    extwallWM = SettingsDS["extwallWM"]
    
    def unitcalc(SettingsDS, WM, finishtype):
        if finishtype == "base": #roomperimeter
            target = getTargetforBase(SettingsDS, WM)
            calcvalue = round(sum(list(map(lambda x: x.Length, target)))/1000,2)
            unit = "M"
        elif finishtype == "ceil":
            target = getTargetforCeil(SettingsDS, WM)
            calcvalue = round(sum(list(map(lambda x: x.Area, target)))/1000000,2)
            unit = "M2"
        elif finishtype == "wall":
            target = getTargetforWall(SettingsDS, WM, masonWallGeo)
            calcvalue = round(sum(list(map(lambda x: x.Area, target)))/1000000,2)
            height = roomDS["roomlimitoffset"]
            unit = "M2"
        elif finishtype == "floor":
            target = getTargetforCeil(SettingsDS, WM)
            calcvalue = round(sum(list(map(lambda x: x.Area, target)))/1000000,2)
            bdlength = sum(list(map(lambda x: x.Length, roomDS["roomperimeter"])))
            unit = "M2"
        elif finishtype == "roof":
            target = getTargetforCeil(SettingsDS, WM)
            calcvalue = round(sum(list(map(lambda x: x.Area, target)))/1000000,2)
            unit = "M2"
        elif finishtype == "extwall":
            target = getTargetforExtWall(SettingsDS, WM, extWall, extWallGeo)
            calcvalue = sum(list(map(lambda x: x.GetParameterValueByName("Area"), target)))
            unit = "M2"
            
        result = []
        result.append(SettingsDS["name"])
        result.append(SettingsDS["roomDS"]["roomelem"].GetParameterValueByName("Department"))
        result.append(finishtype)
#        result.append(WM)
        result.append(WM.split(': ')[0]) ##WM code
        result.append(WM.split(': ')[1]) ##WM description
        result.append(calcvalue)
        result.append(unit)
        if finishtype == "wall":
            result.append(height)
        elif finishtype == "floor":
            result.append(bdlength)
        else:
            pass
            
        return result
    value_base = checkValid(list(map(lambda x: checkValid(unitcalc(SettingsDS, x, "base")), baseWM)))
    value_ceil = checkValid(list(map(lambda x: checkValid(unitcalc(SettingsDS, x, "ceil")), ceilWM)))
    value_wall = checkValid(list(map(lambda x: checkValid(unitcalc(SettingsDS, x, "wall")), wallWM)))
    value_floor = checkValid(list(map(lambda x: checkValid(unitcalc(SettingsDS, x, "floor")), floorWM)))
    value_roof = checkValid(list(map(lambda x: checkValid(unitcalc(SettingsDS, x, "roof")), roofWM)))
    value_extwall = checkValid(list(map(lambda x: checkValid(unitcalc(SettingsDS, x, "extwall")), extwallWM)))
    
    
    return value_base + value_ceil + value_wall + value_floor + value_roof + value_extwall
result = [CalcualteValueForWM(x, funcs) for x in inputs]



# Assign your output to the OUT variable.
OUT = result