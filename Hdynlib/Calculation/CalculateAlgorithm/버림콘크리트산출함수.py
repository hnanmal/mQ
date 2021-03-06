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
collector1 = FilteredElementCollector(doc)
collector2 = FilteredElementCollector(doc)
collector3 = FilteredElementCollector(doc)
collector4 = FilteredElementCollector(doc)
collector5 = FilteredElementCollector(doc)

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

from itertools import chain
from itertools import combinations

allFdns = collector1.OfCategory(BuiltInCategory.OST_StructuralFoundation).WhereElementIsNotElementType().ToElements()
allCols = collector2.OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
allBeams = collector3.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
allFloors = collector4.OfCategory(BuiltInCategory.OST_Floors).WhereElementIsNotElementType().ToElements()
_allEdges = collector5.OfCategory(BuiltInCategory.OST_EdgeSlab).WhereElementIsNotElementType().ToElements()
allIsoFdns = [i.ToDSType(False) for i in allFdns if "Footing-" in i.Name]
allPeds = [i.ToDSType(False) for i in allCols if "UG" in i.Name]
allPedsGeo = [i.Geometry()[0] for i in allPeds]
allTGs = [i.ToDSType(False) for i in allBeams if "TG" in i.Name]
allTGsGeo = [i.Geometry()[0] for i in allTGs]
allSOGs = [i.ToDSType(False) for i in allFdns if "SOG" in i.Name and "GS" in i.Name]
allSOGsGeo = [i.Geometry()[0] for i in allSOGs]
allEdges = [i.ToDSType(False) for i in _allEdges] + [i.ToDSType(False) for i in allFdns if "HAUNCH" in i.Name and "GS" in i.Name]
allEdgesGeo = [i.Geometry()[0] for i in allEdges]
allFdnAndHaunch = [i.ToDSType(False) for i in allFdns+_allEdges]
allFdnAndHaunchGeo = list(chain(*[i.Geometry() for i in allFdnAndHaunch]))
#allFdnAndHaunchGeo = [i.Geometry()[0] for i in allFdnAndHaunch]

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN

refFunc = IN[0]
tag = IN[1]
input = IN[2]

??????thk = IN[3]
??????offset = IN[4]


def getIdxOfMaximum(list):
    result = []
    maxValue = max(list)
    for i in range(len(list)):
        if list[i]==maxValue:
            result.append(i)
    return result

# Place your code below this line

def ??????????????????????????????(input):
    calcTargetNum = 1
    inputGeo = input.Geometry()
    
    if "Footing-Rectangular" in input.Name or "MAT" in input.Name:
        srf_fdn_lean = [i for i in inputGeo[0].Explode() if round(i.NormalAtParameter(0.5,0.5).Z)==-1][0]
        crvs_fdn_lean = srf_fdn_lean.PerimeterCurves()
        crv_fdn_lean = PolyCurve.ByJoinedCurves(crvs_fdn_lean)
        crv_offset = crv_fdn_lean.Offset(??????offset)
        leanSrf = Surface.ByPatch(crv_offset)
        vectorZ = leanSrf.NormalAtParameter(0.5,0.5).Z
        if vectorZ>0:
            target = leanSrf.Thicken(-??????thk, False)
            targetGeo = target
            targetValue = sum([i.Volume for i in [target]])/calcTargetNum/1000000000
        elif vectorZ<0:
            target = leanSrf.Thicken(??????thk, False)
            targetGeo = target
            targetValue = sum([i.Volume for i in [target]])/calcTargetNum/1000000000
        
#    elif "TG" in input.Name:
#        srf_TG_lean = [i for i in inputGeo.Explode() if round(i.NormalAtParameter(0.5,0.5).Z)==-1][0]
#        crvs_TG_lean = srf_TG_lean.PerimeterCurves()
#        len_crvs_TG = [i.Length for i in crvs_TG_lean]
#        idx = getIdxOfMaximum(len_crvs_TG)
#        crvs_long = []
#        for i in idx:
#            crvs_long.append(crvs_TG_lean[i])
#        extdSrfs = []
#        for i in crvs_long:
#            vec = i.NormalAtParameter(0.5)
#            i_tr = i.Translate(??????offset,vec)
#            extdSrfs.append(Surface.ByLoft([i,i_tr]))
#        leanSrf = PolyCurve.ByJoinedCurves([srf_TG_lean]+extdSrfs)
#        vectorZ = leanSrf.NormalAtParameter(0.5,0.5).Z
#        if vectorZ>0:
#            target = leanSrf.Thicken(-??????thk, False)
#        elif vectorZ<0:
#            target = leanSrf.Thicken(??????thk, False)
        
#    elif "SOG" in input.Name:
#        inputGeo = input.Geometry()[0]
#        ??????????????? = inputGeo.Explode()
#        ??????????????? = [i for i in ??????????????? if round(i.NormalAtParameter(0.5,0.5).Z)==-1][0]
#        ???????????? = [i for i in allEdgesGeo if ???????????????.DoesIntersect(i)]
#        ???????????? = [inputGeo] + ????????????
#        ?????????????????? = Solid.ByUnion(????????????)
#        def findBeneathSrf(srfGroup):
#            result = []
#            upperSrfs = [i for i in srfGroup if round(i.NormalAtParameter(0.5,0.5).Z) == 1]
#            headCrvs = []
#            for i in upperSrfs:
#                headCrv = PolyCurve.ByJoinedCurves(i.PerimeterCurves())
#                headCrvs.append(headCrv)
#            for i in srfGroup:
#                tmp=[]
#                for j in headCrvs:
#                    if i.DoesIntersect(j):
#                        tmp.append(False)
#                    else:
#                        tmp.append(True)
#                if all(tmp):
#                    result.append(i)
#            return result
#        leanSrf = findBeneathSrf(??????????????????.Explode())
#        vectorZ = leanSrf.NormalAtParameter(0.5,0.5).Z
#        if vectorZ>0:
#            if len(leanSrf.Surfaces())>1:
#                target = Solid.ByUnion([i.Thicken(-??????thk, False) for i in leanSrf.Surfaces()])
#            else:
#                target = leanSrf.Thicken(-??????thk, False)
#        elif vectorZ<0:
#            if len(leanSrf.Surfaces())>1:
#                target = Solid.ByUnion([i.Thicken(??????thk, False) for i in leanSrf.Surfaces()])
#            else:
#                target = leanSrf.Thicken(??????thk, False)
#        target = leanSrf

#    elif "STOOP" in input.Name or "RAMP" in input.Name or "THICKENED" in input.Name:
    else:
        inputGeo = input.Geometry()[0]
        ??????????????? = inputGeo.Explode()
        ??????????????? = [i for i in ??????????????? if round(i.NormalAtParameter(0.5,0.5).Z)==-1][0]
        ???????????? = [i for i in allEdgesGeo + allFdnAndHaunchGeo if ???????????????.DoesIntersect(i)]
        ???????????? = [inputGeo] + ????????????
        ?????????????????? = Solid.ByUnion(????????????)
        ???????????????????????? = ??????????????????.Translate(0,0,-??????thk)
        ???????????? = ????????????????????????.DifferenceAll([??????????????????])
        
        target = ????????????
        targetGeo = target
        targetValue = sum([i.Volume for i in [target]])/calcTargetNum/1000000000

#    return target
    return (targetGeo, targetValue, "M3")

# Assign your output to the OUT variable.
#OUT = ??????????????????????????????(input)
#OUT = [??????????????????????????????(i) for i in input]
OUT = (??????????????????????????????,tag[0],tag[1],["M3"])