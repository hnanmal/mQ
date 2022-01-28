# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

from DSCore import Color
clr.AddReference('GeometryColor')
from Modifiers import GeometryColor

import random
from itertools import chain

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
선보기여부 = IN[0]
지정색상 = IN[1]
산출결과세트리스트 = IN[2]
공종코드 = IN[3].split(': ')[0]

def listFlatten(inlist):
    result = []
    for i in inlist:
        if isinstance(i, list):
            result += (listFlatten(i))
        else:
            result.append(i)
    return result

def 공종종류(산출결과세트리스트):
    result = []
    for 산출결과세트 in 산출결과세트리스트:
        for i in 산출결과세트:
            공종 = i[1].split(': ')[0]
            if not 공종 in result:
                result.append(공종)
    return result
    
공종목록 = 공종종류(산출결과세트리스트)

def 색상준비(공종목록):
    log = []
    result = {}
    for i in range(len(공종목록)):
        난수1 = random.randint(0,255)
        난수2 = random.randint(0,255)
        난수3 = random.randint(0,255)
        난수4 = random.randint(0,255)
        색상 = Color.ByARGB(난수1,난수2,난수3,난수4)
        if not 색상 in log:
            log.append(색상)
            result[공종목록[i]] = 색상
    return result
    
색상들 = 색상준비(공종목록)
# Place your code below this line
def 시각화(산출결과세트, 색상들, 공종코드):
    result = []
    for 공종결과 in 산출결과세트:
        tmp1 = []
        target = 공종결과[3][0]
        공종 = 공종결과[1].split(': ')[0]
        색상 = 지정색상
        if 공종 == 공종코드:
            if isinstance(target, Revit.Elements.FamilyInstance):
                visual = GeometryColor.ByGeometryColor(target.Geometry()[0], 색상)[0]
                tmp1.append(visual)
            elif isinstance(target, str):
                pass
            else:
                if not isinstance(target, list):
                    visual = GeometryColor.ByGeometryColor(target, 색상)
                    tmp1.append(visual)
                else:
                    for i in target:
                        tmp1.append(GeometryColor.ByGeometryColor(i, 색상))
            result.append(tmp1)
        else:
            pass
    return result

def 시각화_선보기(산출결과세트, 공종코드):
    result = []
    for 공종결과 in 산출결과세트:
        tmp1 = []
        target = 공종결과[3][0]
        공종 = 공종결과[1].split(': ')[0]
        색상 = 지정색상
        if 공종 == 공종코드:
            if isinstance(target, Revit.Elements.FamilyInstance):
                mass = target.Geometry()[0].Explode()
                lines = list(chain(*listFlatten([i.PerimeterCurves() for i in mass])))
                visual = [GeometryColor.ByGeometryColor(i, 색상) for i in lines]
                tmp1.append(visual)
            elif isinstance(target, str):
                pass
            else:
                if not isinstance(target, list):
                    mass = target.Explode()
                    lines = list(chain(*listFlatten([i.PerimeterCurves() for i in mass])))
                    visual = [GeometryColor.ByGeometryColor(i, 색상) for i in lines]
                    tmp1.append(visual)
                else:
                    for i in target:
                        mass = i.Explode()
                        lines = list(chain(*listFlatten([i.PerimeterCurves() for i in mass])))
                        visual = [GeometryColor.ByGeometryColor(i, 색상) for i in lines]
                        tmp1.append(visual)

            result.append(tmp1)
        else:
            pass
    return result



if 선보기여부:
    result = [시각화_선보기(산출결과세트, 공종코드) for 산출결과세트 in 산출결과세트리스트]
else:
    result = [시각화(산출결과세트, 색상들, 공종코드) for 산출결과세트 in 산출결과세트리스트]
# Assign your output to the OUT variable.
OUT = [list(chain(*result))]