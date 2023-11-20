# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
import Autodesk

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
doc = DocumentManager.Instance.CurrentDBDocument

from functools import reduce
from functools import partial

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import Revit

from itertools import chain
from functools import reduce
from copy import deepcopy
import operator
from itertools import groupby
import copy

def make_UnifiedDict(dictsList):
    dicts_AllInOne = {}
    for d in dictsList:
        dict_k_v = d.items()
        for k,v in dict_k_v:
            dicts_AllInOne[k] = v
    return dicts_AllInOne

def find_IsInStr(target, str):
    if target == None or str == None:
        pass
    else:
        res = target in str
        return res

def find_range_by_columnItem(db, col_idx, sep_rule):
    tdb = list(map(lambda x: x[col_idx], db))
    last_idx_tdb = len(tdb)-1
    tdb_enum = enumerate(tdb)
    res = list(filter(lambda x: find_IsInStr(sep_rule, x[1]), tdb_enum))
    endidxs_tmp= list(map(lambda x: x[0]-1,res))
    endidxs_tmp.pop(0)
    endidxs = endidxs_tmp + [last_idx_tdb]
    famTypeNames = list(map(lambda x: x[1],res))
    famTypeNamesIdxs = list(map(lambda x: x[0],res))
    rangeSttIdxs = list(map(lambda x: x[0]+1,res))
    rangeEndIdxs = endidxs
    result = dict(zip(famTypeNames, zip(famTypeNamesIdxs, zip(rangeSttIdxs,rangeEndIdxs))))
    return result

def find_headersAtSheet(sheet):
    headers_sheet = map(lambda x: [x[1].replace("\n",""),x[0]], filter(lambda x: x[1] != None, enumerate(sheet[1])))
    
    return dict(headers_sheet)

def find_rangesAtSheet(sheet, hdrs_withIdx, trgt_hdr, trgt_str):
    return find_range_by_columnItem(sheet, hdrs_withIdx[trgt_hdr], trgt_str)

def get_DataOnRangesAtParamSheet(sheet):
    
    hdrs_withIdx = find_headersAtSheet(sheet)
    rangesATSheet = find_rangesAtSheet(sheet, hdrs_withIdx, "Q'ty Cal Type Tag", "-")
    title_idx = map(lambda x: x[0], rangesATSheet.values())
    calcType_colDatas = list(map(lambda x: x[hdrs_withIdx["Q'ty Cal Type Tag"]], sheet))
    calcTypes = list(map(lambda x: calcType_colDatas[x], title_idx))
    rgs_v = list(map(lambda x: x[1], rangesATSheet.values()))
    rgs_k = list(map(lambda x: x, rangesATSheet.keys()))
    
    hdrs_v = list(hdrs_withIdx.values())
    hdrs_k = list(hdrs_withIdx.keys())
    eff_hdrs_v = hdrs_v[2:]
    eff_hdrs_k = hdrs_k[2:]
    
    datas_allCalType = list(map(lambda x: sheet[x[0]-1:x[1]], rgs_v))
    
    def setDict_OnEachCalType(data_calType):
        paramName_lang = "패밀리 매개변수(from Revit) 영문판" if lang_mode is True else "패밀리 매개변수(from Revit) 한글판"
        calcTypeName = data_calType[0][2]
        data_calType_noneless = list(filter(lambda x: x[hdrs_withIdx["항목"]] != None, data_calType))
#        ## WM row 별 header명 과 짝짓기
        data_withHdrsIdx = list(map(lambda y: list(map(lambda x: y[x], eff_hdrs_v)), data_calType_noneless))
        dict_ = list(map(lambda x: dict(zip(eff_hdrs_k, x)), data_withHdrsIdx))
        dicts_noneless = list(map(lambda y: dict(filter(lambda x: x[1]!=None, y.items())),dict_))
#        ## dict_Cal Type 입력처리
        targetColName = "Q'ty Cal Type Tag"
        dicts_finalNoneless = []
        for d in dicts_noneless:
            d["Q'ty Cal Type Tag"] = calcTypeName
            
            if "입력값" in d.keys():
                d["applyForCalc"] = d["입력값"]
                dicts_finalNoneless.append(d)
            elif paramName_lang in d.keys():
                d["applyForCalc"] = d[paramName_lang]
                dicts_finalNoneless.append(d)
            else:
                pass
        
        return {calcTypeName: dicts_finalNoneless}
        
    return map(setDict_OnEachCalType, datas_allCalType)

def get_SymValDict_PerCalcType(dic):
    def findDictPerCalcType(dicList):
            dic = {}
            for i in dicList:
                dic[i["산출수식 약자"]] = i["applyForCalc"]
            return dic
    
    ks_forDic = list(dic.keys())
    vs_forDic = list(map(findDictPerCalcType, dic.values()))
    res = dict(zip(ks_forDic, vs_forDic))
    return res

def get_DataOnRangesAtCatSheet(catSheet):
    hdrs_withIdx = find_headersAtSheet(catSheet)
    rangesATSheet = find_rangesAtSheet(catSheet, hdrs_withIdx, "Family Type Name", "H_")
    title_idx = map(lambda x: x[0], rangesATSheet.values())
    calcType_colDatas = list(map(lambda x: x[hdrs_withIdx["Q'ty Cal Type Tag"]], catSheet))
    calcTypes = list(map(lambda x: calcType_colDatas[x], title_idx))
    rgs_v = list(map(lambda x: x[1], rangesATSheet.values()))
    rgs_k = list(map(lambda x: x, rangesATSheet.keys()))
    
    hdrs_v = list(hdrs_withIdx.values())
    hdrs_k = list(hdrs_withIdx.keys())
    
    datas_allFamType = list(map(lambda x: list(zip(catSheet[x[0]-1:x[1]], range(x[0]-1,x[1]))), rgs_v))
    
    def setDict_OnEachFamType(data_famType):  ## 최종적으로 산출식 없는 것 걸러내기 추가해야 함
        titleData = list(data_famType).pop(0)[0]
        
        famTypeName = titleData[hdrs_withIdx["Family Type Name"]]
        calcTypeName = titleData[hdrs_withIdx["Q'ty Cal Type Tag"]]
        data_famType_noneless = list(filter(lambda x: x[0][5] != None, data_famType))
        ## WM row 별 header명 과 짝짓기
        data_withHdrsIdx = list(map(lambda y: [list(map(lambda x: y[0][x], hdrs_v)), y[1]], data_famType_noneless))
        hdrs_k.append("rIDX")
        dict_ = list(map(lambda x: dict(zip(hdrs_k, x[0]+[x[1]])), data_withHdrsIdx))
        dicts_noneless = list(map(lambda y: dict(filter(lambda x: x[1]!=None, y.items())),dict_))
        ## dict_gauge, 물량산출식 없는 항목 처리
        dicts_final = []
        needDefault_ColName = "Gauge Code"
        noneRemove_ColName = "Dynamo 물량산출식"
        for d in dicts_noneless:
            d["Family Type Name"] = famTypeName
            
            if calcTypeName == None:
                pass            
            elif noneRemove_ColName in d.keys():
                d["Q'ty Cal Type Tag"] = calcTypeName
                d[needDefault_ColName] = ""
                dicts_final.append(d)

        return dicts_final
        
    dicts_allFamType = list(map(lambda x: setDict_OnEachFamType(list(x)), datas_allFamType))
    ds_famTypesAtCatSheet = dict(zip(rgs_k, dicts_allFamType))
    ds_famTypesAtCatSheet_effCalcType = dict(filter(lambda x: all(list(map(lambda i: "Q'ty Cal Type Tag" in i, x[1]))), list(ds_famTypesAtCatSheet.items())))
    ds_famTypesAtCatSheet_noneless = dict(filter(lambda x: len(list(x[1]))!=0, list(ds_famTypesAtCatSheet_effCalcType.items())))
    
    return  ds_famTypesAtCatSheet_noneless

def make_AIOdic(allCatSheets):

    dataOnRanges_allCat = list(map(get_DataOnRangesAtCatSheet, allCatSheets))
    dataOnRanges_allCat_WithCatNames = list(zip(allCatSheetsNames, dataOnRanges_allCat))
    
    AIOdic = {}
    for d in dataOnRanges_allCat_WithCatNames:
        catName = d[0]
        dict_k_v = d[1].items()
        for k,v in dict_k_v:
            for wm in v:
                wm["SheetName"] = catName
            AIOdic[k] = v
    return AIOdic

def matchWith_paramDic(catSheetDic, paramSheetDic):
    headers = list(catSheetDic.values())[0][0].keys()
    wmspec_headers = list(filter(lambda x: "Work C" in x or "Spec" in x, headers))
    res = {}
    for famType,diclist in catSheetDic.items():
        new_diclist = []
        for d in diclist:
            new_d = {}
            keys = d.keys()
            keys_new = set(keys) - set(wmspec_headers)
            calcType = d["Q'ty Cal Type Tag"]
            new_d["Sym_Val Dict"] = paramSheetDic[calcType]
            new_d["wmSpecs"] = list(map(lambda x: d[x],wmspec_headers))
            for spec in keys_new:
                new_d[spec] = d[spec]
            new_diclist.append(new_d)
        
        res[famType] = new_diclist
        
    return res

def filterEffRevitElems(allRevitElemsFlatten, elemDicts):
    allFamTypesInExcel = elemDicts.keys()
    res = list(filter(lambda x: x.GetParameterValueByName("Type").GetParameterValueByName("Type Name") in allFamTypesInExcel, allRevitElemsFlatten))
    return res

def matchWith_Elem_Dict(famlist_dic,revitElems):
    res = []
    for i in revitElems:
        tmp = {}
        famTypeName = i.GetParameterValueByName("Type").GetParameterValueByName("Type Name")
        tmp["Elem"] = i
        tmp["wms"] = famlist_dic[famTypeName]
        
        res.append(tmp)
    return res

def update_sym_valDict(elemDicts):
    
    def make_newElemDict(elemDict):
        new_elemDict = {}
        elemDict_keys = elemDict.keys()
        elemDict_vals = list(elemDict.values())
        elemDict_items = list(elemDict.items())
        
        def get_newWMsWithcalculatedSymValSet(elemDict):
            elem = elemDict["Elem"]
            wms = elemDict["wms"]
            new_wms = []
            
            for wm in wms:
                new_wm ={}
                sym_valDict = wm["Sym_Val Dict"]
                #wm_keys = wm.Keys
                wm_keys = wm.keys()
                #wm_vals = wm.Values
                wm_vals = wm.values()
                wm_items = list(zip(wm_keys,wm_vals))
                
                #sv_keys = sym_valDict.Keys
                sv_keys = sym_valDict.keys()
                #sv_vals = sym_valDict.Values
                sv_vals = sym_valDict.values()
                sv_items = list(zip(sv_keys, sv_vals))
                sv_Dict = {}
                for k,v in sv_items:
                    if isinstance(v, str): ### 수정 필요 (굳이 v의 타입검사하는 이유?)
                        if v == "Level":
                            sv_Dict[k] = round(elem.GetParameterValueByName("Elevation at Bottom"),2)
                        elif elem.GetParameterValueByName(v):
                            sv_Dict[k] = elem.GetParameterValueByName(v)
                        elif elem.GetParameterValueByName("Type").GetParameterValueByName(v):
                            sv_Dict[k] = elem.GetParameterValueByName("Type").GetParameterValueByName(v)
                        else:
                            sv_Dict[k] = v
                    else:
                        sv_Dict[k] = v
                for k,v in wm_items:
                    if k == "Sym_Val Dict":
                        new_wm[k] = sv_Dict
                    else:
                        new_wm[k] = v
                new_wms.append(new_wm)
            return new_wms
                
                
        for k,v in elemDict_items:
            if k == "wms":
                new_elemDict[k] = get_newWMsWithcalculatedSymValSet(elemDict)
            else:
                new_elemDict[k] = v
                        
        return new_elemDict
    res = list(map(make_newElemDict, elemDicts))
    
    return res

def get_allElems(doc):
    target_bic = Autodesk.Revit.DB.BuiltInCategory.OST_Levels
    
    def getElems(x):
        collector = FilteredElementCollector(doc)
        res = collector.OfCategory(x).WhereElementIsNotElementType().ToElements()
        return res

    res = getElems(target_bic)

    return res

def getGroundLevelElem(allLevelElems):
    res = list(filter(lambda x: "G.L" in x.Name, allLevelElems))[0]
    return res

def makeExcaShape(elem, sym_valDict, FL_GL_gap):
    def findBtmCrv(geo, sym_valDict): ##btmOffset = d1 + d2
        offSetDist = sym_valDict["D1"] + sym_valDict["D2"]
        h = abs(sym_valDict["C1"] + sym_valDict["C2"] + sym_valDict["C3"])
        bdBox_fdn = BoundingBox.ByGeometry(geo).ToCuboid() ## 형상의 자그마한 요철 무시
        srfs = bdBox_fdn.Explode() ## surface들
        btmSrf = PolySurface.ByJoinedSurfaces(list(filter(lambda x: round(x.NormalAtParameter(0.5,0.5).Z, 3) == -1, srfs)))
        btmCrvs = btmSrf.PerimeterCurves()
        btmPolCrv = PolyCurve.ByJoinedCurves(btmCrvs)
        offseted_btmPolCrv = btmPolCrv.Offset(offSetDist)
        #h_modified_btmPolCrv = offseted_btmPolCrv.Translate(0,0,-h-Survey_Base_zGap)
        h_modified_btmPolCrv = offseted_btmPolCrv.Translate(0,0,-h)
        return h_modified_btmPolCrv
    
    def findUprCrv(_btmPolCrv, sym_valDict):
        btmCrvZ = _btmPolCrv.StartPoint.Z
        #test = (sym_valDict["C1"] + sym_valDict["C2"] + sym_valDict["C3"])

        H = abs(round(btmCrvZ,2))
        G = sym_valDict["G"]
        offSetDist = (G * H)
        
        #uprPolCrv = _btmPolCrv.Translate(0,0,H).Offset(offSetDist)
        uprPolCrv = _btmPolCrv.Translate(0,0,H + Survey_Base_zGap -FL_GL_gap).Offset(offSetDist)
        #uprCrvZ = uprPolCrv.StartPoint.Z
        return uprPolCrv


    fdnsGeo = elem.Geometry()[0]
    btmPolCrv = findBtmCrv(fdnsGeo, sym_valDict)
    uprPolCrv = findUprCrv(btmPolCrv, sym_valDict)
    res = Solid.ByLoft([btmPolCrv,uprPolCrv])#.Translate(0,0, Survey_Base_zGap - FL_GL_gap)
    return res

def makeExcaShape_whole(elemDicts, paramSheetDic, wholeExca_CalcType, FL_GL_gap):
    sym_valDict = paramSheetDic[wholeExca_CalcType]
    def findBtmCrv(geo, sym_valDict): ##btmOffset = d1 + d2
        offSetDist = sym_valDict["D1"] + sym_valDict["D2"]
        
        h = abs(sym_valDict["C1"] + sym_valDict["C2"] + sym_valDict["C3"])
        bdBox_fdn = BoundingBox.ByGeometry(geo).ToCuboid() ## 형상의 자그마한 요철 무시
        srfs = bdBox_fdn.Explode() ## surface들
        btmSrf = PolySurface.ByJoinedSurfaces(list(filter(lambda x: round(x.NormalAtParameter(0.5,0.5).Z, 3) == -1, srfs)))
        btmCrvs = btmSrf.PerimeterCurves()
        btmPolCrv = PolyCurve.ByJoinedCurves(btmCrvs)
        offseted_btmPolCrv = btmPolCrv.Offset(offSetDist)
        h_modified_btmPolCrv = offseted_btmPolCrv.Translate(0,0,-h)
        return h_modified_btmPolCrv
    
    def findUprCrv(_btmPolCrv, sym_valDict):
        btmCrvZ = _btmPolCrv.StartPoint.Z
        test = (sym_valDict["C1"] + sym_valDict["C2"] + sym_valDict["C3"])
        
        H = abs(round(btmCrvZ,2))
        G = sym_valDict["G"]
        offSetDist = (G * H)
        
        uprPolCrv = _btmPolCrv.Translate(0,0,H + Survey_Base_zGap -FL_GL_gap).Offset(offSetDist)
        uprCrvZ = uprPolCrv.StartPoint.Z
        return uprPolCrv
        
    def findExcaShapeByColFnds():
        all_ColFdnElems = list(map(lambda x: x["Elem"].Geometry()[0], filter(lambda dic: "ACF_W" in dic["wms"][0]["Family Type Name"], elemDicts)))
        resBdBox = BoundingBox.ByGeometry(all_ColFdnElems).ToCuboid()
        
        btmPolCrv = findBtmCrv(resBdBox, sym_valDict)
        uprPolCrv = findUprCrv(btmPolCrv, sym_valDict)
        res = Solid.ByLoft([btmPolCrv,uprPolCrv])#.Translate(0,0,FL_GL_gap)
        
        return res

    def findExcaShapeByMass():
        all_MassElems = list(map(lambda x: x["Elem"].Geometry()[0], filter(lambda dic: "ACE_Mass" in dic["wms"][0]["Family Type Name"], elemDicts)))
        if all_MassElems:
            resBdBox = BoundingBox.ByGeometry(all_MassElems).ToCuboid()
            btmPolCrv = findBtmCrv(resBdBox, sym_valDict)
            uprPolCrv = findUprCrv(btmPolCrv, sym_valDict)
            res = Solid.ByLoft([btmPolCrv,uprPolCrv])#.Translate(0,0,FL_GL_gap)
        else:
            res = []
        
        return res

    def findExcaShapeByPit():
        all_PitElems = list(map(lambda x: x["Elem"].Geometry()[0], filter(lambda dic: "ACP_Pit Slab" in dic["wms"][0]["Family Type Name"], elemDicts)))
        if all_PitElems:
            resBdBox = BoundingBox.ByGeometry(all_PitElems).ToCuboid()
            
            btmPolCrv = findBtmCrv(resBdBox, sym_valDict)
            uprPolCrv = findUprCrv(btmPolCrv, sym_valDict)
            res = Solid.ByLoft([btmPolCrv,uprPolCrv])#.Translate(0,0,FL_GL_gap)
        else:
            res = []
        return res
        
    finalTarget = list(filter(lambda x: x!=[] ,[findExcaShapeByColFnds(),findExcaShapeByMass(),findExcaShapeByPit()]))
    res = Solid.ByUnion(finalTarget)
    
    return res

def makeDispShape_whole(elemDicts, paramSheetDic, FL_GL_gap):
    total_ExcaGeo = makeExcaShape_whole(elemDicts, paramSheetDic, wholeExca_CalcType, FL_GL_gap)
    allGeo_UG_union = Solid.ByUnion(find_allGeo_UG_elems(elemDicts))
    dispShape = allGeo_UG_union.Split(total_ExcaGeo)[-1]
    backFillShape = total_ExcaGeo.Split(allGeo_UG_union)[0]
    return [dispShape, backFillShape]

def addExcaInElemDicts(elemDicts, FL_GL_gap):
    allExcas = []
    for idx,dic in enumerate(elemDicts):
        elem = dic["Elem"]
        wms = dic["wms"]
        excaBln = "Exca" in "".join(list(map(lambda x: x["Dynamo 물량산출식"], wms)))
        if excaBln:
            sym_valDict = wms[0]["Sym_Val Dict"]
            excaGeo = makeExcaShape(elem, sym_valDict, FL_GL_gap)
            try:
                allExcasUni = Solid.ByUnion(allExcas)
                eff_excaGeo = excaGeo.Split(allExcasUni)[0]
                allExcas.append(excaGeo)
            except:
                eff_excaGeo = excaGeo
                allExcas.append(excaGeo)
            dic["ExcaGeo"] = eff_excaGeo

    return elemDicts

def find_allGeo_UG_elems(elemDicts):
    geoResult = []
    for dic in elemDicts:
        elem = dic["Elem"]
        wms = dic["wms"]
        excaBln = "Exca" in "".join(list(map(lambda x: x["Dynamo 물량산출식"], wms)))
        famType_ = wms[0]["Family Type Name"]
            
        if "MAT_" in famType_ or "Mass_" in famType_ or "Pit" in famType_ or "Trench" in famType_:
            if "Slab" in famType_ or "MAT_" in famType_ or "Mass_" in famType_ : ## 내부 빈공간 있는 RC부재는 꽉채워서 공제 
                srfs = elem.Geometry()[0].Explode() ## surface들
                btmSrf = PolySurface.ByJoinedSurfaces(list(filter(lambda x: round(x.NormalAtParameter(0.5,0.5).Z, 3) == -1, srfs)))
                btmCrvs = btmSrf.PerimeterCurves()
                btmPolCrv = PolyCurve.ByJoinedCurves(btmCrvs)
                btmCrvZ = btmPolCrv.StartPoint.Z
                uprPolCrv = btmPolCrv.Translate(0,0,(0-btmCrvZ))
                targetGeo = Solid.ByLoft([btmPolCrv,uprPolCrv])
                geoResult.append(targetGeo)
            else:
                geoResult.append(elem.Geometry()[0])
        elif "PED_" in famType_ or "TG_" in famType_ or "SOG_" in famType_ or "UG" in famType_:
            geoResult.append(elem.Geometry()[0])
            
        elif excaBln:
            geoResult.append(elem.Geometry()[0])

    return geoResult

def add_effExcaInElemDicts(elemDicts):
    
    FL_GL_gap = 0-GL_zElev
    allGeo_UG_RC_Elems = find_allGeo_UG_elems(elemDicts)
    allUniGeo_UG_RC_Elems = Solid.ByUnion(allGeo_UG_RC_Elems)
    elemDicts_excas = addExcaInElemDicts(elemDicts, FL_GL_gap)
    
    for dic in elemDicts_excas:
        if "ExcaGeo" in dic.keys():
            excaGeo = dic["ExcaGeo"]

            eff_excaGeo = excaGeo
            splitResult = eff_excaGeo.Split(allUniGeo_UG_RC_Elems)
            dic["effExcaGeo"] = eff_excaGeo
            dic["effBackfillGeo"] = splitResult[0]

        
        wms = dic["wms"]
        for wm in wms:
            if "Exca" in wm["Dynamo 물량산출식"] or\
               "Back" in wm["Dynamo 물량산출식"] or\
               "Disp" in wm["Dynamo 물량산출식"]:
                wm["Sym_Val Dict"]["Exca"] = dic["effExcaGeo"].Volume
                wm["Sym_Val Dict"]["Back"] = dic["effBackfillGeo"].Volume
                wm["Sym_Val Dict"]["Disp"] = dic["effExcaGeo"].Volume - dic["effBackfillGeo"].Volume

    return elemDicts_excas

def findBtmSrfs(geo):
    srfs = geo.Explode()
    btmSrf = PolySurface.ByJoinedSurfaces(list(filter(lambda x: round(x.NormalAtParameter(0.5,0.5).Z, 3) == -1, srfs)))
    return btmSrf

def calc_EarthWorkValue_InElemDicts(elemDicts, GL_zElev, paramSheetDic, wholeExca_CalcType):
    FL_GL_gap = 0 - GL_zElev
    allEarthRelatedElemsBtmSrfs = list(
        map(lambda x: findBtmSrfs(x["Elem"].Geometry()[0]), 
            filter(lambda dic: "ACF_W" in dic["wms"][0]["Family Type Name"] or \
                               "ACB_TG" in dic["wms"][0]["Family Type Name"] or \
                               "ACS_SOG" in dic["wms"][0]["Family Type Name"] or \
                               "ACE_Mass" in dic["wms"][0]["Family Type Name"] or \
                               "ACP_Pit Slab" in dic["wms"][0]["Family Type Name"], \
                elemDicts)))
    total_btmSrfsArea = sum(map(lambda x: x.Area, allEarthRelatedElemsBtmSrfs))
    total_Exca = makeExcaShape_whole(elemDicts, paramSheetDic, wholeExca_CalcType, FL_GL_gap)
    total_ExcaVolume = total_Exca.Volume
    total_Disp = makeDispShape_whole(elemDicts, paramSheetDic, FL_GL_gap)[0]
    total_DispVolume = total_Disp.Volume
    total_BackFill = makeDispShape_whole(elemDicts, paramSheetDic, FL_GL_gap)[1]
    total_BackFillVolume = total_BackFill.Volume
    
    for dic in elemDicts:
        elem = dic["Elem"]
        wms = dic["wms"]
        famType = wms[0]["Family Type Name"]
        for wm in wms:
            if "Exca" in wm["Dynamo 물량산출식"] or\
               "Back" in wm["Dynamo 물량산출식"] or\
               "Disp" in wm["Dynamo 물량산출식"] : ### 토공 산출 대상 부재에는 Exca Back Disp 세트로 포함하도록
                elem_btmSrfArea = findBtmSrfs(elem.Geometry()[0]).Area
                wm["Sym_Val Dict"]["Exca"] = total_ExcaVolume * (elem_btmSrfArea / total_btmSrfsArea)
                wm["Sym_Val Dict"]["Back"] = total_BackFillVolume * (elem_btmSrfArea / total_btmSrfsArea)
                wm["Sym_Val Dict"]["Disp"] = total_DispVolume * (elem_btmSrfArea / total_btmSrfsArea)
    
    return [elemDicts, [total_Exca, total_BackFill]]

def finalCalc_SymValDict(elemDicts):
    for dic in elemDicts:
        wms = dic["wms"]
        for wm in wms:
            formula = wm["Dynamo 물량산출식"]
            SymValDicts = wm["Sym_Val Dict"]
            #SymValItems = list(zip(SymValDicts.Keys, SymValDicts.Values))
            SymValItems = SymValDicts.items()
            sym_val_keySets = []
            sym_val_valSets = []
            for k,v in SymValItems:
                if k in formula:
                    sym_val_keySets.append(k)
                    sym_val_valSets.append(v)
            #wm["Sym_Val Set"] = [sym_val_keySets,sym_val_valSets]
            wm["Sym_Val Set"] = dict(zip(sym_val_keySets,sym_val_valSets))
            formula_eqSymRemove = formula.lstrip("=")
            tmp = formula_eqSymRemove
            for k in sym_val_keySets: ## 이 부분은 좀더 범용 처리 필요할수도
                priorSymList = ["Exca", "Back", "Disp"]
                #any(list(map(lambda x: x in tmp, priorList)))
                #if "Exca" in tmp or "Back" in tmp or "Disp" in tmp:
                if any(list(map(lambda x: x in tmp, priorSymList))):
                    appliedSym = list(filter(lambda x: x in tmp, priorSymList))[0]
                    #if len(k) > 1:
                    if k == appliedSym:
                        tmp = tmp.replace(k, str(wm["Sym_Val Set"][k]))
                else:
                    tmp = tmp.replace(k, str(wm["Sym_Val Set"][k]))
                
            
            #wm["calcResult"] = tmp.strip()
            wm["calcResult"] = round(eval(tmp.strip()),3)
    
    return elemDicts

def extractCalcResult(elemDicts):
    res = []
    for d in elemDicts:
        wms = d["wms"]
        for wm in wms:
            keys = ["SheetName", "rIDX", "Work Master Code", "Family Type Name", "calcResult"]
            vals = list(map(lambda x: wm[x],keys))
            k_v = list(zip(keys, vals))
            res.append(dict(k_v))
        
    return res

def extractCalcResult_forTotalBOQ(elemDicts):
    res = []
    for d in elemDicts:
        wms = d["wms"]
        for wm in wms:
            keys = ["SheetName", "rIDX", "Work Master Code", "Gauge Code", "wmSpecs", "Family Type Name", "calcResult"]
            vals = list(map(lambda x: wm[x],keys))
            k_v = list(zip(keys, vals))
            res_d = dict(k_v)
            if "Description" in wm.Keys:
                res_d["Description"] = wm["Description"]
            else:
                res_d["Description"] = ""
            res_d["wmcANDgauge"] = "".join([wm["Work Master Code"],wm["Gauge Code"]])
            res_d["UoM"] = wm["Unit"]
            res.append(res_d)
        
    return res

def make_dict_groupBy_Sheet_WM(elemDicts):
    extractedDicts = extractCalcResult(elemDicts)
    sortedDicts_sheet = sorted(extractedDicts, key=operator.itemgetter("SheetName"))
    grpDicts_Sheet = groupby(sortedDicts_sheet, lambda x: x["SheetName"])
    
    res = {}
    for k, g in grpDicts_Sheet:
        sorted_g = sorted(list(g), key=operator.itemgetter("rIDX"))
        grped_g = groupby(sorted_g, lambda x: x["rIDX"])
        tmp = []
        for k_,g_ in grped_g:
            gg = copy.deepcopy(list(g_))
            calcSum = round(sum(map(lambda x: x["calcResult"],gg)),3)
            rIDX = gg[0]["rIDX"]
            tmp.append((rIDX,calcSum))
            
        res[k] = tmp
    return res

def fill_dict_emptySlot(dic):
    tmp = []
    for k, v in dic.items():
        all_idxs = list(map(lambda x: x[0],v))
        max_idx = max(all_idxs)
        full_range = range(0, max_idx+1)
        
        for i in full_range:
            if i not in all_idxs:
                v.append([i, ""])
        tmp.append(sorted(v, key=operator.itemgetter(0)))
        
    res = list(zip(dic.keys(),tmp))
    return dict(res)

def make_dict_groupBy_WM(elemDicts):
    extractedDicts = extractCalcResult_forTotalBOQ(elemDicts)
    sortedDicts_WMC = sorted(extractedDicts, key=operator.itemgetter("wmcANDgauge"))
    grpDicts_WMC = groupby(sortedDicts_WMC, key=operator.itemgetter("wmcANDgauge"))
    
    res = []
    for k, g in grpDicts_WMC: 
        wmCode = k
        gg = copy.deepcopy(list(g))
        calcSum = round(sum(map(lambda x: x["calcResult"], gg)),3)
        wmSpecs = gg[0]["wmSpecs"]
        catStr = "_".join([wmSpecs[0],wmSpecs[1]])
        specOnly = list(filter(lambda x: x!=0, wmSpecs))[3:]
        addSpec = gg[0]["Description"]
        dict_res = {
            "catStr": catStr,
            "Work Master Code": wmCode,
            "Gauge Code": gg[0]["Gauge Code"],
            "Description": wmSpecs[2],
            "Spec.": "\n".join(specOnly),
            "Additional Spec.": addSpec,
            "calcVal": calcSum,
            "UoM": gg[0]["UoM"]
            #"wmSpecs": wmSpecs,
            }
        res.append(dict_res)
    
    
    return res

def getCompleteDicts_earth(elemDicts):
    if earthWork_calcMode:
        return calc_EarthWorkValue_InElemDicts(elemDicts, GL_zElev, paramSheetDic, wholeExca_CalcType)
    else:
        return [add_effExcaInElemDicts(elemDicts),0]



# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
lang_mode = IN[0]
earthWork_calcMode = IN[1]
wholeDatas = IN[2]

allCatSheetsNames = IN[3][2:]

allRevitElemsFlatten = IN[4]
GL_zElev = IN[5]
wholeExca_CalcType = IN[6]

# Place your code below this line
db = wholeDatas[1:]
paramSheet = db[0]
allCatSheets = db[1:]
Survey_Base_zGap = Revit.Elements.Coordinates.BasePoint().Z - Revit.Elements.Coordinates.SurveyPoint().Z

calcTypeDictsList = get_DataOnRangesAtParamSheet(paramSheet)
calcTypeDict = make_UnifiedDict(calcTypeDictsList)
paramSheetDic = get_SymValDict_PerCalcType(calcTypeDict) 

catSheetDic = make_AIOdic(allCatSheets)
catFam_paramDic = matchWith_paramDic(catSheetDic, paramSheetDic)

filteredEffRevitElems = filterEffRevitElems(allRevitElemsFlatten, catSheetDic)

elemDicts_updated_sym_valDict = update_sym_valDict(matchWith_Elem_Dict(catFam_paramDic,filteredEffRevitElems))

elemDicts_updated_Earthwork = getCompleteDicts_earth(elemDicts_updated_sym_valDict)
elemDicts_finalCalculated = finalCalc_SymValDict(elemDicts_updated_Earthwork[0])
dict_groupBy_Sheet_WM = make_dict_groupBy_Sheet_WM(elemDicts_finalCalculated)
resultForFamList = fill_dict_emptySlot(dict_groupBy_Sheet_WM)
resultForTotalBOQ = dict_groupBy_Sheet_WM



# Assign your output to the OUT variable.
OUT = [0,[resultForFamList, resultForTotalBOQ, 0]]