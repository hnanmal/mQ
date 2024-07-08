import numpy as np
np.set_printoptions(precision=6, suppress=True)
from .setgeometry import *

# V3.000
# 모듈화 분리


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