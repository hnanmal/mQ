import numpy as np
np.set_printoptions(precision=6, suppress=True)
from .setgeometry import *
from .solvestructure import *


# V3.000
# 모듈화 분리


################################ 클래스 실행을 위한 함수##################################
################################ = 사용자 명령어 인터페이스##################################

def Node(_inputdatalist): 
    
    result_ = {}
    for one_node_ in _inputdatalist:
        tag_ = one_node_[0]
        x_ = one_node_[1]
        y_ = one_node_[2]

        temp_ = Nodes(x_,y_)
        temp_.def_name(tag_)

        result_[tag_] = temp_

        number_of_nodes = len(result_.keys())
        temp_.DOF = [number_of_nodes*3-2,number_of_nodes*3-1,number_of_nodes*3] # Node 별 자유도 자동배치 
        # 전체 노드 갯수 확인하는 부분이 class밖으로 나옴에 따라 일단 밖에서 정의하도록 고쳐둠

    return result_



def Element_ElasticBeamcolumn(nodeinformation, _inputdatalist):
    # _inputdatalist = [elementnumber, node1, node2, A, I, E]

    result_ = {}
    for one_element_ in _inputdatalist:
        tag_ = one_element_[0]

        nodenumber1 = one_element_[1]
        nodenumber2 = one_element_[2]

        temp_ = Elements2D(nodeinformation[nodenumber1],nodeinformation[nodenumber2])
        temp_.Frame2D(*one_element_[3:6])
        
        result_[tag_] = temp_ 

    return result_
    
def Element_ElasticTruss(nodeinformation, _inputdatalist):
    # _inputdatalist = [elementnumber, node1, node2, A, E]

    result_ = {}
    for one_element_ in _inputdatalist:
        tag_ = one_element_[0]

        nodenumber1 = one_element_[1]
        nodenumber2 = one_element_[2]

        temp_ = Elements2D(nodeinformation[nodenumber1],nodeinformation[nodenumber2])
        temp_.Truss2D(*one_element_[3:5])
        
        result_[tag_] = temp_ 

    return result_


def Loads(nodeinformations,elementinformations,all_load_input):

    # 입력가능한 load type 
    # "joint"     / ["joint", joint number, Fx, Fy , Mz], global coordinate
    # "uniform"   / ["uniform", element number, wx , wy], member local coordinate
    # "beampoint" / ["beampoint", element number, px, py, Mz, location of load from member start], member local coordinate
    # "beamtriangle"/ ["beamtriangle", element number, wx , wy, start=0 / end=1 ]


    tempload_ = DefineLoad(nodeinformations, elementinformations) # load matrix 객체

    nodal_load_ = []
    element_load_ = []

    for one_load_ in all_load_input:

        if one_load_[0] == "joint":
            # print("joint load")
            tempload_.JointLoad(*one_load_[1:])
            nodal_load_.append(one_load_[1:])

        elif one_load_[0] =="uniform":
            # print("uniform Beam load")
            tempload_.UniformBeamLoad(*one_load_[1:])
            element_load_.append(one_load_[0:])

        elif one_load_[0] =="beampoint":
            # print("Beam point load")
            tempload_.PointLoad_local(*one_load_[1:]) # element_name, px, py, a
            element_load_.append(one_load_[0:])

        elif one_load_[0] =="beamtriangle":
            tempload_.TriangleBeamLoad(*one_load_[1:]) # element_name, px, py, a
            element_load_.append(one_load_[0:])

        else:
            print("미구현 load type")


    return [tempload_, nodal_load_, element_load_]
        
    pass

def Fix(nodeinformations,all_bdry_input): #bdry BounDRY
    
    result_ = {}
    for one_bdry_ in all_bdry_input:
        tempnode_ = nodeinformations[one_bdry_[0]]
        tempnode_.fix(*one_bdry_[1:])

        result_[one_bdry_[0]] = one_bdry_[1:]

    return result_



def Eleasticsolve(nodeinformation,elementinformation,boundaryinformation,loadinformation):

    Solve2 = ElasticSolver(nodeinformation,elementinformation,boundaryinformation,loadinformation)

    grobal_K = Solve2.Build_Matrix(3)
    
    Solve2.ReduceMatrix()
    Solve2.SolveStructure()
    Solve2.FindMemberForce()


    return [Solve2.reaction, Solve2.structure_displacement_total]

#
def Buildreducedstiff(nodeinformation,elementinformation,boundaryinformation):
    # geometry 정보만 받아서 reduce matrix 까지 만든 전체 구조물 객체를 반환
    # load만 바꿔 solve 하는 함수와 연계하여 사용 
    # load가 비었으므로 빈칸으로 입력
    Solve2 = ElasticSolver(nodeinformation,elementinformation,boundaryinformation,[])

    Solve2.Build_Matrix(3)
    Solve2.ReduceMatrix()
    return Solve2

def Repeatsolver(solverobject, loadinformation):
    #self.loads = loadinformations in ElasticSolver
    solverobject.loads = loadinformation

    solverobject.SolveStructure()
    solverobject.FindMemberForce()

    return [solverobject.reaction, solverobject.structure_displacement_total]
#

def Showelementforce(element_number_, elementinformation_, element_load_,showoption=0):
    # show option을 1로 놓으면 그래프 띄우도록 설정
    # 확인하고싶은 부재 번호 , elementinformation 객체 세트, load input 객체, 그래프 출력여부 
    from .ElementForce_240621 import ElementForce 
    
    endforce = [elementinformation_[element_number_].element_force[0],
    elementinformation_[element_number_].element_force[1],
    -elementinformation_[element_number_].element_force[2], # 매트릭스 해석 회전의 양의 방향과 부재력의 회전 양의 방향 다름
    elementinformation_[element_number_].element_force[3:],]
    
    # element force 중에서 해당 element 번호만 찾기
    elementforcedmember = [i[1] for i in element_load_]
    elementindex = [i for i, ele in enumerate(elementforcedmember) if ele == element_number_]


    # 부재력 모듈 객체 정의
    E1 = ElementForce(elementinformation_[element_number_].length,endforce)
    for i in elementindex: # Principle of superposition원리 작성.
        if element_load_[i][0] == "uniform":
            E1.UniformBeamLoad(element_load_[i][2],element_load_[i][3])

        elif element_load_[i][0] == "beampoint":
            E1.PointLoad([element_load_[i][2]],[element_load_[i][3]],[element_load_[i][4]], [element_load_[i][5]])

        else:
            print('No element force')

    if showoption ==1: 
        E1.TotalPlot()

    return {element_number_:{'x':list(E1.x), 'P':list(E1.P), 'V':list(E1.V), 'Mz':list(E1.Mz)}}
    ###


def arraythereturn(node_input, boundary_input, reactions, displacement):
    # reaction은 boundary information 에 입력한 순서대로, 고정단에 대하여 차례로 출력됨. 
    # node별 reaction이 어떻게 나오는지 x y Mz 순서로 정리
    # 자유단에 대해서는 0을 넣도록 짜서, x y mz 순서로 값이 항상 보이도록 정의
    # reaction.keys() 로부터 지점을 전부 소팅할 수 있게됨
    reaction_return = {}
    r_idx = 0
    for i in boundary_input:
        rl = i[1:]
        res = []
        for j in rl:
            if j == 1:
                res.append(reactions[r_idx])
                r_idx = r_idx + 1
            else: 
                res.append(0)

        reaction_return[i[0]] = res

    # 모든 node에 대한 변위를 dict 타입으로 정리 
    displacement_return = {}
    d_idx = 0
    for i in node_input:
        displacement_return[i[0]] = displacement[d_idx*3:d_idx*3+3]
        d_idx = d_idx + 1

    return [reaction_return, displacement_return]



def convert_result2json(nodeinformation, elementinformation, boundaryinformation, reactions, displacement):
    # node, boundary 정보처리
    noderesult = {}
    for i in nodeinformation.keys():
        # print(i)
        node = nodeinformation[i]
        
        if node.boundary_DOF == []:
            boundary = {}
        else:
            boundary = boundaryinformation[i]

        noderesult[i] ={'coordinate': [node.x, node.y], 'boundary': boundary}
    

    #displace 정보 처리 -> node 결과에 입력
    for i in displacement.keys():
        disp = displacement[i]
        noderesult[i].update({"displacement":list(disp)})

    #reaction 정보처리 -> node 결과에 반력 입력
    for i in reactions.keys():
        reac = reactions[i]
        noderesult[i].update({"reaction":list(reac)})


    # element 정보 처리
    elementresult = {}
    for i in elementinformation.keys():
        el = elementinformation[i]
        # print(el.node2.name) # start end node 번호 저장법 고민좀..

        elementresult[i] = {'element_force':list(el.element_force), 
        'startnode':el.node1.name, 
        'endnode':el.node2.name,
        'length':el.length,
        'guid':el.GUID,
        'unbr_segment':el.unbr_segment}

    # print(noderesult.keys())
    # print(noderesult['1000101'].get('displacement'))

    return {"node":noderesult, "element":elementresult}