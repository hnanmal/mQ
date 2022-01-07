# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from itertools import chain

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
inputs = IN[0]
wmdict = IN[1]
    

# Place your code below this line
def main():

    def Create_SettingsDS(roomDS, wmdict):
        def find_WM(finishtype, wmdict):
            result = []
            #result = {}
            if finishtype:
                if finishtype[0] =="":
                    pass
                else:
                    if "WK" in str(finishtype):
                        #result = list(map(lambda x: {"base": wmdict[x]}, finishtype))
                        result = [wmdict[x] for x in finishtype]
                    elif "CL" in str(finishtype):
                        #result = list(map(lambda x: {"ceil": wmdict[x]}, finishtype))
                        result = [wmdict[x] for x in finishtype]
                    elif "IW" in str(finishtype):
                        #result = list(map(lambda x: {"wall": wmdict[x]}, finishtype))
                        result = [wmdict[x] for x in finishtype]
                    elif "FL" in str(finishtype):
                        #result = list(map(lambda x: {"floor": wmdict[x]}, finishtype))
                        result = [wmdict[x] for x in finishtype]
                    elif "RF" in str(finishtype):
                        #result = list(map(lambda x: {"roof": wmdict[x]}, finishtype))
                        result = [wmdict[x] for x in finishtype]
                    elif "EW" in str(finishtype):
                        #result = list(map(lambda x: {"extwall": wmdict[x]}, finishtype))
                        result = [wmdict[x] for x in finishtype]
            else:
                result = []
            return result
            
        name = roomDS["name"]
        roomDS = roomDS
        _baseWM = find_WM(roomDS["basefinish"], wmdict)
        if _baseWM:
            baseWM = _baseWM[0]
        else:
            baseWM = []
        _ceilWM = find_WM(roomDS["ceilfinish"], wmdict)
        if _ceilWM:
            ceilWM = _ceilWM[0]
        else:
            ceilWM = []
        _wallWM = find_WM(roomDS["wallfinish"], wmdict)
        if _wallWM:
            wallWM = _wallWM[0]
        else:
            wallWM = []
        _floorWM = find_WM(roomDS["floorfinish"], wmdict)
        if _floorWM:
            floorWM = _floorWM[0]
        else:
            floorWM = []
        _roofWM = find_WM(roomDS["rooffinish"], wmdict)
        if _roofWM:
            roofWM = _roofWM[0]
        else:
            roofWM = []
        _extwallWM = find_WM(roomDS["extwallfinish"], wmdict)
        if _extwallWM:
            extwallWM = _extwallWM[0]
        else:
            extwallWM = []
        
        result = {
            "name": name,
            "roomDS": roomDS,
            "baseWM": baseWM,
            "ceilWM": ceilWM,
            "wallWM": wallWM,
            "floorWM": floorWM,
            "roofWM": roofWM,
            "extwallWM": extwallWM
        }
        
        return result
        
        
    SettingsDS = [Create_SettingsDS(x, wmdict) for x in inputs]
    
    result = SettingsDS
    return result

# Assign your output to the OUT variable.
OUT = main()