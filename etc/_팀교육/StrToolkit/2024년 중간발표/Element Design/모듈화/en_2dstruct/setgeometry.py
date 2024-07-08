import numpy as np
np.set_printoptions(precision=6, suppress=True)


# V3.000
# 모듈화 분리

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

    def def_unbr_segment(self,ubr):
    	self.unbr_segment = ubr

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

    def def_name(self, name_):
        self.name = name_
    
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
        Vy = -0.5 * wy * L 
        M_fem = -wy * L ** 2 /12 

        q_fem = np.array([-Fx/2, Vy, +M_fem, -Fx/2, Vy, -M_fem]) # local coordination

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
            Vy1 = -7/20 * wy * L
            Vy2 = -3/20 * wy * L
            M_fem1 = -1/20 * wy * L **2
            M_fem2 = -1/30 * wy * L **2

        elif location == 1: 
            Fx = wx * L * 0.5
            Vy1 = -3/20 * wy * L
            Vy2 = -7/20 * wy * L
            M_fem1 = -1/30 * wy * L **2
            M_fem2 = -1/20 * wy * L **2


        else: 
            print("error wrong value inputed")


        q_fem = np.array([-Fx/2, Vy1, +M_fem1, -Fx/2, Vy2, -M_fem2]) # local coordination
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
        Vy1 = -(3*a + b)*b**2 * py / L**3     - 6 * a * b * Mz / L**3
        Vy2 = -(3*b + a)*a**2 * py / L**3     - 6 * b * a * Mz / L**3
        M_fem1 = -py * a * b**2 / L**2       - (2*a-b) * b * Mz / L**2
        M_fem2 = -py * b * a**2 / L**2       - (2*b-a) * a * Mz / L**2

        q_fem = np.array([-Fx/2, Vy1, +M_fem1, -Fx/2, Vy2, -M_fem2]) # local coordination

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
