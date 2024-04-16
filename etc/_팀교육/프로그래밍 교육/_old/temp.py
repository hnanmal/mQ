# Load the Python Standard and DesignScript Libraries"
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

#wmspec_headers = [
#    "Work Master Code" ,"GaugeCode" ,"Unit" ,"Work Category-L1"
#    ,"Work Category-L2" ,"Work Category-L3" ,"Spec. 1- L4" ,"Spec. 2- L5"
#    ,"Spec. 3- L6" ,"Spec. 4- L7" ,"Spec. 5- L8" ,"Spec. 6- L9"
#    ,"Spec. 7- L10" ,"Spec. 8- L11" ,"BOQ Spec1" ,"BOQ Spec2" ,"BOQ Spec3"
#    ,"BOQ Spec4" ,"BOQ Spec5" ,"BOQ Spec6" ,"BOQ Spec7" ,"BOQ Spec8" ,"BOQ Spec9"
#    ,"Description" ,"입찰_물량산출식" ,"실행_물량산출식"
#]
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
    headers_sheet = list(map(lambda x: [x[1].replace("\n",""),x[0]], filter(lambda x: x[1] != None, enumerate(sheet[1]))))
    
    return dict(headers_sheet)
    #return list(headers_sheet)

def find_rangesAtSheet(sheet, hdrs_withIdxDict, trgt_hdr, trgt_str):
    #hdrs_withIdxDict = dict(hdrs_withIdx)
    return find_range_by_columnItem(sheet, hdrs_withIdxDict[trgt_hdr], trgt_str)


def get_DataOnGrpsAtSheet(sheet:list, discrHDRStr, discrRowStr):
    """
    판별기준 Header문자열(discrHDRStr)이 들어있는 열에서,
    판별기준 행 문자열(discrRowStr)이 들어있는 행번호 기준으로 구역을 나누어 데이터 리스트 반환
    """
    
    hdrs_withIdxDict = find_headersAtSheet(sheet)
    rowAreasAtSheet = find_rangesAtSheet(sheet, hdrs_withIdxDict, discrHDRStr, discrRowStr)
#    typesTitle_idx = list(map(lambda x: x[0]-1, rowAreasAtSheet)) # 각 타입 명이 위치한 인덱스
    rowsGrps_perType_withNone = list(map(lambda x: sheet[x[0]-1:x[1]], rowAreasAtSheet))
    # None 데이터 치환 구간
    rowsListGrps_perType = go(#>
        rowsGrps_perType_withNone, list,
        ## 하나의 타입을 규정하는 행들의 모임에서
        map(lambda rowGrp: \
        ## 한 행씩 골라서
        list(map(lambda row: \
        ## 행을 구성하는 셀 값 중 None이 있으면 빈문자열로 치환
        list(map(lambda cell: "" if cell==None else cell, row)), rowGrp)) ),
        ## 맵 객체가 반환되므로 리스트 변환
        list,
    )#<
    
    return (rowsListGrps_perType, hdrs_withIdxDict)

def cvt_rowsListGrps_toDictGrps(rowsListGrps_perType, hdrs_withIdxDict):
    """
    헤더 행과 다수의 컨텐츠 행으로 이루어진 rowListGrps를,
    모든 행을 헤더와 결합된 딕셔너리화 해서 rowDictGrps를 만드는 함수
    """
    eff_hdrs_idx = hdrs_withIdxDict.values()
    eff_hdrs_name = hdrs_withIdxDict.keys()
    
    rowsDictGrps_perType = go(#>
        rowsListGrps_perType,
        ## 하나의 타입을 규정하는 행들의 모임에서 한 행 씩 조작하는 함수들을 구상 후
        ## 맵 함수 내에서 go로 합성하여 반복시켜 사용
        map(lambda rowGrp: go(#>>
            ### 그룹 전체 가져와서
            rowGrp,
            ### 각 행을 리스트 타입으로 변환
            map(list), list,
            ### 헤더에 해당하는 행 값을 추출--
            map(lambda row: list(map(lambda idx: row[idx], eff_hdrs_idx))), list,
            ### 헤더이름과 행 내부의 값을 2개씩 짝지어 줌
            map(lambda row: list(zip(eff_hdrs_name, row))), list,
            ### 헤더이름 : 값의 형태로 각 행 데이터를 딕셔너리로 만듬
            map(lambda x: dict(x)), list,
            )#<<
        ), list,
    )#<
    return rowsDictGrps_perType

# 행딕셔너리 별 입력한 규칙에 따라 참거짓 여부를 반환하는 함수
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



def form_TypeDict(rowsDictGrps,titleKeyName,sttIdx):
    """
    rowsDictGrps_perType을 받아서 각 그룹의 이름을 키로 하는
    새로운 중첩구조의 Dictionary를 만들어서,
    바깥에서 타입이름으로 딕셔너리에 접근하면 
    바로 해당 구성내용을 반환해주는 데이터 구조를 만드는 함수
    """
    typeDict = go(#>
        rowsDictGrps, list,
        filter(lambda x: x!=[]),
        map(lambda rowsDictGrp: \
            ### 그룹 전체 첫행 중 타이틀키값과 나머지 row 들 dict를 짝지어 새로운 딕셔너리로 형성
            [list(rowsDictGrp)[0][titleKeyName],go(#>>
                list(rowsDictGrp)[sttIdx:],
                #### 모두 빈칸인 값일때 제외 필터링
                filter(lambda row: any(list(map(lambda cell: cell!="", list(row.values()))))),
                list,
            )]#<<
        ),list,
        dict,
    )#<
    
    return typeDict

def updateDict_symValPair(calcTypeDict):
    allCalcTypeNames = list(calcTypeDict.keys())
    res = {}
    for x in allCalcTypeNames:
        type = {}
        for rD in calcTypeDict[x]:
            if rD["수동 입력값"]!="" and rD["산출수식 약자"]!="":
                rD["applyForCalc"] = rD["수동 입력값"]
                type[rD["산출수식 약자"]]=rD["applyForCalc"]
            elif rD["Parameter"]!="" and rD["산출수식 약자"]!="":
                rD["applyForCalc"] = rD["Parameter"]
                type[rD["산출수식 약자"]]=rD["applyForCalc"]
        res[x] = type
    return res
   

def find_stdWMdicts_inGrp(rowsDictGrp):
    res = go(
        rowsDictGrp, list,
        ## 엑셀 "물량산출식", "Work Master Code" 열에 값이 없는 행 제외
        filter(lambda rD: rD["입찰_물량산출식"] != "" and rD["실행_물량산출식"] != ""),
        filter(lambda rD: rD["Work Master Code"] != ""),
        ## Family Type Name에 "H_" 문자열 포함된 경우 제외
        filter(lambda rD: not findRow_AppliedType(rD, "Family Type Name", rule="H_")),
        ## 행 딕셔너리의 NO, Standard Type 업데이트
        map(lambda rD: dictUpdate(rD,{"NO":rowsDictGrp[0]["NO"], "Standard Type":rowsDictGrp[0]["Standard Type"]})),
        ## Q'ty Cal Type Tag 업데이트
        map(lambda rD: dictUpdate(rD,{"Q'ty Cal Type Tag":rowsDictGrp[0]["Q'ty Cal Type Tag"]})),
        list,
    )
    return res


def find_stdWMdicts_forCat(rowsDictsGrps):
    res = go(#>
        rowsDictsGrps, list,
        map(find_stdWMdicts_inGrp),
        #filter(lambda x: x!=[]),
        list,
    )#<
    return res

def find_appliedTypeDicts_forCat(rowsDictsGrps):
    eff_hdrs_name = list(rowsDictsGrps[0][0].keys())
    wmspec_headers = ["Work Master Code", "GaugeCode", "Unit"]\
        + list(filter(lambda x: "Work Cat" in x or "Spec" in x, eff_hdrs_name))\
        + ["Description","입찰_물량산출식", "실행_물량산출식"]
    #stdWMsDicts = find_stdWMdicts_forCat(rowsDictGrps)
    
    appliedTypeDicts = go(#>
        rowsDictsGrps,
        map(lambda rowsDictsGrp: go(#>>
            rowsDictsGrp, list,
            ## Family Type Name에 "H_" 문자열 포함된 경우만 필터링
            filter(lambda rD: findRow_AppliedType(rD, "Family Type Name", rule="H_")),
            ## 행 딕셔너리의 NO, Standard Type 업데이트 - 추후 함수 분리 염두
            map(lambda rD: dictUpdate(rD,{"NO":rowsDictsGrp[0]["NO"], "Standard Type":rowsDictsGrp[0]["Standard Type"]})),
            ## 그룹 첫행을 기준으로 Q'ty Cal Type Tag 업데이트 - 추후 함수 분리 염두
            map(lambda rD: dictUpdate(rD,{"Q'ty Cal Type Tag":rowsDictsGrp[0]["Q'ty Cal Type Tag"]})),
            
            # wmSpecs 속성들을 헤더로 하는 새로운 딕셔너리 형성 및 값 추가(값은 list형태)
            map(lambda rD: dictUpdate(rD, {"wmSpecs": go(
                ### wmspec관련 항목들 값을 리스트로 모음
                map(lambda x: rD[x], wmspec_headers), list,
                ### 항목명과 항목값을 모아서 딕셔너리 형태로 변환
                lambda x: zip(wmspec_headers,x), dict,
                ### wmSpecs 항목을 리스트 구조로 수정해 두기
                lambda x: [x] if x["Work Master Code"]!="" else [],
                
            )}) ),
            ## 밖으로 꺼내진 WorkMaster 관련 속성 삭제
            map(lambda rD: dictDeleteKeys(rD, wmspec_headers)), list,
            #filter(lambda rD: rD["wmSpecs"][0]["Work Master Code"]!=""),
            list,
            )#<<
        ),
        # 실적용 패밀리타입이 없는 그룹은 제외하는 구간
        filter(lambda x: list(x)!=[]),
        list,
    )#<
    
    return appliedTypeDicts

def find_appliedTypeDicts_forRoom(rowsDictsGrps):
    eff_hdrs_name = list(rowsDictsGrps[0][0].keys())
    wmspec_headers = ["Work Master Code", "GaugeCode", "Unit"]\
        + list(filter(lambda x: "Work Cat" in x or "Spec" in x, eff_hdrs_name))\
        + ["Description","입찰_물량산출식", "실행_물량산출식"]
    
    appliedTypeDicts = go(#>
        rowsDictsGrps,
        map(lambda rowsDictsGrp: go(#>>
            rowsDictsGrp, list,
            ## Family Type Name에 "H_" 문자열 포함된 경우만 필터링
            filter(lambda rD: findRow_AppliedType(rD, "Standard Type")),
            ## 행 딕셔너리의 NO, Standard Type 업데이트 - 추후 함수 분리 염두
            map(lambda rD: dictUpdate(rD,{"NO":rD["Standard Type"], "Standard Type":rowsDictsGrp[0]["Standard Type"]})),
            ## 그룹 첫행을 기준으로 Q'ty Cal Type Tag 업데이트 - 추후 함수 분리 염두
            map(lambda rD: dictUpdate(rD,{"Q'ty Cal Type Tag":rowsDictsGrp[0]["Q'ty Cal Type Tag"]})),
            
            # wmSpecs 속성들을 헤더로 하는 새로운 딕셔너리 형성 및 값 추가(값은 list형태)
            map(lambda rD: dictUpdate(rD, {"wmSpecs": go(
                ### wmspec관련 항목들 값을 리스트로 모음
                map(lambda x: rD[x], wmspec_headers), list,
                ### 항목명과 항목값을 모아서 딕셔너리 형태로 변환
                lambda x: zip(wmspec_headers,x), dict,
                ### wmSpecs 항목을 리스트 구조로 수정해 두기
                lambda x: [x] if x["Work Master Code"]!="" else [],
                
            )}) ),
            ## 밖으로 꺼내진 WorkMaster 관련 속성 삭제
            map(lambda rD: dictDeleteKeys(rD, wmspec_headers)), list,
            #filter(lambda rD: rD["wmSpecs"][0]["Work Master Code"]!=""),
            list,
            )#<<
        ),
        # 실적용 패밀리타입이 없는 그룹은 제외하는 구간
        filter(lambda x: list(x)!=[]),
        list,
    )#<
    
    return appliedTypeDicts

def merge_sameFamType_wmSpecs(appliedTypeDicts):
    def merge_inGrp(appliedTypeDicts_perGrp):
        keysPerGrp = go(#>
            appliedTypeDicts_perGrp,
            map(lambda rD: rD["Family Type Name"]),
            filter(lambda x: "H_" in x),
            ## 중복 Family Type Name 단일화
            set,
            list,
        )#<
        
        for k in keysPerGrp:
            sameNameDicts = list(filter(lambda x: x["Family Type Name"] == k, appliedTypeDicts_perGrp))
            if len(sameNameDicts)>=2:
                for i,rD in enumerate(sameNameDicts[1:]):
                    sameNameDicts[0]["wmSpecs"].append(*rD["wmSpecs"])
                appliedTypeDicts_perGrp.remove(sameNameDicts[i+1])
            else:                
                pass
        return appliedTypeDicts_perGrp
    
    return map(merge_inGrp, appliedTypeDicts)



def inject_stdWMtoAppliedTypeDicts(appliedTypeDicts, allCat_stdWMdicts_stdTypeName):
    def inject_inGrp(appliedTypeDict_perGrp):
        for rD in appliedTypeDict_perGrp:
            if rD["Standard Type"] in list(allCat_stdWMdicts_stdTypeName.keys()):
                rD["wmSpecs"] = rD["wmSpecs"] + allCat_stdWMdicts_stdTypeName[rD["Standard Type"]]
            else:
                pass

        return appliedTypeDict_perGrp
    return list(map(inject_inGrp, appliedTypeDicts))
    
def updateFamTypeDicts_symValPair(total_appliedTypeDicts, calcTypeDict_symValPair):
    res = {}
    for d in total_appliedTypeDicts:
        if d["Q'ty Cal Type Tag"]!="":
            symValPair = calcTypeDict_symValPair[d["Q'ty Cal Type Tag"]]
            d["Sym_Val Dict"] = symValPair
        res[d["Family Type Name"]] = d    
    return res
    
    
    
    
calcSheet_rowsListGrps_perType = get_DataOnGrpsAtSheet(calcStdSheet, "구간판별", "#")
calcSheet_rowsDictGrps_perType = cvt_rowsListGrps_toDictGrps(*calcSheet_rowsListGrps_perType)
calcTypeDict = form_TypeDict(calcSheet_rowsDictGrps_perType,"Q'ty Cal Type Tag",sttIdx=1)
calcTypeDict_symValPair = updateDict_symValPair(calcTypeDict)

roomSheet_rowsListGrps_perType = get_DataOnGrpsAtSheet(allCatSheets[0], "Standard Type", "H_")
roomSheet_rowsDictGrps_perType = cvt_rowsListGrps_toDictGrps(*roomSheet_rowsListGrps_perType)
room_stdWMdicts = find_stdWMdicts_forCat(deepcopy(roomSheet_rowsDictGrps_perType))
room_stdWMdicts_stdTypeName = form_TypeDict(room_stdWMdicts, "Standard Type",sttIdx=0)

room_appliedTypeDicts = find_appliedTypeDicts_forRoom(roomSheet_rowsDictGrps_perType)
room_appliedTypeDicts_noDupl = merge_sameFamType_wmSpecs(room_appliedTypeDicts)

room_appliedTypeDicts_withStdWm = list(chain(*inject_stdWMtoAppliedTypeDicts(room_appliedTypeDicts_noDupl, room_stdWMdicts_stdTypeName)))

# 룸 제외 모든 카테고리 시트 처리
allCatSheet_rowsListGrps = map( lambda x: get_DataOnGrpsAtSheet(x, "Standard Type", "H_"), allCatSheets[1:] )
allCatSheet_rowsDictGrps = map( lambda x: cvt_rowsListGrps_toDictGrps(*x), allCatSheet_rowsListGrps )

# "Standard Type" 별 wm 공통항목 찾기
allCat_stdWMdicts = list(map( lambda x: find_stdWMdicts_forCat(x), deepcopy(allCatSheet_rowsDictGrps) ))
# "Standard Type" 명으로 검색할 수 있는, 전 카테고리 "Standard Type" 별 공통 WM항목 사전 만들기
allCat_stdWMdicts_stdTypeName = dictsMerge(list(map(lambda x: form_TypeDict(x, "Standard Type",sttIdx=0), allCat_stdWMdicts)))

allCat_appliedTypeDicts = map( lambda x: find_appliedTypeDicts_forCat(x), allCatSheet_rowsDictGrps )
allCat_appliedTypeDicts_noDupl = map( lambda x: merge_sameFamType_wmSpecs(x), allCat_appliedTypeDicts )

allCat_appliedTypeDicts_withStdWm = list(chain(*chain(*map( lambda x: inject_stdWMtoAppliedTypeDicts(x,allCat_stdWMdicts_stdTypeName), allCat_appliedTypeDicts_noDupl ))))

total_appliedTypeDicts = room_appliedTypeDicts_withStdWm + allCat_appliedTypeDicts_withStdWm
FamTypeDicts_symValPair = updateFamTypeDicts_symValPair(total_appliedTypeDicts,calcTypeDict_symValPair)

# Assign your output to the OUT variable.

OUT = FamTypeDicts_symValPair