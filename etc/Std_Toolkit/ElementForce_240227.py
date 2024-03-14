import numpy as np
np.set_printoptions(precision=4, suppress=True)

# V1.000

# 2D frame 해석을 기반으로 고려하여, 하중의 방향은 부재 Local axis 기준 x y Mz 방향의 하중이 작용하는 경우에 대해서만 고려하였음.
# 3D frame 해석을 위해 확장하기 위해, 추후 외력입력시 방향 벡터값을 같이 받는 방식이 추가 되어야 한다. 
class ElementForce:
    def __init__(self, L, end_force, numberofdivide = 200):
        self.EF = end_force # 부재 단부에 작용하는 힘 [x1, y1, Mz1, x2, y2, Mz2]

        self.L = L #부재길이 
        self.nod = numberofdivide #number of devide -> index 0~ nod
        self.x = np.arange(0,self.nod+1) * L / self.nod # 부재를 201개로 분절. -> 모든 load 의 위치를 0.5%단위로 부재 길이 위에 있는 것으로 고려 
        self.P = [0 for i in range(0,len(self.x))]  # 축력 axial force
        self.V = [0 for i in range(0,len(self.x))]  # 전단력
        self.Mz = [0 for i in range(0,len(self.x))] # 휨 모멘트

        for i in range(0,len(self.x)):
          self.V[i] = end_force[1]

        for i in range(0,len(self.x)):
          self.Mz[i] = round(-end_force[2]+end_force[1]*self.x[i] ,3) # ef 5 더하는것 추가할것


    def FindNodeIndex(self,locations): # 위치정보를 받았을 때 x 의 index로 변환
        # 해당 class에서 알고리즘은 시작점. 끝점을 같이 확인할 수 있도록 디자인 함.
        node_index = [0]
        for i in range(0,len(locations)):
            node_index.append(round(locations[i] / self.L * self.nod))
        node_index.append(round(self.nod))

        return node_index



    def PointLoad(self, p, loading_point):  # 부재 point load 가 작용할 때 

        node_index = self.FindNodeIndex(loading_point)
        x = self.x
        # x 에 대한 수식으로 싸그리 다 정리하면 된다.

        for i in range(0,len(p)+1): # 구간 분할.

            
            # shear force calculation
            ext_force = 0 
            for j in range(0,i): # 전단력에 영향을 주는 외력의 합
                ext_force = ext_force + p[j]
            shear_f = 0 - ext_force   
            for j in range(node_index[i] , node_index[i+1]):
                self.V[j] = self.V[j]+shear_f
                
            # Bending moment calculation
            for j in range(node_index[i] , node_index[i+1]): # j= x의 인덱스
                
                for k in range(0,i):
                    M_i = 0 - p[k] * ( self.x[j] - self.x[node_index[k+1]])

                    self.Mz[j] = self.Mz[j] + M_i


        # 마지막 숫자 처리
        self.V[self.nod] = self.V[self.nod]+shear_f 

        for k in range(0,i):
            self.Mz[self.nod] = self.Mz[self.nod] - p[k] * (self.x[self.nod] - self.x[node_index[k+1]])




    def DistributionLoad(self,x1,x2,y1,y2):  # 하중의 시작점, 끝점, 시작점의 하중크기 끝점의 하중크기
        # 여러 등분포 하중을 처리할 수 있는 basic 형태 
        node_index = self.FindNodeIndex([x1, x2])
        x = self.x
        for i in range(node_index[1] , node_index[2]): # + 1 은 아래 후처리 만든후 삭제
            y = (y2-y1)/(x2-x1)*(x[i]-x1) + y1 
            sum_y = 0.5 * (y+y1) * (x[i]-x1)
            if y1>=y2:
                armlength = (x[i]-x1) /3 * (y + 2*y1)/(y1+y)
            else: 
                armlength = (x[i]-x1) /3 * (y*2 + y1)/(y1+y)
            
            self.V[i] = self.V[i] - sum_y
            self.Mz[i] = self.Mz[i] - sum_y*armlength

        for i in range(node_index[2] , node_index[3]+1):
            sum_y = 0.5 * (y2+y1) * (x2-x1)
            if y1>=y2:
                armlength = (x2-x1) /3 * (y2 + 2*y1)/(y1+y2)+ (x[i]-x2)
            else: 
                armlength = (x2-x1) /3 * (y2*2 + y1)/(y1+y2) + (x[i]-x2)

            self.V[i] = self.V[i] - sum_y
            self.Mz[i] = self.Mz[i] - sum_y*armlength


    def UniformBeamLoad(self,w): # beam 전체에 동일한 등분포 하중이 오는 경우
        self.DistributionLoad(0,self.L,w,w)



    def DrawShearForce(self):
        plt.plot(self.x, self.V,color='b')
        plt.fill_between(self.x[:], self.V[:], alpha=0.1)
        plt.plot([0,0],[0,self.V[0]],color='b')
        plt.plot([self.L,self.L],[0,self.V[self.nod]],color='b')
        plt.plot([0,self.L],[0,0],color='#000000')
        
        
        plt.title('SFD', size = 13)
        plt.xlim([-0.1,self.L+0.1]) # x축 범위
        # plt.ylim([-3,3]) # y축 범위
        plt.ylabel('kN') # 단위 입력 부분은 추후 구현 고려 
        plt.grid(True)

    def ShowShearForce(self): # 실제 사용자 사용 함수

        self.DrawShearForce()        
        plt.show()

    def DrawMoment(self):
        plt.plot(self.x, self.Mz,color='b')
        plt.fill_between(self.x[:], self.Mz[:], alpha=0.1)
        plt.plot([0,0],[0,self.Mz[0]],color='b')
        plt.plot([self.L,self.L],[0,self.Mz[self.nod]],color='b')
        plt.plot([0,self.L],[0,0],color='#000000')
        
        
        plt.title('BMD', size = 13)
        plt.xlim([-0.1,self.L+0.1]) # x축 범위
        # plt.ylim([-3,3]) # y축 범위
        plt.ylabel('kN-m') # 단위 입력 부분은 추후 고려
        plt.gca().invert_yaxis()
        plt.grid(True)

    def ShowMoment(self): # 실제 사용자 사용 함수

        self.DrawMoment()
        plt.show()


    def TotalPlot(self):
        plt.subplot(2,1,1)
        self.DrawShearForce()

        plt.subplot(2,1,2)
        self.DrawMoment()
        plt.show()





############################################################################################


import matplotlib.pyplot as plt


############################################################################################
# Example simple beam

p_amount = [1,1,1]
p_location = [2.5,5,7.5]

E1 = ElementForce(10, [0,1.5,0,0,1.5,0])
E1.PointLoad(p_amount,p_location)

# E1.ShowShearForce()
# E1.ShowMoment()
E1.TotalPlot()





# ############################################################################################
# # Example simple beam

# p_amount = [1,1]
# p_location = [5,10]

# E2 = ElementForce(10, [0,2,-15,0,0,0])
# E2.PointLoad(p_amount,p_location)


# E2.TotalPlot()


# ############################################################################################
# # Example simple beam


# E3 = ElementForce(10, [0,5,0,0,5,0])
# # E3.DistributionLoad(0,10,1,1)
# E3.UniformBeamLoad(1)

# E3.TotalPlot()


# E4 = ElementForce(10, [0,2.5,0,0,2.5,0])
# E4.DistributionLoad(2.5,7.5,1,1)

# E4.TotalPlot()