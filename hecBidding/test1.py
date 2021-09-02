# Python 표준 및 DesignScript 라이브러리 로드
from random import randint
import sys
import clr
clr.AddReference('ProtoGeometry')
clr.AddReference('DSCoreNodes')
from DSCore import *
from Autodesk.DesignScript.Geometry import *



def GetXOrderSurfaces(sl):
    ls = []
    for s in sl:
        ls.append(SortByMinX(s))

    ls.sort()

    r = []
    for l in ls:
        r.append(l.val)

    return r

def GetYOrderSurfaces(sl):
    ls = []
    for s in sl:
        ls.append(SortByMinY(s))

    ls.sort()

    r = []
    for l in ls:
        r.append(l.val)

    return r

def GetIndexOfSurface(s, sl):
    for i in range(0, len(sl)):
        if sl[i] == s:
            return i

def GetSurfaceMinX(s):
    a1 = Math.Min(s.PointAtParameter(0,0).X, s.PointAtParameter(0,1).X)
    a2 = Math.Min(s.PointAtParameter(1,0).X, s.PointAtParameter(1,1).X)
    return Math.Min(a1, a2)

def GetSurfaceMaxX(s):
    a1 = Math.Max(s.PointAtParameter(0,0).X, s.PointAtParameter(0,1).X)
    a2 = Math.Max(s.PointAtParameter(1,0).X, s.PointAtParameter(1,1).X)
    return Math.Max(a1, a2)

def GetSurfaceMinY(s):
    a1 = Math.Min(s.PointAtParameter(0,0).Y, s.PointAtParameter(0,1).Y)
    a2 = Math.Min(s.PointAtParameter(1,0).Y, s.PointAtParameter(1,1).Y)
    return Math.Min(a1, a2)

def GetSurfaceMaxY(s):
    a1 = Math.Max(s.PointAtParameter(0,0).Y, s.PointAtParameter(0,1).Y)
    a2 = Math.Max(s.PointAtParameter(1,0).Y, s.PointAtParameter(1,1).Y)
    return Math.Max(a1, a2)


class SortByMinX(object):
     def __init__(self, val):
         self.val = val

     def __lt__(self, other):
         return GetSurfaceMinX(self.val) < GetSurfaceMinX(other.val)

class SortByMinY(object):
     def __init__(self, val):
         self.val = val

     def __lt__(self, other):
         return GetSurfaceMinY(self.val) < GetSurfaceMinY(other.val)


def CreateXCheckerSurface(s):
    minX = GetSurfaceMinX(s)
    minY = GetSurfaceMinY(s)
    maxX = GetSurfaceMaxX(s)
    maxY = GetSurfaceMaxY(s)
    minZ = s.PointAtParameter(0,0).Z
    pl = [
            Point.ByCoordinates(minX - 100000, minY + 0.1, minZ),
            Point.ByCoordinates(minX - 100000, maxY - 0.1, minZ),
            Point.ByCoordinates(minX, maxY - 0.1, minZ),
            Point.ByCoordinates(minX, minY + 0.1, minZ),
        ]

    checkerX = Surface.ByPerimeterPoints(pl)

    return checkerX

def CreateYCheckerSurface(s):
    minX = GetSurfaceMinX(s)
    minY = GetSurfaceMinY(s)
    maxX = GetSurfaceMaxX(s)
    maxY = GetSurfaceMaxY(s)
    minZ = s.PointAtParameter(0,0).Z
    pl = [
            Point.ByCoordinates(minX + 0.1, minY - 100000, minZ),
            Point.ByCoordinates(minX + 0.1, minY, minZ),
            Point.ByCoordinates(maxX - 0.1, minY, minZ),
            Point.ByCoordinates(maxX - 0.1, minY - 100000, minZ),
        ]

    checkerX = Surface.ByPerimeterPoints(pl)

    return checkerX

def GetDistanceXToMove(s, sl):
    checkerX = CreateXCheckerSurface(s)

    cl = []

    noHit = True

    for si in sl:
        if si == s:
            continue
        else:
            if checkerX.DoesIntersect(si) == True:
                noHit = False

                cl.append(si.PointAtParameter(0,0).X)
                cl.append(si.PointAtParameter(0,1).X)
                cl.append(si.PointAtParameter(1,0).X)
                cl.append(si.PointAtParameter(1,1).X)

    if noHit == True:
        return - GetSurfaceMinX(s)
    else:
        cl.sort(reverse=True)
        return cl[0] - GetSurfaceMinX(s)

def GetDistanceYToMove(s, sl):
    checkerY = CreateYCheckerSurface(s)

    cl = []

    noHit = True

    for si in sl:
        if si == s:
            continue
        else:
            if checkerY.DoesIntersect(si) == True:
                noHit = False

                cl.append(si.PointAtParameter(0,0).Y)
                cl.append(si.PointAtParameter(0,1).Y)
                cl.append(si.PointAtParameter(1,0).Y)
                cl.append(si.PointAtParameter(1,1).Y)

    if noHit == True:
        return - GetSurfaceMinY(s)
    else:
        cl.sort(reverse=True)
        return cl[0] - GetSurfaceMinY(s)


def MoveX():
    xOrdered = GetXOrderSurfaces(surfacelist)

    for s in xOrdered:    
        toMoveX = GetDistanceXToMove(s, surfacelist)
        idx = GetIndexOfSurface(s, surfacelist)
        surfacelist[idx] = Geometry.Translate(surfacelist[idx], toMoveX, 0, 0)

def MoveY():
    yOrdered = GetYOrderSurfaces(surfacelist)

    for s in yOrdered:
        toMoveY = GetDistanceYToMove(s, surfacelist)
        idx = GetIndexOfSurface(s, surfacelist)
        surfacelist[idx] = Geometry.Translate(surfacelist[idx], 0, toMoveY, 0)

def SplitX():
    xOrdered = GetXOrderSurfaces(surfacelist)

    offsetX = 0   
    for i in range(0, len(xOrdered)):
        idx = GetIndexOfSurface(xOrdered[i], surfacelist)

        mx = offsetX - GetSurfaceMinX(surfacelist[idx])
        surfacelist[idx] = Geometry.Translate(surfacelist[idx], mx, 0, 0)

        sx = GetSurfaceMaxX(surfacelist[idx]) - GetSurfaceMinX(surfacelist[idx])
        offsetX = offsetX + sx

def SplitY():
    yOrdered = GetYOrderSurfaces(surfacelist)

    offsetY = 0   
    for i in range(0, len(yOrdered)):
        idx = GetIndexOfSurface(yOrdered[i], surfacelist)

        my = offsetY - GetSurfaceMinY(surfacelist[idx])
        surfacelist[idx] = Geometry.Translate(surfacelist[idx], 0, my, 0)

        sy = GetSurfaceMaxY(surfacelist[idx]) - GetSurfaceMinY(surfacelist[idx])
        offsetY = offsetY + sy

def MinofAll():
    allX = []
    allY = []
    for s in surfacelist:
        allX.append(GetSurfaceMinX(s))
        allY.append(GetSurfaceMinY(s))
    allX.sort()
    allY.sort()
    x = 0
    if allX[0] < 0:
        x = -allX[0]
    y = 0
    if allY[0] < 0:
        y = -allY[0]

    return x,y

def MaxofAll():
    allX = []
    allY = []
    for s in surfacelist:
        allX.append(GetSurfaceMaxX(s))
        allY.append(GetSurfaceMaxY(s))
    allX.sort(reverse=True)
    allY.sort(reverse=True)

    return (allX[0], allY[0])

def GetRectMinMaxCornerPoint(center, width, length):
    return (Point.ByCoordinates(center.X - width / 2, center.Y - length /2, center.Z), Point.ByCoordinates(center.X + width / 2, center.Y + length /2, center.Z))


def RepositionInRectOutX(center, width, length):
    (minPos, maxPos) = GetRectMinMaxCornerPoint(center, width, length)
    rectX = maxPos.X - minPos.X
    rectY = maxPos.Y - minPos.Y

    for i in range(0, len(surfacelist)):
        if GetSurfaceMaxX(surfacelist[i]) > rectX:
            (allMaxX, allMaxY) = MaxofAll()
            offsetY = allMaxY - GetSurfaceMinY(surfacelist[i])
            surfacelist[i] = Geometry.Translate(surfacelist[i], 0, offsetY, 0)
            MoveX()
            MoveY()

def RepositionInRectInX(center, width, length):
    (minPos, maxPos) = GetRectMinMaxCornerPoint(center, width, length)
    rectX = maxPos.X - minPos.X
    rectY = maxPos.Y - minPos.Y

    for i in range(0, len(surfacelist)):
        if GetSurfaceMaxX(surfacelist[i]) > rectX:
            offsetY = rectY - GetSurfaceMaxY(surfacelist[i])
            surfacelist[i] = Geometry.Translate(surfacelist[i], 0, offsetY, 0)
            MoveX()
            MoveY()

def RepositionInRectOutY(center, width, length):
    (minPos, maxPos) = GetRectMinMaxCornerPoint(center, width, length)
    rectX = maxPos.X - minPos.X
    rectY = maxPos.Y - minPos.Y

    for i in range(0, len(surfacelist)):
        if GetSurfaceMaxY(surfacelist[i]) > rectY:
            (allMaxX, allMaxY) = MaxofAll()
            offsetX = allMaxX - GetSurfaceMinX(surfacelist[i])
            surfacelist[i] = Geometry.Translate(surfacelist[i], offsetX, 0, 0)
            MoveY()
            MoveX()

def RepositionInRectInY(center, width, length):
    (minPos, maxPos) = GetRectMinMaxCornerPoint(center, width, length)
    rectX = maxPos.X - minPos.X
    rectY = maxPos.Y - minPos.Y

    for i in range(0, len(surfacelist)):
        if GetSurfaceMaxY(surfacelist[i]) > rectY:
            offsetX = rectX - GetSurfaceMaxX(surfacelist[i])
            surfacelist[i] = Geometry.Translate(surfacelist[i], offsetX, 0, 0)
            MoveY()
            MoveX()

def MoveAllTo(ox, oy):
    for i in range(0, len(surfacelist)):
        surfacelist[i] = Geometry.Translate(surfacelist[i], ox, oy, 0)

def CheckOutOfBoundary(center, width, length):
    result = []
    (minPos, maxPos) = GetRectMinMaxCornerPoint(center, width, length)
    rectX = maxPos.X - minPos.X
    rectY = maxPos.Y - minPos.Y

    for i in range(0, len(surfacelist)):
        if GetSurfaceMaxX(surfacelist[i]) > rectX or GetSurfaceMaxY(surfacelist[i]) > rectY:
            result.append(i)
    return result



#def FindBoundaryPoint(crv):
#    x = crv.PointAtParameter(0).X
#    y = crv.PointAtParameter(0).Y
#    
#    return x,y


# 이 노드에 대한 입력값은 IN 변수에 리스트로 저장됩니다.
dataEnteringNode = IN

# 코드를 이 선 아래에 배치

surfaces = IN[0]
cs = IN[1]
width = IN[2]
length = IN[3]
#bdCrv = IN[1]

(boundryMin, boundryMax) = GetRectMinMaxCornerPoint(cs[0].Origin, width[0], length[0])

surfacelist = []
for s in surfaces:
    surfacelist.append(s)

(basX, basY) = MinofAll()
#(basX, basY) = FindBoundaryPoint(bdCrv)
#(basX, basY) = 0, 0

for i in range(0, len(surfacelist)):
    surfacelist[i] = Geometry.Translate(surfacelist[i], basX, basY, 0)

if randint(0, 1) == 0:
    SplitX()
    MoveX()
    MoveY()
    MoveX()
    MoveY()

else:
    SplitY()
    MoveY()
    MoveX()
    MoveY()
    MoveX()

RepositionInRectOutX(cs[0].Origin, width[0], length[0])
RepositionInRectOutY(cs[0].Origin, width[0], length[0])
RepositionInRectInX(cs[0].Origin, width[0], length[0])
RepositionInRectInY(cs[0].Origin, width[0], length[0])

failed = CheckOutOfBoundary(cs[0].Origin, width[0], length[0])

MoveAllTo(boundryMin.X, boundryMin.Y)

# testnum = IN[1]
# xOrdered = GetXOrderSurfaces(surfacelist)

# # for s in xOrdered:    
# toMoveX = GetDistanceXToMove(xOrdered[testnum], surfacelist)
# idx = GetIndexOfSurface(xOrdered[testnum], surfacelist)
# surfacelist[idx] = Geometry.Translate(surfacelist[idx], toMoveX, 0, 0)



# 출력을 OUT 변수에 지정합니다.
OUT = (surfacelist, failed)