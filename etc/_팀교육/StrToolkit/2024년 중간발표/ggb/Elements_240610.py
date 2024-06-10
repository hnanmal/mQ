import numpy as np
np.set_printoptions(precision=6, suppress=True)

# V2.300
# 부재력을 return하는 기능 추가

class Elements2D:
    def __init__(self, node1, node2):
        self.nodes = [node1, node2]
        self.node1 = node1
        self.node2 = node2
        self.x1 = node1.x
        self.x2 = node2.x
        self.y1 = node1.y
        self.y2 = node2.y
        self.length = ((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2 )**0.5
        self.element_force = [] #해석 결과 저장위치

    def def_GUID(self, GUID_input_):
        self.GUID = GUID_input_


    def Truss2D(self, A, E): # 동일하게 3x3 매트릭스가 되도록 행렬 수정하기 
        self.element_type = "truss2D"
        rx = (self.x2 - self.x1) / self.length #λx
        ry = (self.y2 - self.y1) / self.length #λy
        L = self.length 
        # print("λx , λy", rx, ry)

        T = np.array([
            [rx,ry,0,0,0,0],
            [-ry,rx,0,0,0,0],
            [0,0,1,0,0,0],
            [0,0,0,rx,ry,0],
            [0,0,0,-ry,rx,0],
            [0,0,0,0,0,1]
            ])
        T_t = np.array([
            [rx,-ry,0,0,0,0],
            [ry,rx,0,0,0,0],
            [0,0,1,0,0,0],
            [0,0,0,rx,-ry,0],
            [0,0,0,ry,rx,0],
            [0,0,0,0,0,1]
            ]) #transvers of T matrix

        k_lc = np.array([
            [A*E/L,0,0,-A*E/L,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0],
            [-A*E/L,0,0,A*E/L,0,0],
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]
            ])


        self.k = T_t @ k_lc @ T
        self.k_lc = k_lc
        self.T = T
        self.T_t = T_t
        
        # print(self.k)

    def Frame2D(self,A,I,E):
        self.element_type = "frame2D"
        rx = (self.x2 - self.x1) / self.length #λx
        ry = (self.y2 - self.y1) / self.length #λy
        # print("λx , λy", rx, ry)
        L = self.length 

        T = np.array([
            [rx,ry,0,0,0,0],
            [-ry,rx,0,0,0,0],
            [0,0,1,0,0,0],
            [0,0,0,rx,ry,0],
            [0,0,0,-ry,rx,0],
            [0,0,0,0,0,1]
            ])
        T_t = np.array([
            [rx,-ry,0,0,0,0],
            [ry,rx,0,0,0,0],
            [0,0,1,0,0,0],
            [0,0,0,rx,-ry,0],
            [0,0,0,ry,rx,0],
            [0,0,0,0,0,1]
            ]) #transvers of T matrix

        k_lc = np.array([
            [A*E/L,0,0,-A*E/L,0,0],
            [0,12*E*I/L**3,6*E*I/L**2,0,-12*E*I/L**3,6*E*I/L**2],
            [0,6*E*I/L**2,4*E*I/L,0,-6*E*I/L**2,2*E*I/L],
            [-A*E/L,0,0,A*E/L,0,0],
            [0,-12*E*I/L**3,-6*E*I/L**2,0,12*E*I/L**3,-6*E*I/L**2],
            [0,6*E*I/L**2,2*E*I/L,0,-6*E*I/L**2,4*E*I/L]
            ])

        self.k = T_t @ k_lc @ T
        self.k_lc = k_lc
        self.T = T
        self.T_t = T_t

        # print(self.k)

        pass

    def PinFix(self,node1, node2):
        pass

    @classmethod
    def get_elements_list(cls):
        return cls.elements_list


class Nodes:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.DOF = [] # Node 별 자유도 
        self.boundary_DOF = []
    
    def DefineDOF(self,degree_of_freedom):
        self.DOF = degree_of_freedom
        pass #노드별 자유도값 가지게 하기

    def mass(self):
        pass

    def fix(self,x,y,Mz=0):
        
        if x == 1: 
            self.boundary_DOF = list(list(self.boundary_DOF) + [self.DOF[0]])
        if y == 1: 
            self.boundary_DOF = list(list(self.boundary_DOF) + [self.DOF[1]])
        if Mz == 1:
            self.boundary_DOF = list(list(self.boundary_DOF) + [self.DOF[2]])



    @classmethod 
    def get_nodes_list(cls):
        return cls.nodes_list




class ElasticSolver:
    def __init__(self,nodeinformations,elementinformations,boundaryinformations,loadinformations): 
        # 아래 리스트의 값은 각자 클래스명으로 활용 가능. ex) nodes_list_from_class[1].x
        self.nodes_dict = nodeinformations
        self.elements_dict = elementinformations

        self.nodes_list_from_class = nodeinformations.values()
        self.elements_list_from_class = elementinformations.values()
        self.DOF_all = [];
        for i in nodeinformations.keys():
            self.DOF_all = self.DOF_all + nodeinformations[i].DOF
        self.DOF_all.sort()
        self.p_matrix = np.zeros( len(self.DOF_all))
        # print("all dof : ",self.DOF_all)

        self.loads = loadinformations

        self.BDOF = []
        for i in boundaryinformations.keys():
            self.BDOF = self.BDOF + nodeinformations[i].boundary_DOF[:]


    def Build_Matrix(self, DOF_per_node=3): # DOF per node 입력 없이, truss matrix 수정후 수정
        nodes = list(self.nodes_list_from_class)
        elements = list(self.elements_list_from_class)

        total_DOF = len(nodes) * DOF_per_node # 이부분은 해석 모델 특성에 따라 변하도록 확장 할것 
        global_matrix = np.zeros([total_DOF,total_DOF])
    
        for i_el in range(0,len(elements)):
            local_k = elements[i_el].k   
            local_index = np.array(elements[i_el].node1.DOF + elements[i_el].node2.DOF)-1
            # element 별로 가진 index 정리. -1 을 한 이유는 자유도 시작번호 1 list index 시작번호 0 매치 위함
    
            
            for i in range(0,len(local_index)):
                for j in range(0,len(local_index)):
                    global_matrix[local_index[i]][local_index[j]]=global_matrix[local_index[i]][local_index[j]]+local_k[i][j];
        self.total_matrix = global_matrix
        # print(global_matrix)

        
        return global_matrix

    def killmatrix(self,matrix_):

        killedindex=[]
        for i in range(0,len(matrix_)):
            if np.all(matrix_[i][:] == 0):
                killedindex.append(i)


        i = 0
        while np.linalg.det(matrix_) == 0:
            if np.all(matrix_[i][:] == 0): 
                matrix_ = np.delete(matrix_, i , axis = 0)
                matrix_ = np.delete(matrix_, i , axis = 1)
            else: 
                i += 1

        return [matrix_, killedindex]



    def ReduceMatrix(self):
        BDOF = self.BDOF

        DOF_free = list(self.DOF_all)
        for i in range(0,len(BDOF)):
            DOF_free.remove(BDOF[i])

        # print("Free DOF : ",DOF_free)
        



        #변위 산출 매트릭스
        k = np.zeros([len(DOF_free),len(DOF_free)])
        for i in range(0,len(DOF_free)):
            for j in range(0,len(DOF_free)):
                k[i][j] = self.total_matrix[DOF_free[i]-1][DOF_free[j]-1]
        self.free_stiffness = k
        # print(k)

        #반력 산출 매트릭스
        k = np.zeros([len(BDOF),len(BDOF)])
        for i in range(0,len(BDOF)):
            for j in range(0,len(BDOF)):
                k[i][j] = self.total_matrix[BDOF[i]-1][BDOF[j]-1]
        self.fix_stiffness = k
        # print(k)

        

    def SolveStructure(self):

        BDOF = self.BDOF

        DOF_free = list(self.DOF_all)
        for i in range(0,len(BDOF)):
            DOF_free.remove(BDOF[i])
        
        force_free = np.zeros(len(DOF_free))
        for i in range(0,len(force_free)):
            force_free[i] = self.loads.p_matrix[DOF_free[i]-1]

        force_boundary = np.zeros(len(BDOF))
        for i in range(0,len(BDOF)):
            force_boundary[i] = self.loads.p_matrix[BDOF[i]-1]

        # kill 
        [free_stiffness_modified, killed_index] = self.killmatrix(self.free_stiffness)

        force_free = np.delete(force_free, killed_index , axis = 0)  # force도 삭제 


        #역함수 계산
        disp_free = force_free @ np.linalg.inv(free_stiffness_modified) 

        # free disp에서 삭제된 부분에 0으로 정의 (트러스만 있는 node는 회전하지 않았음.)
        disp_free = list(disp_free)
        for i in killed_index:
            disp_free = disp_free[:i] + [0] + disp_free[i:] # np.r_[a, b] 대신 python list 합치는 문법을 차용
        disp_free = np.array(disp_free)
        # print( disp_free ) 



        self.structure_displacement_free = disp_free # 자유 node의 displacement 만 저장
        
        disp = np.zeros(len(self.DOF_all))
        for i in range(0,len(disp_free)):
            disp[DOF_free[i]-1] = disp_free[i]

        self.structure_displacement_total = disp[:]

        # print("disp",disp)
        force = self.total_matrix @ disp
        self.force = force
        # print( "all force", force)

        

        # 빈 reactio에 force 메트릭스에서 boundary에 해당하는 값 + P matrix에서 boundary에 해당하는 값 더하기 
        reaction = np.zeros(len(BDOF))
        for i in range(0,len(BDOF)):
            reaction[i] = force[BDOF[i]-1] - force_boundary[i]#부호결과 검증 할것

        self.reaction = reaction # return 값 
        # print("reaction", reaction)


    def FindMemberForce(self):

        e_list = self.elements_dict
        for ie in e_list.keys():
            #Element 양 쪽 node 추출
            # node 별 자유도 정렬 -> element를 정의 할때 node 순서로 // node 1 2 순서로 매트릭스 생성 -> 부를때도 똑같음.
            temp_element_DOF = e_list[ie].node1.DOF + e_list[ie].node2.DOF
            

            # 자유도에 해당하는 변위값 추출, -> element_disp
            # 해당 element의 T matrix 불러오기 
            # q = 부재력  k_e = element.k   T = element.T-> Tmatrix 객체값으로 정의 할것  D=추출된 변위 값 
            D = np.zeros(len(temp_element_DOF))
            for i in range(len(temp_element_DOF)):
                D[i] = self.structure_displacement_total[temp_element_DOF[i]-1]
            k_e = e_list[ie].k_lc
            T = e_list[ie].T

            q = k_e @ (T @ D) + self.loads.q_fem[ie]

            e_list[ie].element_force = q 

            # print("k_e",k_e)
            # print("T",T)
            # print("D",D)
            # print("d",T @ D)
            # print('q',e_list[ie].element_force)



        
        pass


class DefineLoad:
    def __init__(self,nodeinformations,elementinformations): 
        self.DOF_all = [];
        for i in nodeinformations.keys():
            self.DOF_all = self.DOF_all + nodeinformations[i].DOF
        self.DOF_all.sort()
        self.p_matrix = np.zeros( len(self.DOF_all))

        self.node_dict = nodeinformations
        self.element_dict = elementinformations

        self.q_fem = {}
        for i in elementinformations.keys():
            self.q_fem[i] = np.zeros(6)
        

    def JointLoad(self,node_number,x,y,Mz):
        
        DOF_of_node = self.node_dict[node_number].DOF
        #node 의 dof와 일치하는 P matrix의 위치에 하중 입력 
        if x != 0: 
            self.p_matrix[DOF_of_node[0]-1] = self.p_matrix[DOF_of_node[0]-1] + x # 
        if y != 0: 
            self.p_matrix[DOF_of_node[1]-1] = self.p_matrix[DOF_of_node[1]-1] + y
        if Mz != 0: 
            self.p_matrix[DOF_of_node[2]-1] = self.p_matrix[DOF_of_node[2]-1] + Mz

        # print("P : ", self.p_matrix)
        pass

    def UniformBeamLoad(self,element_name,wx,wy):  #2D frame 해석이므로 부재 Local axis 기준 축에 축력과 수직한 방향 하중만 받음

        element = self.element_dict[element_name]
        node1 = element.node1
        node2 = element.node2 

        L = element.length
        T = element.T 
        T_t = element.T_t

        Fx = wx * L # sum of axial force 
        Vy = 0.5 * wy * L 
        M_fem = -wy * L ** 2 /12 

        q_fem = np.array([-Fx/2, Vy, -M_fem, -Fx/2, Vy, M_fem]) # local coordination

        Q_fem = T_t @ q_fem # Global coordination

        self.Superposition(element_name, node1, node2, Q_fem, q_fem)

    def TriangleBeamLoad(self,element_name, wx,wy, location): 
        #location 0 : load max - member start  location 1 : load max - member end
        #사다리꼴 보편식을 계산한게 아니라 공식 입력해서 만든것이므로 응용력이 낮음 
        element = self.element_dict[element_name]
        node1 = element.node1
        node2 = element.node2 

        L = element.length
        T = element.T 
        T_t = element.T_t

        if location == 0: 
            Fx = wx * L * 0.5
            Vy1 = 7/20 * wy * L
            Vy2 = 3/20 * wy * L
            M_fem1 = -1/20 * wy * L **2
            M_fem2 = -1/30 * wy * L **2

        elif location == 1: 
            Fx = wx * L * 0.5
            Vy1 = 3/20 * wy * L
            Vy2 = 7/20 * wy * L
            M_fem1 = -1/30 * wy * L **2
            M_fem2 = -1/20 * wy * L **2


        else: 
            print("error wrong value inputed")


        q_fem = np.array([-Fx/2, Vy1, -M_fem1, -Fx/2, Vy2, M_fem2]) # local coordination
        Q_fem = T_t @ q_fem # Global coordination

        self.Superposition(element_name, node1, node2, Q_fem, q_fem)



    def PointLoad_local(self, element_name, px, py, Mz, a): 
        # element_name,
        # px, py  부재 Local 축 기준 x, y 방향 힘   -> Global 축 기준으로 하중 받는 기능 추가 필요
        # a 부재 시작점에서 a 만큼 떨어진 거리  0 < a < L 

        element = self.element_dict[element_name]
        node1 = element.node1
        node2 = element.node2 

        L = element.length
        T = element.T 
        T_t = element.T_t

        b = L - a  # 하중점에서 부재 끝단까지 거리

        Fx = px # sum of axial force 
        Vy1 = (3*a + b)*b**2 * py / L**3     + 6 * a * b * Mz / L**3
        Vy2 = (3*b + a)*a**2 * py / L**3     + 6 * b * a * Mz / L**3
        M_fem1 = -py * a * b**2 / L**2       - (2*a-b) * b * Mz / L**2
        M_fem2 = -py * b * a**2 / L**2       - (2*b-a) * a * Mz / L**2

        q_fem = np.array([-Fx/2, Vy1, -M_fem1, -Fx/2, Vy2, M_fem2]) # local coordination

        Q_fem = T_t @ q_fem # Global coordination

        self.Superposition(element_name, node1, node2, Q_fem, q_fem)


    def Superposition(self,element_name, node1, node2, Q_fem, q_fem):

        self.p_matrix[node1.DOF[0]-1] = self.p_matrix[node1.DOF[0]-1] - Q_fem[0]
        self.p_matrix[node2.DOF[0]-1] = self.p_matrix[node2.DOF[0]-1] - Q_fem[3]

        self.p_matrix[node1.DOF[1]-1] = self.p_matrix[node1.DOF[1]-1] - Q_fem[1]
        self.p_matrix[node2.DOF[1]-1] = self.p_matrix[node2.DOF[1]-1] - Q_fem[4]

        self.p_matrix[node1.DOF[2]-1] = self.p_matrix[node1.DOF[2]-1] - Q_fem[2]
        self.p_matrix[node2.DOF[2]-1] = self.p_matrix[node2.DOF[2]-1] - Q_fem[5]

        self.q_fem[element_name] = self.q_fem[element_name] + q_fem

        pass


class Builder2D:
    def __init__(self):
        self.elements_list = []
        self.nodes_list = []

################################ 클래스 실행을 위한 함수##################################
################################ = 사용자 명령어 인터페이스##################################

def Node(_inputdatalist): 
    
    result_ = {}
    for one_node_ in _inputdatalist:
        tag_ = one_node_[0]
        x_ = one_node_[1]
        y_ = one_node_[2]

        temp_ = Nodes(x_,y_)

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



def Showelementforce(element_number_ ,elementinformation_, element_load_,showoption=0):
    # show option을 1로 놓으면 그래프 띄우도록 설정
    import ElementForce_240227 as elf 
    
    efef = [elementinformation_[element_number_].element_force[0],
    elementinformation_[element_number_].element_force[1],
    -elementinformation_[element_number_].element_force[2], # 매트릭스 해석 회전의 양의 방향과 부재력의 회전 양의 방향 다름
    elementinformation_[element_number_].element_force[3:],]
    
    # element force 중에서 해당 element 번호만 찾기
    elementforcedmember = [i[1] for i in element_load_]
    elementindex = [i for i, ele in enumerate(elementforcedmember) if ele == element_number_]


    # 그래프 모듈 
    E1 = elf.ElementForce(elementinformation[element_number_].length,efef)
    for i in elementindex: # Principle of superposition원리 작성.
        if element_load_[i][0] == "uniform":
            E1.UniformBeamLoad(element_load_[i][3])

        elif element_load_[i][0] == "beampoint":
            E1.PointLoad([element_load_[i][3]],[element_load_[i][4]], [element_load_[i][5]])

        else:
            print('No element force')

    if showoption ==1: 
        E1.TotalPlot()

    return {element_number_:[E1.x, E1.V, E1.Mz]}
    ###




# #########################running test###################################

#########################################################################
print("\nex 117")

node_input = [
[1,0,0],
[2,5,0],
[3,-3,-3],
[4,1.732,-3],
]
Es = 210000  #Mpa
A1 = 25 * 100  # mm2
Ix = 4 * 10000 * 10000 # mm2

element_input_frame = [
[1,1,2,A1,Ix,Es],
]
element_input_truss = [
[2,3,1 ,A1,Es],
[3,4,1 ,A1,Es],
]

boundary_input = [
[4,1,1,0],
[2,1,1,0],
[3,1,1,0],
]

load_input = [
["beamtriangle", 1, 0, -30000 ,0],
]




### 실행을 위한 함수 
def kgbstruct_2D(node_input,element_input_truss,element_input_frame,boundary_input,load_input):  # truss input과 beamcolumninput 구분
    nodeinformation = Node(node_input)

    elementinformation = Element_ElasticTruss(nodeinformation, element_input_truss)
    asdf = Element_ElasticBeamcolumn(nodeinformation, element_input_frame)
    elementinformation.update(asdf)

    boundaryinformation = Fix(nodeinformation, boundary_input)
    [loadmatrix, nodal_load, element_load] = Loads(nodeinformation, elementinformation,load_input)
    [reactions, displacement]= Eleasticsolve(nodeinformation,elementinformation,boundaryinformation,loadmatrix)

    # reaction은 boundary information 에 입력한 순서대로, 고정단에 대하여 차례로 출력됨. 
    #node별 reaction이 어떻게 나오는지 x y Mz 순서로 정리
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




    return nodeinformation, elementinformation, boundaryinformation, reaction_return, displacement_return


[nodeinformation, elementinformation, boundaryinformation, reactions, displacement] = kgbstruct_2D(node_input,element_input_truss,element_input_frame,boundary_input,load_input)

print("reactions",reactions)
print("displacement", displacement)
print("element force check", elementinformation[1].element_force)
# see result 같은 함수를 작성하여 진행?


####################################################
print("\n ex simple beam with point load")

node_input = [
[1,0,0],
[2,10,0],
]



element_input_frame = [
["1",1,2,100,5000,29000],
]
element_input_truss = [
] # 업으면 없는데로 빈칸으로 두기
boundary_input = [
[1,1,1,1],
[2,1,1,1],
]

load_input = [
["beampoint", "1", 0, 1, 0, 5],
]

[nodeinformation, elementinformation, boundaryinformation, reactions, displacement] = kgbstruct_2D(node_input,element_input_truss,element_input_frame,boundary_input,load_input)

print("node informaiton",nodeinformation)
print("boundary informaiton",boundaryinformation)
print("reactions",reactions)
print("displacement", displacement)
print("element force check", elementinformation)
print("element length", elementinformation["1"].length)


eeeeee1=Showelementforce("1",elementinformation,load_input,1) # element 의 위치별 전단력, moment 값 출력
print("element 1 force",eeeeee1)


# line = '3 3 3    3 '
# print(str(line.strip()).split())

# story_array = list(map(lambda x:3,range(0,3)))
# print(story_array) (⊙⊙)
print(eeeeee1)