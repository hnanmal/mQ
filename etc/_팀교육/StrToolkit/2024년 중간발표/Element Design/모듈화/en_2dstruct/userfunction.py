import numpy as np
np.set_printoptions(precision=6, suppress=True)
from .bridgefunction import *
from .r2f import rabbit2kgbsturct
from .utilityfunction import getTimeStamp, findReadFile


# V3.000
# 모듈화 분리


def kgbstruct_2D(node_input,element_input_truss,element_input_frame,boundary_input,load_input):  # truss input과 beamcolumninput 구분
    nodeinformation = Node(node_input)

    elementinformation = Element_ElasticTruss(nodeinformation, element_input_truss)
    asdf = Element_ElasticBeamcolumn(nodeinformation, element_input_frame)
    elementinformation.update(asdf)

    boundaryinformation = Fix(nodeinformation, boundary_input)
    [loadmatrix, nodal_load, element_load] = Loads(nodeinformation, elementinformation,load_input)
    [reactions, displacement]= Eleasticsolve(nodeinformation,elementinformation,boundaryinformation,loadmatrix)


    [reaction_return, displacement_return]= arraythereturn(node_input, boundary_input, reactions, displacement)


    return nodeinformation, elementinformation, boundaryinformation, reaction_return, displacement_return

def kgbstruct_2D_wGUID(node_input,element_input_truss,element_input_frame,boundary_input,load_input, GUID):  # GUID 입력이 필요한 사용자에 한해 사용
    nodeinformation, elementinformation, boundaryinformation, reaction_return, displacement_return = kgbstruct_2D(node_input,element_input_truss,element_input_frame,boundary_input,load_input)

    #GUID 메서드를 이용해 GUID속성을 추가해 줌
    ei = elementinformation
    for i in list(ei.keys()):
        ei[i].def_GUID(GUID[i])

    return nodeinformation, elementinformation, boundaryinformation, reaction_return, displacement_return



def anabunny\
(node_input,element_input_truss,element_input_frame,boundary_input,load_input, GUID, unbr_segment={}):
    import copy

    res = {} #load별 결과 수집 
    for loadtype in load_input.keys():
        nodeinformation = Node(node_input)

        elementinformation = Element_ElasticTruss(nodeinformation, element_input_truss)
        asdf = Element_ElasticBeamcolumn(nodeinformation, element_input_frame)
        elementinformation.update(asdf)

        # element에 입력받은 GUID 입력
        ei = elementinformation
        for i in list(ei.keys()):
            ei[i].def_GUID(GUID[i])
            ei[i].def_unbr_segment(unbr_segment.get(i))

        boundaryinformation = Fix(nodeinformation, boundary_input)
        solveobject = Buildreducedstiff(nodeinformation,elementinformation,boundaryinformation)# matrix생성

        oneload = load_input[loadtype]
        [loadmatrix, nodal_load, element_load] = Loads(nodeinformation, elementinformation, oneload)
        [reactions, displacement] = Repeatsolver(solveobject, loadmatrix) # matrix 해석

        [reaction_return, displacement_return] = arraythereturn(node_input, boundary_input, reactions, displacement)

        [nodeinformation, elementinformation, boundaryinformation, reaction_return, displacement_return]
        
        res[loadtype] = {'node':nodeinformation,'element': elementinformation,'boundary':boundaryinformation , 'reaction':reaction_return, 'displacement':displacement_return}


    return res


def save_revitresult(totalresult,foldername = 'HSD_frame_module_IO', runtime = ''):
    res_f = {}
    for frk in totalresult.keys():
        frm = totalresult[frk]

        res_l = {}
        for lt in frm.keys():
            oneset = frm[lt]  # load type 별 결과 한세트
            res_l[lt] = convert_result2json(oneset['node'], oneset['element'], oneset['boundary'], oneset['reaction'], oneset['displacement'])
        res_f[frk] = res_l

    # out put 정리구간 추가##################


    ########################################


    import os
    if not os.path.isdir(foldername):
        os.makedirs(foldername)


    import json
    with open(foldername+'/HSD_frame_result_json'+runtime+'.txt', 'w') as outfilevar:
        json.dump(res_f, outfilevar)