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