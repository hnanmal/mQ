# Load the Python Standard and DesignScript Libraries
import sys
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#################################Module For Functional Programing#############################################
from functools import reduce
from itertools import chain
from itertools import groupby
from copy import deepcopy
curry = lambda f: lambda a,*args: f(a, *args) if (len(args)) else lambda *args: f(a, *args)

filter = curry(filter)
map = curry(map)
reduce = curry(reduce)

go = lambda *args: reduce(lambda a,f: f(a), args) ## 함수도 축약 가능 ##

def dictUpdate(dic1,dic2):
    res = dic1.update(dic2)
    #res = {**dic1,**dic2}
    return dic1 #res
    
def dictsMerge(dics):
    res = reduce(dictUpdate, dics)
    return res
    
def dictDeleteKeys(dic, keys):
    for k in keys:
        del dic[k]
    return dic
##############################################################################################################

import re
from functools import partial

# The inputs to this node will be stored as a list in the IN variables.
dataEnteringNode = IN
lang_mode = IN[0]
wholeDatas = IN[1]
db = wholeDatas[1:]
allCatSheetsNames = IN[2][2:]

calcStdSheet = db[0] ##산출기준 시트
allCatSheets = db[1:]


# Place your code below this line

def find_IsInStr(target, string):
    if target == None or string == None:
        pass
    else:
        res = str(target) in str(string)
        return res

def find_range_by_columnItem(db, col_idx, sep_rule):
    tdb = list(map(lambda x: x[col_idx], db)) ##targetTransposedDB (col_idx에 해당하는 데이터만 추출)
    last_idx_tdb = len(tdb)-1
    tdb_enum = enumerate(tdb)
    target_RowNumber = list(filter(lambda x: find_IsInStr(sep_rule, x[1]), tdb_enum))
    endidxs_tmp= list(map(lambda x: x[0]-1,target_RowNumber))
    endidxs_tmp.pop(0)
    endidxs = endidxs_tmp + [last_idx_tdb] ## 각 구간별 마지막 행 번호
    rangeSttIdxs = list(map(lambda x: x[0]+1,target_RowNumber))
    rangeEndIdxs = endidxs
    result = list(zip(rangeSttIdxs, rangeEndIdxs))
    return result

    
def find_headersAtSheet(sheet):
    headers_sheet = map(lambda x: [x[1].replace("\n",""),x[0]], filter(lambda x: x[1] != None, enumerate(sheet[1])))
    
    #return dict(headers_sheet)
    return list(headers_sheet)

def find_rangesAtSheet(sheet, hdrs_withIdx, trgt_hdr, trgt_str):
    hdrs_withIdxDict = dict(hdrs_withIdx)
    return find_range_by_columnItem(sheet, hdrs_withIdxDict[trgt_hdr], trgt_str)


def get_DataOnRowAreasAtSheet(sheet:list, discrHDRStr, discrRowStr):
    """
    판별기준 Header문자열(discrHDRStr)이 들어있는 열에서,
    판별기준 행 문자열(discrRowStr)이 들어있는 행번호 기준으로 구역을 나누어 데이터 리스트 반환
    """
    
    hdrs_withIdx = find_headersAtSheet(sheet)
    rowAreasAtSheet = find_rangesAtSheet(sheet, hdrs_withIdx, discrHDRStr, discrRowStr)
    typesTitle_idx = list(map(lambda x: x[0]-1, rowAreasAtSheet)) # 각 타입 명이 위치한 인덱스
    rowsGrps_perType_withNone = list(map(lambda x: sheet[x[0]-1:x[1]], rowAreasAtSheet))
    # None제거
    rowsGrps_perType = go(
        rowsGrps_perType_withNone,
        ## 하나의 타입을 규정하는 행들의 모임에서
        map(lambda rowGrp: \
        ## 한 행씩 골라서
        map(lambda row: \
        ## 행을 구성하는 셀 값 중 None이 있으면 빈문자열로 치환
        map(lambda cell: "" if cell==None else cell, row), rowGrp) ),
        ## 맵 객체가 반환되므로 리스트 변환
        list,
    )
    
    return (rowsGrps_perType, hdrs_withIdx)


def setDict_OnEachCalType(data_perType, hdrs_withIdx):
    """
    data_perType: '#' 등의 구분기호를 통해 나뉘어진 행 구간 내 전체 데이터_(행기준으로 구분된 형식)
    """
    hdrs_withIdxDict = dict(hdrs_withIdx)
    eff_hdrs_idx = list(zip(*hdrs_withIdx))[1]
    eff_hdrs_name = list(zip(*hdrs_withIdx))[0]
    # 
    calcTypeName = data_perType[0][hdrs_withIdxDict["Q'ty Cal Type Tag"]]

    paramDicts_withTypeName = go(
        data_perType,
        ## 엑셀 "항목" 열에 값이 없는 행 제외
        filter(lambda row: row[hdrs_withIdxDict["항목"]] != None), list,
        
        ## 모든 Null 값 빈문자열로 치환
        map(lambda row: list(map(lambda cell: cell if cell!=None else "",row))), list,

        ## 헤더에 해당하는 행 값을 추출--
        map(lambda row: list(map(lambda idx: row[idx], eff_hdrs_idx))), list,
        
        ## 헤더이름과 행 내부의 값을 2개씩 짝지어 줌
        map(lambda row: list(zip(eff_hdrs_name, row))), list,
        
        ## 헤더이름 : 값의 형태로 각 행 데이터를 딕셔너리로 만듬
        map(lambda x: dict(x)), list,
        
        ## "산출수식 약자" 키에 할당된 값이 빈문자열인 경우 제외
        filter(lambda d: d["산출수식 약자"]!=""), list,
        
        ## 딕셔너리에 "Q'ty Cal Type Tag" 키-값 추가
        map(lambda d: dictUpdate(d,{"Q'ty Cal Type Tag":calcTypeName})), list,
        
        ## 딕셔너리에 "applyForCalc" 키-값 추가
        ## ("수동 입력값"항목이 있는 경우에는 그값을 적용하고 아닌경우 "Parameter"항목 값
        map(lambda d: dictUpdate(d, { "applyForCalc":\
            d["수동 입력값"] if d["수동 입력값"] != "" \
            else d["Parameter"] if d["Parameter"] != "" \
            else 0 })), list,
        
        ## 타입이름을 키값으로 하는 중첩 딕셔너리 형성
        lambda x: {calcTypeName: x},
    )

    return paramDicts_withTypeName

###################################################################################################################
#!!! 함수가 너무 크다 쪼개자
#!!! setDict_OnEachFamType
#!!! -> setDict_EachRow_perGroup//setDict_stdWM_perGroup//setDict_applied_perGroup
###################################################################################################################

#def setDict_OnEachFamType(data_perType, hdrs_withIdx, cat=None):


def setDict_OnEachFamType(data_perType, hdrs_withIdx, cat=None):
    """
    data_perType: '#' 등의 구분기호를 통해 나뉘어진 행 구간 내 전체 데이터_(행기준으로 구분된 형식)
    hdrs_withIdx: 헤더 명과 인덱스 번호가 순서대로 나열된 중첩 리스트
    cat : Room 시트 여부 판별용 입력값
    """
    hdrs_withIdxDict = dict(hdrs_withIdx)
    eff_hdrs_idx = list(zip(*hdrs_withIdx))[1]
    eff_hdrs_name = list(zip(*hdrs_withIdx))[0]
    # data_perType 에서, 타입 그룹 별로 "Q'ty Cal Type Tag" 열에 있는 값이
    # None일때가 있으므로 예외처리를 해주는 구간
    calcTypeName = data_perType[0][hdrs_withIdxDict["Q'ty Cal Type Tag"]] \
        if data_perType[0][hdrs_withIdxDict["Q'ty Cal Type Tag"]]!=None else "N/A"
    stdFamTypeNo = data_perType[0][hdrs_withIdxDict["NO"]]
    stdFamTypeName = data_perType[0][hdrs_withIdxDict["Standard Type"]]

    wmspec_headers = ["Work Master Code", "GaugeCode", "Unit"]\
        + list(filter(lambda x: "Work Cat" in x or "Spec" in x, eff_hdrs_name))\
        + ["Description","입찰_물량산출식", "실행_물량산출식"]
    
    # 그룹 안의 모든 행을 리스트에서 칼럼 명이 붙은 딕셔너리로 전환하는 구간
    # 실제 적용 패밀리 타입 및 각각 개별할당 WM 정리
    rowDicts = go(
        data_perType,
        ## 모든 Null 값 빈문자열로 치환
        map(lambda row: list(map(lambda cell: cell if cell!=None else "",row))), list,
        
        ## 헤더에 해당하는 행 내용을 추출
        map(lambda row: list(map(lambda idx: row[idx], eff_hdrs_idx))), list,
        
        ## 헤더이름과 행 내부의 값을 2개씩 짝지어 줌
        map(lambda row: list(zip(eff_hdrs_name, row))), list,        

        ## 헤더이름 : 값의 형태로 각 행 데이터를 딕셔너리로 만듬
        map(lambda x: dict(x)), list,
    )

    # 그룹 내의 모든 행딕셔너리 들 중 찾고자 하는 규칙에 따라 참거짓 여부를 반환하는 함
    def findRow_AppliedType(rowDict, tgtHDRname, rule=None):
        p = re.compile('[0-9]{3,5}')
        target = str(rowDict[tgtHDRname])
        ## 함수 호출시 구분자(rule) 없이 호출한 경우
        ## -Room Category 시트 용 이며 "Standard Type" 항목의 값이 000형태의 숫자인지를 판별
        ## -Room Category 중 "Standard Type" 칼럼에 룸 넘버, "Family Type Name" 칼럼에 룸 이름 입력하게 되어있음
        if rule==None:
            p = re.compile('[0-9]{3,5}')
            m = p.match(target)
            stdCase = target =="Room No"
            res = all([m or stdCase])
        ## 구분자(rule)가 정규표현식 객체로 들어온 경우
        elif isinstance(rule, re.Pattern):
            m = p.match(target)
            res = all([m])
        ## 구분자(rule)가 문자열로 들어온 경우
        else:
            res = rule in target
        return res
    
    # 그룹 내의 모든 행 딕셔너리 중, 개별 적용 패밀리명이 아닌 공통 WM 항목에 대한 정보 추출
    stdFamTypeInfo = go(
        rowDicts,
        ## 엑셀 "물량산출식", "Work Master Code" 열에 값이 없는 행 제외
        ## Family Type Name에 "H_" 문자열 포함된 경우 제외
        filter(lambda d: d["입찰_물량산출식"] != ""),
        filter(lambda d: d["실행_물량산출식"] != ""),
        filter(lambda d: d["Work Master Code"] != ""),
        filter( lambda d: \
            (not findRow_AppliedType(d, "Standard Type")) or (not findRow_AppliedType(d, "Standard Type", rule="H_")) \
            ### 룸카테고리인 경우는 "Standard Type"항목에 값이 숫자가 아니거나, "H_"문자열이 포함되지 않은 항목 추출
            if cat == "roomCat" else\
            ### 룸카테고리가 아닌 경우, "Family Type Name" 항목에 "H_"문자열 포함되지 않은 항목 추출 
            not findRow_AppliedType(d, "Family Type Name", rule="H_") ),
        list,
        
        # wmSpecs 속성들을 헤더로 하는 새로운 딕셔너리 형성 및 값 추가(값은 list형태)
        map( lambda d: \
            go(
                ### wmspec관련 항목들 값을 리스트로 모음
                map(lambda x: d[x], wmspec_headers), list,
                ### 항목명과 항목값을 모아서 딕셔너리 형태로 변환
                lambda x: zip(wmspec_headers,x), dict,
            )
        ),
        list,
    )
    
    def dictsUnion_withInnerKey(dicts:list,innerkey):
        """
        최상위 키값이 "하나"이고, 그 하위에 종속된 딕셔너리의 키구성이 동일한 복수의 딕셔너리 중 ,
        키 값이 동일한 것이 있을 때 딕셔너리별로 해당 키에 대응하는 값들을
        맨 처음의 딕셔너리로 값으로 재할당하고 해당 딕셔너리만 반환
        """
        # 최상위 키값을 기준으로 딕셔너리들 그루핑
        if len(dicts) != 0:
            groupedDicts = go(
                dicts,
                lambda col: sorted(col, key=lambda x:list(x.keys())),
                lambda col: groupby(col, lambda x: list(x.keys())),
                map(lambda x: list(map(lambda y: list(y), x))),
                list,
            )
            # 최상위 키값이 중복되는 딕셔너리를 모은 리스트
            plurals = list(map(lambda y: y[1], filter(lambda x: len(x[1])>1, groupedDicts)))
            # 최상위 키값이 다른 어떤 딕셔너리와 중복되지 않는 단일 개체들 모은 리스트
            singles = list(map(lambda y: y[1][0], filter(lambda x: len(x[1])==1, groupedDicts)))
            # 하부딕셔너리 구성키 전체
            #hdrs = list(dicts[0][list(dicts[0].keys())[0]].keys())
            
            # plurals 없는 경우 처리
            if len(plurals)==0:
                res = singles
            else:
                newPlurals = []
                for sameKeyGroup in plurals:
                    ### 최상단 키
                    titleKey = list(sameKeyGroup[0].keys())[0]
                    newD = deepcopy(sameKeyGroup[0])
                    newD[titleKey][innerkey]=[]
                    for d in sameKeyGroup:
                        newD[titleKey][innerkey].append(d[titleKey][innerkey][0])
                    newPlurals.append(newD)
                res = newPlurals + singles
        
            return res
        
    # 그룹 내의 모든 행 딕셔너리 중, 개별 적용 패밀리에 대한 정보 추출
    # 엑셀 시트에서 "Family Type Name" 칼럼의 값이 보라색으로 기입된 모든 행 대상
    actualAppliedFamTypeInfo = go( ##!!! 적용 패밀리 이름 동일한게 있을때 내용 합치는 구간 추가 필요
        rowDicts,
        ## Family Type Name 항목 중 "H_" 문자열이 포함된 개체만 필터링
        filter( lambda d: \
            findRow_AppliedType(d, "Standard Type") \
            if cat == "roomCat" else\
            findRow_AppliedType(d, "Family Type Name", rule="H_")
            ),
        
        ## 행 딕셔너리에 wmSpecs 속성 및 값 추가(값은 list형태)
        ##!!! 적용 패밀리 이름 동일한게 있을때 내용 합치는 구간 추가 필요 - 공통 WM 추가 코드는 분리 필요
        map( lambda d: dictUpdate(d, {"wmSpecs": \
            go(
                ### wmspec관련 항목들 값을 리스트로 모음
                map(lambda x: d[x], wmspec_headers), list,
                ### 항목명과 항목값을 모아서 딕셔너리 형태로 변환
                lambda x: zip(wmspec_headers,x), dict,
                
                ### wmSpecs 항목을 리스트 구조로 수정해 두기 & 개별 WM정보가 없는 경우는 리스트에서 제외
                #lambda x: [x] if x["Work Master Code"]!="" else [],
                ### stdFamType의 WM정보와 합치기 - 밖으로 분리 필요
                lambda x: [ *stdFamTypeInfo, x \
                    if x["Work Master Code"]!="" else ["No Individual WM information"] ],
                ### 개별 WM정보가 없는 경우는 리스트에서 제외
                filter(lambda x: isinstance(x,dict)), list,
            ) }) 
        ), list,
        
        ## 밖으로 꺼내진 WorkMaster 관련 속성 삭제
        map(lambda d: dictDeleteKeys(d, wmspec_headers)), list,
        
        ## 딕셔너리에 Q'ty Cal Type Tag 키에 값 업데이트
        map(lambda d: dictUpdate(d,{"Q'ty Cal Type Tag": calcTypeName})), list,
        
        ## 딕셔너리에 Standard Type키에 값 업데이트
        map( lambda d: dictUpdate(d,{"NO":d["Standard Type"], "Standard Type":stdFamTypeName})) \
            if cat=="roomCat" \
            else map(lambda d: dictUpdate(d,{"NO":stdFamTypeNo, "Standard Type":stdFamTypeName}) ), 
        list,
        
        ## 딕셔너리에 wmSpecs 내 "Work Master Code" 값을 GaugeCode 포함한 값으로 업데이트 (필요한가?)
        
        
        ## Family Type Name 문자열을 키값으로 하는 딕셔너리로 변형
        #map(lambda d: {d["Family Type Name"]:d}), list,
        map(lambda d: {f'{d["NO"]}'+"_"+d["Family Type Name"]:d})\
            if cat=="roomCat" \
            else map(lambda d: {d["Family Type Name"]:d}), list,
        
        ## 최상위 키가 1개인 딕셔너리들 중 최상위 키 값이 같은 딕셔너리 들만 "wmSpecs" 내용 합치기
        #lambda x: dictsUnion_withInnerKey(x, "wmSpecs"),
        
    )
    
    return eff_hdrs_idx#actualAppliedFamTypeInfo



def dataToDict(setDict_f, args, cat=None):
    (datas_perType, hdrs_withIdx) = args
    res = go(
        datas_perType,
        ## 
        map( lambda datas: \
            setDict_f(datas, hdrs_withIdx, cat=cat) if cat=="roomCat" \
            else setDict_f(datas, hdrs_withIdx)
        ),
            
        ## 빈 리스트라서 매치할 수 없는 개체 제외
        filter(lambda x: x!=[] and x!=None), list,
        
        ## 산출기준 시트와, 카테고리별 시트의 산출 결과물이 양식이 조금 다르므로
        ## 각 단위 데이터가 리스트인지 여부를 확인후 펼쳐주는 구간 추가
        lambda x: list(chain(*x)) if all(map(lambda y: isinstance(y, list),x)) else x,
    )    

    return res

def dataToDict_tmp(setDict_f, args, cat=None): ### 디버깅 용으로만 한정적 사용
    (datas_perType, hdrs_withIdx) = args
    res = go(
        datas_perType,
        ## 
        map( lambda datas: \
            setDict_f(datas, hdrs_withIdx, cat=cat) if cat=="roomCat" \
            else setDict_f(datas, hdrs_withIdx)
        ), list,
    )
    
    return res

def merge_wmSpecs_sameKey(d:dict):
    pass
    

def match_FamTypeWithCalcType(calcStdTypeDict, allCatFamTypeDict):
    allFamTypeDicts = list(chain(*allCatFamTypeDict))
    res = dictsMerge(allFamTypeDicts)
    
    return res
    pass


calcStdTypeData = get_DataOnRowAreasAtSheet(calcStdSheet, "구간판별", "#")
#calcStdTypeDict = dataToDict(setDict_OnEachCalType, calcStdTypeData)

#roomFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[0], "Standard Type", "H_")
#roomFamTypeDict = dataToDict(setDict_OnEachFamType, roomFamTypeData, cat="roomCat")
#
#allCatFamTypeData = map( lambda x: get_DataOnRowAreasAtSheet(x, "Standard Type", "H_"), allCatSheets[1:] )
#allCatFamTypeDict = [roomFamTypeDict] + list(map( lambda x: dataToDict(setDict_OnEachFamType, x), allCatFamTypeData ))

#allCatFamType_CalcDict = 

floorsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[1], "Standard Type", "H_")
#floorsFamTypeDict = dataToDict(setDict_OnEachFamType, floorsFamTypeData)
#res = setDict_OnEachFamType(floorsFamTypeData)

#roofsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[2], "Standard Type", "H_")
#roofsFamTypeDict = dataToDict(setDict_OnEachFamType, roofsFamTypeData)
#
#wallsExtFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[3], "Standard Type", "H_")
#wallsExtFamTypeDict = dataToDict(setDict_OnEachFamType, wallsExtFamTypeData)
#
#wallsIntFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[4], "Standard Type", "H_")
#wallsIntFamTypeDict = dataToDict(setDict_OnEachFamType, wallsIntFamTypeData)
#
#stFdnsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[5], "Standard Type", "H_")
#stFdnsFamTypeDict = dataToDict(setDict_OnEachFamType, stFdnsFamTypeData)
#
#stColsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[6], "Standard Type", "H_")
#stColsFamTypeDict = dataToDict(setDict_OnEachFamType, stColsFamTypeData)
#
#stFrmsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[7], "Standard Type", "H_")
#stFrmsFamTypeDict = dataToDict(setDict_OnEachFamType, stFrmsFamTypeData)
#
#ceilingsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[8], "Standard Type", "H_")
#ceilingsFamTypeDict = dataToDict(setDict_OnEachFamType, ceilingsFamTypeData)
#
#doorsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[9], "Standard Type", "H_")
#doorsFamTypeDict = dataToDict(setDict_OnEachFamType, doorsFamTypeData)
#
#windowsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[10], "Standard Type", "H_")
#windowsFamTypeDict = dataToDict(setDict_OnEachFamType, windowsFamTypeData)
#
#stairsFamTypeData = get_DataOnRowAreasAtSheet(allCatSheets[11], "Standard Type", "H_")
#stairsFamTypeDict = dataToDict(setDict_OnEachFamType, stairsFamTypeData)

# Assign your output to the OUT variable.

OUT = calcStdTypeData#match_FamTypeWithCalcType(calcStdTypeDict, allCatFamTypeDict)