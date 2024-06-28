from pandas import DataFrame
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import interp1d
from scipy import interpolate
import numpy as np

Kd = 0.85 # direcionality factor in ASCE 7
V = 58.11 # basic wind speed in ASCE 7
exp = 'Exposure C' #Exposure Class B, C, D
h = 9.906 #mean roof height in m 
B = 12.19 #Building Dimension normal to wind
L = 9.14 #Building Dimension parallel to wind
beta = 0.05 #Damping ratio
Type = 'ECL' # 'ECL' for Enclosed Building / 'PECL' for Partially Enclosed Building
theta =  15 # Roof Angle in Degree
n=4 #Dividing Numbers for Building Elevation, >=1 
BldgH = 7.62 #Building Height in meter (h: mean roof height와 다른 것)

Topographic_data = 'N' # 'Y' for available data exists, otherwise, 'N'
Lh =  60 # distance upwind of crest to where the difference in ground elevation in half the height of hill
H_hill = 187 # height of hill
x = 253 # distance from the crest to the building site
topho = '2Dridges' #'2Dridges', '2Descarpments', '3Daxisymmetric'
UD = 'Up' #'Up' / 'Down' for Upwind & Downwind of Crest, respectively

ewa = 'EWA2' # effective wind area 'EWA1', 'EWA2', 'EWA3' for <=a^2, a^2<&<=4a^2, >4a^2, respectively 
a = max(min(B*0.1, L*0.1, 0.4*h), 0.04*min(B,L), 0.9)

def Steel(h):
    na=22.2/h**0.8
    return na

def Concrete(h):
    na=43.5/h**0.9
    return na

def Other(h):
    na=75/h
    return na

H = h/0.305 #mean roof height in ft
n1 = round(Steel (H), 4) # 'Steel' / 'Concrete'  / 'Other' / ASCE 7-10 ss26.9.3 / Fundamental Frequency
print("Fundamental Frequency = ", n1)

DB = {
    "Exposure B": {
        "c": 0.3,
        "l": 97.54,
        "epsilon": 1/3,
        "alpha_bar":1/4,
        "b":0.45,
        "z_min":9.14,
        "z_g":365.76,
        "alpha": 7.0
    },
    "Exposure C": {
        "c": 0.2,
        "l": 152.4,
        "epsilon": 1/5,
        "alpha_bar":1/6.5,
        "b":0.65,
        "z_min":4.57,
        "z_g":274.32,
        "alpha":9.5
    },
    "Exposure D": {
        "c": 0.15,
        "l": 198.12,
        "epsilon": 1/8,
        "alpha_bar":1/9.0,
        "b":0.8,
        "z_min":2.13,
        "z_g":213.36,
        "alpha":11.5
    },
}

z_bar = max(h*0.6,DB[(exp)]['z_min']) #ASCE 7-10 ss26.9.4
gq = 3.4 #ASCE 7-10 ss26.9.4
gv = 3.4 #ASCE 7-10 ss26.9.4

Lz = DB[(exp)]['l']*(z_bar/10)**(DB[(exp)]['epsilon']) #ASCE 7-10 eq26.9-9
Q = (1/(1+0.63*((B+h)/Lz)**0.63))**0.5 #ASCE 7-10 eq26.9-8
Q_1 = (1/(1+0.63*((L+h)/Lz)**0.63))**0.5 #ASCE 7-10 eq26.9-8
Vz = DB[(exp)]['b']*(z_bar/10)**(DB[(exp)]['alpha_bar'])*V #ASCE 7-10 eq26.9-16
N1 = n1*Lz/Vz
Rn = 7.47*N1/((1+10.3*N1)**(5/3))
eta1 = 4.6*n1*h/Vz
eta2 = 4.6*n1*B/Vz
eta2_1 = 4.6*n1*L/Vz
eta3 = 15.4*n1*L/Vz
eta3_1 = 15.4*n1*B/Vz
e = 2.718281828459045
Rh = 1/eta1-1/(2*eta1**2)*(1-e**(-2*eta1))
RB = 1/eta2-1/(2*eta2**2)*(1-e**(-2*eta2))
RB_1 = 1/eta2_1-1/(2*eta2_1**2)*(1-e**(-2*eta2_1))
RL = 1/eta3-1/(2*eta3**2)*(1-e**(-2*eta3))
RL_1 = 1/eta3_1-1/(2*eta3_1**2)*(1-e**(-2*eta3_1))
R = (1/beta*Rn*Rh*RB*(0.53+0.479*RL))**0.5
R_1 = (1/beta*Rn*Rh*RB_1*(0.53+0.479*RL_1))**0.5
Iz = DB[(exp)]['c']*(10/z_bar)**(1/6)
gR =(2*np.log(3600*n1))**0.5+0.577/(2*np.log((3600*n1))**0.5)

if n1>=1:
    G = 0.925*((1+1.7*gq*Iz*Q)/(1+1.7*gv*Iz))
else:
    G = 0.925*((1+1.7*Iz*(gq**2*Q**2+gR**2*R**2)**0.5)/(1+1.7*gv*Iz))

if n1>=1:
    G_1 = 0.925*((1+1.7*gq*Iz*Q_1)/(1+1.7*gv*Iz))
else:
    G_1 = 0.925*((1+1.7*Iz*(gq**2*Q_1**2+gR**2*R_1**2)**0.5)/(1+1.7*gv*Iz))

print("G = ", round(G, 4))
print("G_1 = ", round(G_1, 4))

def CP(hL, ang, cp):
    db = []
    for i in range(len(hL)):
        for j in range(len(ang)):
            k = [hL[i],ang[j],cp[j]]
            db.append(k)
    return db

def CPdata(ang, hL1, cp1, hL2, cp2, hL3, cp3):
    DB1 = DataFrame(CP(hL1, ang, cp1))
    DB2 = DataFrame(CP(hL2, ang, cp2))
    DB3 = DataFrame(CP(hL3, ang, cp3))
    DB = pd.concat([DB1, DB2,DB3], ignore_index=True)
    DB.columns = ['hOverL', 'Angle', 'Cp']
    return DB

def Interpolation(hOverLNew, AngleNew):
    DBDB = CPdata(angle, hOverL1, cp1, hOverL2, cp2, hOverL3, cp3)
    f = LinearNDInterpolator(list(zip(DBDB['hOverL'], DBDB['Angle'])), DBDB['Cp'])
    Cp1 = f(hOverLNew, AngleNew)
    return Cp1

angle = [1, 9, 10, 15, 20, 25, 30, 35, 45, 60]
hOverL1 = [0.0, 0.1, 0.2, 0.25]
cp1 = [-0.9, -0.9, -0.7, -0.5, -0.3, -0.2, -0.2, 0.0, 0.0, 0.0]
hOverL2 = [0.50]
cp2 = [-0.9, -0.9, -0.9, -0.7, -0.4, -0.3, -0.2, -0.2, 0.0, 0.0]
hOverL3 = [1, 2, 10, 15, 20]
cp3 = [-1.3, -1.3, -1.3, -1.0, -0.7, -0.5, -0.3, -0.2, 0.0, 0.0]

CP1 = Interpolation (h/L, theta)
print ("CP1 = ", Interpolation (h/L, theta))

hOverL1 = [0.0, 0.1, 0.2, 0.25]
angle = [1, 9, 10, 15, 20, 25, 30, 35, 45, 60]
cp1 = [-0.18, -0.18, -0.18, 0.0, 0.2, 0.3, 0.3, 0.4, 0.4, 0.6]
hOverL2 = [0.50]
cp2 = [-0.18, -0.18, -0.18, -0.18, 0.0, 0.2, 0.2, 0.3, 0.4, 0.6]
hOverL3 = [1.0, 2.0, 10.0, 15.0, 20.0]
cp3 = [-0.18, -0.18, -0.18, -0.18, -0.18, 0.0, 0.2, 0.2, 0.3, 0.6]

def Interpolation(hOverLNew, AngleNew):
    DBDB = CPdata(angle, hOverL1, cp1, hOverL2, cp2, hOverL3, cp3)
    f = LinearNDInterpolator(list(zip(DBDB['hOverL'], DBDB['Angle'])), DBDB['Cp'])
    Cp1 = f(hOverLNew, AngleNew)
    return Cp1

CP2 = Interpolation (h/L, theta)
print ("CP2 =", Interpolation (h/L, theta))

hOverL1 = [0.0, 0.1, 0.2, 0.25]
angle = [1, 9, 10, 12.5, 15, 17.5, 20, 25, 30, 35, 45, 60]
cp1 = [-0.3, -0.3, -0.3, -0.4, -0.5, -0.55, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6]
hOverL2 = [0.50]
cp2 = [-0.5, -0.5, -0.5, -0.5, -0.5, -0.55, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6]
hOverL3 = [1.0, 2.0, 10.0, 15.0, 20.0]
cp3 = [-0.7, -0.7, -0.7, -0.65, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6]

def Interpolation(hOverLNew, AngleNew):
    DBDB = CPdata(angle, hOverL1, cp1, hOverL2, cp2, hOverL3, cp3)
    f = LinearNDInterpolator(list(zip(DBDB['hOverL'], DBDB['Angle'])), DBDB['Cp'])
    Cp1 = f(hOverLNew, AngleNew)
    return Cp1
CP3 = Interpolation (h/L, theta)
print ("CP3 =", Interpolation (h/L, theta))

LOverB = [0.0, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 10.0, 100.0]
cp4 = [-0.5, -0.5, -0.4, -0.3, -0.25, -0.2, -0.2, -0.2, -0.2]

DF1 = DataFrame(LOverB)
DF2 = DataFrame(cp4)
DF3 = pd.concat([DF1, DF2], axis = 1)
DF3.columns = ['LOverB', 'Cp']

Func = interpolate.interp1d(DF3['LOverB'], DF3['Cp'])

CP4 = Func(L/B)
print ("CP4 = ", Func(L/B))

CP4_1 = Func(B/L)
print ("CP4_1 = ", Func(B/L))

if h/B<=0.5:
    CP5 = -0.9
elif h/B<=1.0:
    CP5 = -0.8*(h/B)-0.5
else:
    CP5 = -1.3

print ("CP5 = ", CP5)

z = np.linspace(0,BldgH,n+1, endpoint=True)
DF4 = DataFrame(z)

KZ =[]

for i in range(len(z)):
    if z[i] > 4.572:
        Kz = 2.01*(z[i]/DB[(exp)]['z_g'])**(2/DB[(exp)]['alpha'])
    else:
        Kz = 2.01*(4.572/DB[(exp)]['z_g'])**(2/DB[(exp)]['alpha'])
    KZ.append(Kz)

KH = []
if h > 4.572:
    Kh = 2.01*(h/DB[(exp)]['z_g'])**(2/DB[(exp)]['alpha'])
else:
    Kh = 2.01*(4.572/DB[(exp)]['z_g'])**(2/DB[(exp)]['alpha'])
KH.append(Kh)

DF5 = DataFrame(KZ)

DF6 = pd.concat([DF4, DF5], axis = 1)
DF6.columns = ['Elevation(m)', 'KZ']
print (DF6)

print ("KH = ", KH)

KztTable1 = {
    "Exposure B": {
        "2Dridges": 1.3,
        "2Descarpments": 0.75,
        "3Daxisymmetric": 0.95
    },
    "Exposure C": {
        "2Dridges": 1.45,
        "2Descarpments": 0.85,
        "3Daxisymmetric": 1.05
    },
    "Exposure D": {
        "2Dridges": 1.55,
        "2Descarpments": 0.95,
        "3Daxisymmetric": 1.15
    },
}

KztTable2 = {
    "gammas": {
        "2Dridges": 3.0,
        "2Descarpments": 2.5,
        "3Daxisymmetric": 4
    },
    "mus": {
        "2DridgesUp": 1.5,
        "2DescarpmentsUp": 1.5,
        "3DaxisymmetricUp": 1.5,
        "2DridgesDown": 1.5,
        "2DescarpmentsDown": 4,
        "3DaxisymmetricDown": 1.5
    },
}

if H_hill/Lh>0.5:
    K1 = KztTable1[(exp)][(topho)]*0.5
else :
    K1 = KztTable1[(exp)][(topho)]*H_hill/Lh
print ("K1 = ", K1)

if H_hill/Lh>0.5:
    K2 = 1-abs(x)/(KztTable2["mus"][(topho + UD)]*2*H_hill)
else : 
    K2 = 1-abs(x)/(KztTable2["mus"][(topho + UD)]*Lh)
print ("K2 = ", K2)

K3 = []

if H_hill/Lh>0.5:
    for i in z:
        k3 = 2.718281828**(-KztTable2["gammas"][(topho)]*i/(2*H_hill))
        K3.append(k3)
    k3 = 2.718281828**(-KztTable2["gammas"][(topho)]*h/(2*H_hill))
    K3.append(k3)
else: 
    for i in z:
        k3 = 2.718281828**(-KztTable2["gammas"][(topho)]*i/Lh)
        K3.append(k3)
    k3 = 2.718281828**(-KztTable2["gammas"][(topho)]*h/Lh)
    K3.append(k3)

print ("K3 = ", K3[:-1])
print ("K3H = ", K3[-1])

Kzt = []
for j in range(0,len(K3)):
    kzt = (1+K1*K2*K3[j])**2
    Kzt.append(kzt)

if Topographic_data == 'Y':
    KZT = Kzt[:-1]
    KHT = [Kzt[-1]]
else: 
    KZT = [1 for i in range (n+1)]
    KHT = [1]

print ("KZT = ", KZT)
print ("KHT = ", KHT) 

#Velocity pressure
QZ=[]
QH=[]
for i in range(len(KZT)):
    qZ = round(0.613*KZ[i]*KZT[i]*Kd*V**2,1)
    QZ.append(qZ)
for j in range(len(KHT)):
    qH = round(0.613*KH[j]*KHT[j]*Kd*V**2,1)
    QH.append(qH) 
print ("qZ = ", QZ, " N/m2")
print ("qH = ", QH, " N/m2")

if Type == 'ECL':
    print ('Enclosed Building')
    GCpi = 0.18
    print ('GCpi = ', GCpi)
else :
    print ('Partially Enclosed Building')
    GCpi = 0.55
    print ('GCpi = ', GCpi)
print ("")
print ("<< Wind for normal to ridge >>")
#Windward Wall Pressure
Cp_ww = 0.8
P_ww = []
for i in range(len(QZ)):
    p_ww = round(QZ[i]*G*Cp_ww-QH[0]*GCpi,1)
    P_ww.append(p_ww)
print ("Windward Wall Pressure = ", P_ww, "N/m2")
P_ww = []
for i in range(len(QZ)):
    p_ww = round(QZ[i]*G*Cp_ww+QH[0]*GCpi,1)
    P_ww.append(p_ww)
print ("Windward Wall Pressure = ", P_ww, "N/m2")

#Leeward Wall Pressure
Cp_lw = CP4
P_lw = round(QH[0]*G*Cp_lw-QH[0]*GCpi,1)
print ("Leeward Wall Pressure = ", P_lw, "N/m2")
P_lw = round(QH[0]*G*Cp_lw+QH[0]*GCpi,1)
print ("Leeward Wall Pressure = ", P_lw, "N/m2")

#Side Wall Pressure
Cp_sw = -0.7
P_sw = round(QH[0]*G*Cp_sw-QH[0]*GCpi,1)
print ("Side Wall Pressure = ", P_sw, "N/m2")
P_sw = round(QH[0]*G*Cp_sw+QH[0]*GCpi,1)
print ("Side Wall Pressure = ", P_sw, "N/m2")

#Windward Roof Pressure
Cp_wr1 = CP1
P_wr1 = round(QH[0]*G*Cp_wr1-QH[0]*GCpi,1)
print ("Windward Roof Pressure = ", P_wr1, "N/m2")
P_wr1 = round(QH[0]*G*Cp_wr1+QH[0]*GCpi,1)
print ("Windward Roof Pressure = ", P_wr1, "N/m2")
Cp_wr2 = CP2
P_wr2 = round(QH[0]*G*Cp_wr2-QH[0]*GCpi,1)
print ("Windward Roof Pressure = ", P_wr2, "N/m2")
P_wr2 = round(QH[0]*G*Cp_wr2+QH[0]*GCpi,1)
print ("Windward Roof Pressure = ", P_wr2, "N/m2")

#Leeward Roof Pressure
Cp_lr = CP3
P_lr = round(QH[0]*G*Cp_lr-QH[0]*GCpi,1)
print ("Leeward Roof Pressure = ", P_lr, "N/m2")
P_lr = round(QH[0]*G*Cp_lr+QH[0]*GCpi,1)
print ("Leeward Roof Pressure = ", P_lr, "N/m2")

print ("")
print ("<< Wind for parallel to ridge >>")
#Windward Wall Pressure
Cp_ww = 0.8
P_ww = []
for i in range(len(QZ)):
    p_ww = round(QZ[i]*G_1*Cp_ww-QH[0]*GCpi,1)
    P_ww.append(p_ww)
print ("Windward Wall Pressure = ", P_ww, "N/m2")
P_ww = []
for i in range(len(QZ)):
    p_ww = round(QZ[i]*G_1*Cp_ww+QH[0]*GCpi,1)
    P_ww.append(p_ww)
print ("Windward Wall Pressure = ", P_ww, "N/m2")

#Leeward Wall Pressure
Cp_lw = CP4_1
P_lw = round(QH[0]*G_1*Cp_lw-QH[0]*GCpi,1)
print ("Leeward Wall Pressure = ", P_lw, "N/m2")
P_lw = round(QH[0]*G_1*Cp_lw+QH[0]*GCpi,1)
print ("Leeward Wall Pressure = ", P_lw, "N/m2")

#Side Wall Pressure
Cp_sw = -0.7
P_sw = round(QH[0]*G_1*Cp_sw-QH[0]*GCpi,1)
print ("Side Wall Pressure = ", P_sw, "N/m2")
P_sw = round(QH[0]*G_1*Cp_sw+QH[0]*GCpi,1)
print ("Side Wall Pressure = ", P_sw, "N/m2")

#Parallel Roof Pressure
Cp_prR = CP5
P_prR = round(QH[0]*G_1*Cp_prR-QH[0]*GCpi,1)
print ("Paralle Roof Pressure = ", P_prR, "N/m2")
P_prR = round(QH[0]*G_1*Cp_prR+QH[0]*GCpi,1)
print ("Paralle Roof Pressure = ", P_prR, "N/m2")
