import numpy as np
np.set_printoptions(precision=4, suppress=True)

# V1.000

class Elements2D:
    def __init__(self, node1, node2):
        self.nodes = [node1, node2]
        self.node1 = node1
        self.node2 = node2
        self.x1 = node1.x
        self.x2 = node2.x
        self.y1 = node1.y
        self.y2 = node2.y
        self.length = ( (self.x2 - self.x1)**2 + (self.y2 - self.y1)**2 )**0.5
        self.element_force = [] #해석 결과 저장위치
        



    def Truss2D(self, A, E): # 동일하게 3x3 매트릭스가 되도록 행렬 수정하기 
        rx = (self.x2 - self.x1) / self.length #λx
        ry = (self.y2 - self.y1) / self.length #λy
        L = self.length 
        print("λx , λy", rx, ry)

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
        # T' k' T 메트릭스를 미리 풀어서 입력했음. (물론 예제가 미리 풀어줬음)

    def Frame2D(self,A,I,E):
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
        print("all dof : ",self.DOF_all)

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
    
            print(local_index+1)
            for i in range(0,len(local_index)):
                for j in range(0,len(local_index)):
                    global_matrix[local_index[i]][local_index[j]]=global_matrix[local_index[i]][local_index[j]]+local_k[i][j];
        self.total_matrix = global_matrix
        print(global_matrix)
        return global_matrix


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
        print(k)

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


        disp_free = force_free @ np.linalg.inv(self.free_stiffness) 
        print( disp_free ) 

        self.structure_displacement_free = disp_free # 자유 node의 displacement 만 저장
        
        disp = np.zeros(len(self.DOF_all))
        for i in range(0,len(disp_free)):
            disp[DOF_free[i]-1] = disp_free[i]

        self.structure_displacement_total = disp[:]

        print("disp",disp)
        force = self.total_matrix @ disp
        print( "all force", force)

        

        # 빈 reactio에 force 메트릭스에서 boundary에 해당하는 값 + P matrix에서 boundary에 해당하는 값 더하기 
        reaction = np.zeros(len(BDOF))
        for i in range(0,len(BDOF)):
            reaction[i] = force[BDOF[i]-1] - force_boundary[i]#부호결과 검증 할것


        print("reaction", reaction)


    def FindMemberElement(self):

        e_list = self.elements_dict
        for ie in e_list.keys():
            print("emelement No.", ie )            
            #Element 양 쪽 node 추출
            # node 별 자유도 정렬 -> element를 정의 할때 node 순서로 // node 1 2 순서로 매트릭스 생성 -> 부를때도 똑같음.
            temp_element_DOF = e_list[ie].node1.DOF + e_list[ie].node2.DOF
            print(temp_element_DOF)


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
            print('q',e_list[ie].element_force)



        
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

        print("P : ", self.p_matrix)
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
        M_fem = wy * L ** 2 /12 

        q_fem = np.array([-Fx/2, Vy, M_fem, -Fx/2, Vy, -M_fem])

        Q_fem = T_t @ q_fem

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

def Model(modelname):
    globals()[modelname] = Builder2D()

    pass


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
    

def Loads(nodeinformations,elementinformations,all_load_input):

    tempload_ = DefineLoad(nodeinformations, elementinformations)

    for one_load_ in all_load_input:

        if one_load_[0] == "joint":
            print("joint load")
            tempload_.JointLoad(*one_load_[1:])

        elif one_load_[0] =="uniform":
            print("uniform Beam load")
            tempload_.UniformBeamLoad(*one_load_[1:])

        else:
            print("미구현 load type")


    return tempload_
        
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
    Solve2.FindMemberElement()



# #########################running test###################################


############frame example#######################

print("\nex 16.1")
model_name = "ex_16_1"


# solve identifier 


nodeinformation = Node([
    [1,0,0],
    [2,20*12,0],
    [3,20*12,-20*12],
    ])


# #set element tag 

#define element properties 

elementinformation = Element_ElasticBeamcolumn(nodeinformation,
    [
    [1,1,2,10,500,29000],
    [2,2,3,10,500,29000],
    ])



print("length E1", elementinformation[1].length)
print("length E2", elementinformation[2].length)

print("k_E1= \n",elementinformation[1].k)
print("k_E2= \n",elementinformation[2].k)




#예제와 비교를 위한 정의
# x y Mz
nodeinformation[1].DefineDOF([4,6,5])
nodeinformation[2].DefineDOF([1,2,3])
nodeinformation[3].DefineDOF([7,8,9])


boundaryinformation = Fix(nodeinformation,
    [
    [1,0,1,0],
    [3,1,1,1],
    ])

print("boundaryinformation",boundaryinformation)
print(nodeinformation[1].boundary_DOF)
print(nodeinformation[3].boundary_DOF)



loadinformation = Loads(nodeinformation, elementinformation,
    [
    ["joint", 2, 5, 0 ,0],
    ["joint", 3, 0, 0 ,0],


    ])




Eleasticsolve(nodeinformation,elementinformation,boundaryinformation,loadinformation)




####################################################
print("/n ex simple beam with uniform load")


nodeinformation = Node([
    [1,0,0],
    [2,1000,0],
    
    ])


# #set element tag 

#define element properties 

elementinformation = Element_ElasticBeamcolumn(nodeinformation,
    [
    [1,1,2,100,5000,29000],
    ])


boundaryinformation = Fix(nodeinformation,
    [
    [1,1,1,1],
    [2,1,1,1],
    ])

loadinformation = Loads(nodeinformation, elementinformation,
    [
    ["uniform", 1, 0 ,1],
    
    ])

Eleasticsolve(nodeinformation,elementinformation,boundaryinformation,loadinformation)

import ElementForce_240227 as elf 

E1 = elf.ElementForce(elementinformation[1].length,elementinformation[1].element_force)
E1.UniformBeamLoad(1)
E1.TotalPlot()

