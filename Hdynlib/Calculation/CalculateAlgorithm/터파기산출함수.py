# Load the Python Standard and DesignScript Libraries
import sys
import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument
collector1 = FilteredElementCollector(doc)#Autodesk.Revit.DB.FilteredElementCollector(doc)

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from itertools import chain
from functools import reduce
###################################################################################################
curry = lambda f: lambda a,*args: f(a, *args) if (len(args)) else lambda *args: f(a, *args)

add = curry(lambda a,b: a + b)

filter = curry(filter)
map = curry(map)

def _take(length, iter):
    res = []
    for a in iter:
        res.append(a)
        if len(res) == length:
            return res
take = curry(_take)
reduce = curry(reduce)

go = lambda *args: reduce(lambda a,f: f(a), args) ## 함수도 축약 가능 ##
###########################################

allFdns = collector1.OfCategory(BuiltInCategory.OST_StructuralFoundation).WhereElementIsNotElementType().ToElements()
allIsoFdns = [i.ToDSType(False) for i in allFdns if "Footing-" in i.Name]

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

refFunc = IN[0]
tag = IN[1]
input = IN[2]

wholeExcavationBln = IN[3]
bttmOffset = IN[4]
버림thk = IN[5]
slopeExcav = IN[6]

# Place your code below this line

def 터파기산출함수(input):
    targets = []
    
    if wholeExcavationBln:
        calcTargetNum = len(allIsoFdns)
        fdnsGeo = [i.Geometry()[0] for i in allIsoFdns]
        bdBox_fdn = BoundingBox.ByGeometry(fdnsGeo).ToCuboid()
        srfs = bdBox_fdn.Explode()
        belowSrf = [i for i in srfs if i.NormalAtParameter(0.5,0.5).Z == -1][0]
        def getSrfHeight(srf):
            _crvs = srf.PerimeterCurves()
            heights = [i.StartPoint.Z for i in _crvs]
            height = min(heights)
            return height
        belowSrf_height = getSrfHeight(belowSrf)
        
        def findLeanThk(leanobj):
            if leanobj:
                return leanobj.GetParameterValueByName("thk")
            else:
                return 버림thk
        leanobj = None
        leanthk = findLeanThk(leanobj)
        
        def offsetCrv(crv, offset=300):
            return crv.Offset(offset)
        def correctElev(crv, thk):
            return crv.Translate(0,0,thk)
        _exca_belowbdry = offsetCrv(PolyCurve.ByJoinedCurves(belowSrf.PerimeterCurves()), bttmOffset)
        exca_belowbdry = correctElev(_exca_belowbdry, -버림thk)
        _exca_upperbdry = correctElev(_exca_belowbdry, -belowSrf_height)
        exca_upperbdry = offsetCrv(_exca_upperbdry, -belowSrf_height/slopeExcav)
        target = Solid.ByLoft([exca_belowbdry,exca_upperbdry])
        targetGeo = target
        targetValue = sum([i.Volume for i in [target]])/calcTargetNum/1000000000
        
        
    else:
        calcTargetNum = 1
        def 터파기형상생성기(input, slopeExcav=2, bttmOffset=300, 버림thk=50):
            geo = input.Geometry()[0]
            def 터파기깊이계산기(list):
                res = lambda list: go( list,
                map(lambda a: a.StartPoint.Z)
                )
                return min(res(list))
                
            def 터파기밑테두리들생성기(geo, bttmOffset):
                list = geo.Explode() ## surface들
                res = lambda list: go( list,
                filter(lambda a: round(a.NormalAtParameter(0.5,0.5).Z, 3) == -1),
                map(lambda a: a.PerimeterCurves())
                )
                return res(list)
                
            def 터파기윗테두리생성기(밑테두리, 깊이, slopeExcav):
                윗테두리들 = 밑테두리.Translate(0,0,-깊이)
                윗테두리 = 윗테두리들.Offset(-깊이/slopeExcav)
                return  윗테두리
            
        
            밑테두리들 = list(chain(*터파기밑테두리들생성기(geo, bttmOffset)))
            깊이 = 터파기깊이계산기(밑테두리들)
            밑테두리 = PolyCurve.ByJoinedCurves(밑테두리들)
            윗테두리 = 터파기윗테두리생성기(밑테두리, 깊이, slopeExcav)
            터파기형상 = Solid.ByLoft([밑테두리.Offset(bttmOffset), 윗테두리])
            return 터파기형상
        target = 터파기형상생성기(input, slopeExcav, bttmOffset, 버림thk)
        targetGeo = target
        targetValue = sum([i.Volume for i in [target]])/calcTargetNum/1000000000

    return (targetGeo, targetValue, "M3")

# Assign your output to the OUT variable.
#OUT = fdnsGeo
OUT = (터파기산출함수,tag[0],tag[1],["M3"])