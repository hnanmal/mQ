# 240409
# Shelters Wind Load - Main Structure
# Included Component and Cladding
# Loop for Load Case and Wind Directions - Swtiching B&L not considered
# Effective Wind Area for C&C should be considered manually (ewa)
# 250418 Automatic Effective Wind Area for C&C included 
# 250418 Topographic Data Modified
# 250422 Tables Modified to include every case

import numpy as np
from pandas import DataFrame
from scipy.interpolate import interp1d
from scipy import interpolate

exp = 'Exposure C' #Exposure Class, 'Exposure B', 'Exposure C', 'Exposure D'
h = 14 #mean roof height in m 
B = 15 #Building Dimension normal to wind
L = 20 #Building Dimension parallel to wind
beta = 0.02 #Damping ratio
Type = 'OM' # 'OM' for Open Monoslope / 'OP' for Open Pitched
blockage = 'C'# 'C' for Clear Wind / 'O' for Obstructed 
xnew = 37 # Roof Angle in Degree
Kd = 0.85 # direcionality factor
V = 58 # basic wind speed in ASCE 7
StructuralType = 'Steel' # 'Concrete' or 'Steel' or 'Other' for calculation fundamental frequency
purlin_s = 1.2 #purlin spacing in m
purlin_l = 6 # purlin length in m
Topographic_data = 'no' # Should Consider Topographic Feature? 'yes' or 'no'

print (' <Basic Input Data>')
print ('Exposure Class : ', exp)
print ('Basic Wind Speed : ', V, 'm/s')
print ('Building Mean Roof Height : ', h, 'm')
print ('Building Dimension normal to wind, B : ', B, 'm')
print ('Building Dimension parallel to wind, L : ', L, 'm')
building_type = 'Open Monoslope' if Type == 'OM' else 'Open Pitched'
print ('Building Type : ', building_type)
print ('Building Roof Angle : ', xnew, 'degree')
print ('Building Purlin Spacing : ', purlin_s, 'm')
print ('Building Purlin Un-supported Length : ', purlin_l, 'm')
print ('Should Consider Topographic Feature?', Topographic_data)


BldgH = 13 #Building Height in meter (h: mean roof height와 다름, 처마높이)
Lh = 561.454 # distance upwind of crest to where the difference in ground elevation in half the height of hill
H_hill = 280.7 # height of hill
x = -1127 # distance from the crest to the building site
topho = '2Descarpments' #'2Dridges', '2Descarpments', '3Daxisymmetric'
UD = 'Up' #'Up' / 'Down' for Upwind & Downwind of Crest, respectively

print ('\n <Topographic Input Data>')
print ('Building Eave Height : ', BldgH, 'm')
print ('Distance upwind of crest to where the difference in ground elevation in half the height of hill : ', Lh, 'm')
print ('Height of Hill : ', H_hill, 'm')
print ('Distance from the crest to the building site : ', abs(x), 'm')
print ('Topographic Type : ', topho)

EffecWindArea = max(purlin_s*purlin_l,purlin_l**2/3 )
zone_a = max(min(B*0.1, L*0.1, 0.4*h), 0.04*min(B,L), 0.9)
ewa = 'EWA1' if EffecWindArea <= zone_a**2 else 'EWA2' if EffecWindArea <= 4*zone_a**2 else 'EWA3'

# print ('Effective Wind Area =', EffecWindArea, 'm^2' )
# print ('Corner Zone Width a = ', zone_a, 'm')

H = h/0.305 #mean roof height in ft
if StructuralType == 'Steel':
    na=22.2/H**0.8
elif StructuralType == 'Concrete':
    na=43.5/H**0.9
else:
    na=75/H
# print("Fundamental Frequency = ", round(na, 4))

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

# print (DB)

z_bar = max(h*0.6,DB[(exp)]['z_min']) #ASCE 7-10 ss26.9.4
gq = 3.4 #ASCE 7-10 ss26.9.4
gv = 3.4 #ASCE 7-10 ss26.9.4

Lz = DB[(exp)]['l']*(z_bar/10)**(DB[(exp)]['epsilon']) #ASCE 7-10 eq26.9-9
Q = (1/(1+0.63*((B+h)/Lz)**0.63))**0.5 #ASCE 7-10 eq26.9-8
Vz = DB[(exp)]['b']*(z_bar/10)**(DB[(exp)]['alpha_bar'])*V #ASCE 7-10 eq26.9-16
N1 = na*Lz/Vz
Rn = 7.47*N1/((1+10.3*N1)**(5/3))
eta1 = 4.6*na*h/Vz
eta2 = 4.6*na*B/Vz
eta3 = 15.4*na*L/Vz
e = 2.718281828459045
Rh = 1/eta1-1/(2*eta1**2)*(1-e**(-2*eta1))
RB = 1/eta2-1/(2*eta2**2)*(1-e**(-2*eta2))
RL = 1/eta3-1/(2*eta3**2)*(1-e**(-2*eta3))
R = (1/beta*Rn*Rh*RB*(0.53+0.479*RL))**0.5
Iz = DB[(exp)]['c']*(10/z_bar)**(1/6)
gR =(2*np.log(3600*na))**0.5+0.577/(2*np.log((3600*na))**0.5)

if na>=1:
    G = 0.925*((1+1.7*gq*Iz*Q)/(1+1.7*gv*Iz))
else:
    G = 0.925*((1+1.7*Iz*(gq**2*Q**2+gR**2*R**2)**0.5)/(1+1.7*gv*Iz))

# print("G = ", round(G, 4))

CNW = {'RoofSlop':  [0, 7.5, 15, 22.5, 30, 37.5, 45],
           'OMAgamma0C':  [1.2, -0.6, -0.9, -1.5, -1.8, -1.8, -1.6],
           'OMBgamma0C': [-1.1, -1.4, -1.9, -2.4, -2.5, -2.4, -2.3],
           'OMAgamma0O': [-0.5, -1, -1.1, -1.5, -1.5, -1.5, -1.3],
           'OMBgamma0O': [-1.1, -1.7, -2.1, -2.3, -2.3, -2.2, -1.9],
           'OMAgamma180C':[1.2, 0.9, 1.3, 1.7, 2.1, 2.1, 2.2],
           'OMBgamma180C':[-1.1, 1.6, 1.8, 2.2, 2.6, 2.7, 2.6],
           'OMAgamma180O':[-0.5, -0.2, 0.4, 0.5, 0.6, 0.7, 0.8],
           'OMBgamma180O':[-1.1, 0.8, 1.2, 1.3, 1.6, 1.9, 2.1],
           'OPAgamma0C':  [1.2, 1.1, 1.1, 1.1, 1.3, 1.3, 1.1],
           'OPBgamma0C': [-1.1, 0.2, 0.1, -0.1, -0.1, -0.2, -0.3],
           'OPAgamma180C': [0.3, -0.3, -0.4, 0.1, 0.3, 0.6, 0.9],
           'OPBgamma180C': [-0.1, -1.2, -1.1, -0.8, -0.9, -0.6, -0.5],
           'OPAgamma0O':[-0.5, -1.6, -1.2, -1.2, -0.7, -0.6, -0.5],
           'OPBgamma0O':[-1.1, -0.9, -0.6, -0.8, -0.2, -0.3, -0.3],
           'OPAgamma180O':[-1.2, -1, -1, -1.2, -0.7, -0.6, -0.5],
           'OPBgamma180O':[-0.6, -1.7, -1.6, -1.7, -1.1, -0.9, -0.7]           
           }

CNW=DataFrame(CNW)

LoadCase = ['A', 'B']
gamma = ['gamma0', 'gamma180']
cnw=[]
for i in LoadCase:
    for j in gamma:
        k=Type+i+j+blockage
        xi = CNW['RoofSlop']
        yi = CNW[(k)]
        f = interpolate.interp1d(xi, yi, kind='linear')
        ynew = round(float(f(xnew)), 5)
        cnw.append(ynew)
# print ("Net Pressure Coefficient, C_NW = ", cnw)
# print("CNW = ", round(max(cnw),5))
# print("CNW = ", round(min(cnw),5))

CNL = {'RoofSlop':  [0, 7.5, 15, 22.5, 30, 37.5, 45],
           'OMAgamma0C':  [0.3, -1.0, -1.3, -1.6, -1.8, -1.8, -1.8],
           'OMBgamma0C': [-0.1, 0.0, 0.0, -0.3, -0.5, -0.6, -0.7],
           'OMAgamma0O': [-1.2, -1.5, -1.5, -1.7, -1.8, -1.8, -1.8],
           'OMBgamma0O': [-0.6, -0.8, -0.6, -0.9, -1.1, -1.1, -1.2],
           'OMAgamma180C':[0.3, 1.5, 1.6, 1.8, 2.1, 2.2, 2.5],
           'OMBgamma180C':[-0.1, 0.3, 0.6, 0.7, 1.0, 1.1, 1.4],
           'OMAgamma180O':[-1.2, -1.2, -1.1, -1.0, -1.0, -0.9, -0.9],
           'OMBgamma180O':[-0.6, -0.3, -0.3, 0.0, 0.1, 0.3, 0.4],
           'OPAgamma0C':  [0.3, -0.3, -0.4, 0.1, 0.3, 0.6, 0.9],
           'OPBgamma0C': [-0.1, -1.2, -1.1, -0.8, -0.9, -0.6, -0.5],
           'OPAgamma180C': [0.3, -0.3, -0.4, 0.1, 0.3, 0.6, 0.9],
           'OPBgamma180C': [-0.1, -1.2, -1.1, -0.8, -0.9, -0.6, -0.5],
           'OPAgamma0O':[-1.2, -1.0, -1.0, -1.2, -0.7, -0.6, -0.5],
           'OPBgamma0O':[-0.6, -1.7, -1.6, -1.7, -1.1, -0.9, -0.7],
           'OPAgamma180O':[-1.2, -1.0, -1.0, -1.2, -0.7, -0.6, -0.5],
           'OPBgamma180O':[-0.6, -1.7, -1.6, -1.7, -1.1, -0.9, -0.7],
           }

CNL = DataFrame(CNL)

cnl = []

for i in LoadCase:
    for j in gamma:
        k=Type+i+j+blockage
        xi = CNL['RoofSlop']
        yi = CNL[(k)]
        f = interpolate.interp1d(xi, yi, kind='linear')
        ynew = round(float(f(xnew)), 5)
        cnl.append(ynew)
# print ("Net Pressure Coefficient, C_NL = ", cnl)
# print("CNL = ", round(max(cnl),5))
# print("CNL = ", round(min(cnl),5))

CNgamma90 = {'RoofSlop':  [0, 7.5, 15, 22.5, 30, 37.5, 45],
            'OMAgamma90<hC' :[-0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8],
            'OMBgamma90<hC' :[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
            'OMAgamma90<hO' :[-1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2],
            'OMBgamma90<hO' :[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'OPAgamma90<hC' :[-0.8, -0.8, -0.8, -0.8, -0.8, -0.8, -0.8],
            'OPBgamma90<hC' :[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
            'OPAgamma90<hO' :[-1.2, -1.2, -1.2, -1.2, -1.2, -1.2, -1.2],
            'OPBgamma90<hO' :[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], 
            'OMAgamma90<2hC' :[-0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6],
            'OMBgamma90<2hC' :[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'OMAgamma90<2hO' :[-0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9],
            'OMBgamma90<2hO' :[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'OPAgamma90<2hC' :[-0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6],
            'OPBgamma90<2hC' :[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'OPAgamma90<2hO' :[-0.9, -0.9, -0.9, -0.9, -0.9, -0.9, -0.9],
            'OPBgamma90<2hO' :[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
            'OMAgamma90>2hC' :[-0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3],
            'OMBgamma90>2hC' :[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            'OMAgamma90>2hO' :[-0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6],
            'OMBgamma90>2hO' :[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            'OPAgamma90>2hC' :[-0.3, -0.3, -0.3, -0.3, -0.3, -0.3, -0.3],
            'OPBgamma90>2hC' :[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3],
            'OPAgamma90>2hO' :[-0.6, -0.6, -0.6, -0.6, -0.6, -0.6, -0.6],
            'OPBgamma90>2hO' :[0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3]
             }

gamma90 = ['gamma90<h', 'gamma90<2h', 'gamma90>2h']

CNgamma90 = DataFrame(CNgamma90)

cngamma90 = []
for i in LoadCase:
    for j in gamma90:
        k=Type+i+j+blockage
        xi = CNgamma90['RoofSlop']
        yi = CNgamma90[(k)]
        f = interpolate.interp1d(xi, yi, kind='linear')
        ynew = float(f(xnew))
        cngamma90.append(ynew)
# print ("Net Pressure Coefficient, CN_gamma90 for <h, <2h, >2h = ", cngamma90)
# print ("CNgamma90 = ", round(max(cngamma90),4))
# print ("CNgamma90 = ", round(min(cngamma90),4))

print ('\n <Wind Load Calculation Basis>')
print ('Effective Wind Area =', EffecWindArea, 'm^2' )
print ('Corner Zone Width a = ', zone_a, 'm')
print("Fundamental Frequency = ", round(na, 4))
print("Gust-Effect Factor, G  = ", round(G, 4))

# z = np.linspace(0, BldgH, n+1, endpoint=True)

KZ = []
if h > 4.572:
    Kz = round(2.01*(h/DB[(exp)]['z_g'])**(2/DB[(exp)]['alpha']), 4)
else:
    Kz = round(2.01*(4.572/DB[(exp)]['z_g'])**(2/DB[(exp)]['alpha']), 4)
KZ.append(Kz)

print ("Velocity Pressure Exposure Coefficient KZ = ", KZ)

if Topographic_data == 'yes':
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
        "mus":  {
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

    K2 = 1-abs(x)/(KztTable2["mus"][(topho + UD)]*Lh)
    print ("K2 = ", round(K2, 4))

    K3 = []
    # for i in z:
    #     k3 = 2.718281828**(-KztTable2["gammas"][(topho)]*i/Lh)
    #     K3.append(k3)
    k3 = round(2.718281828**(-KztTable2["gammas"][(topho)]*h/Lh),4)
    K3.append(k3)
    print ("K3 = ", K3)
    for j in range(0,len(K3)):
        kzt = round((1+K1*K2*K3[j])**2,4)
        KZT = kzt
else:
    KZT = 1.0 # 지형의 영향 무시한 값 ('ASCE 7-10 cl. 26.8.1 Condition' '모두' 불만족할 경우)

print ('Topographic Factor, KZT = ', KZT)

PW_Main = []
for k in range(0,len(KZ)):
    for l in cnw:
        q = 0.613*KZ[k]*KZT*Kd*V**2
        p = round(q*G*l,1)
        PW_Main.append(p)
print ('\n <Wind Pressure for Main Structure>')
print ("Net Pressure Coefficient, C_NW = ", cnw)
print ("Pressure for Main Structural Frame(CW) = ", PW_Main, "Pa")
# print ("Positive Pressure for Main Structural Frame(CW) = ", max(PW_Main), "Pa")
# print ("Negative Pressure for Main Structural Frame(CW) = ", min(PW_Main), "Pa")

PL_Main = []
for k in range(0,len(KZ)):
    for l in cnl:
        q = 0.613*KZ[k]*KZT*Kd*V**2
        p = round(q*G*l,1)
        PL_Main.append(p)
print ("\n Net Pressure Coefficient, C_NL = ", cnl)
print ("Pressure for Main Structural Frame(CL) = ", PL_Main, "Pa")
# print ("Positive Pressure for Main Structural Frame(CL) = ", max(PL_Main), "Pa")
# print ("Negative Pressure for Main Structural Frame(CL) = ", min(PL_Main), "Pa")

Pgamma90_Main = []
for k in range(0,len(KZ)):
    for l in cngamma90:
        q = 0.613*KZ[k]*KZT*Kd*V**2
        p = round(q*G*l,1)
        Pgamma90_Main.append(p)
print ("\nNet Pressure Coefficient, CN_gamma90 for <h, <2h, >2h = ", cngamma90)
print ("Pressures for Main Structural Frame(gamma90), <h, <2h, >2h = ", Pgamma90_Main, "Pa")
# print ("Positive Pressure for Main Structural Frame(gamma90) = ", max(Pgamma90_Main), "Pa")
# print ("Negative Pressure for Main Structural Frame(gamma90) = ", min(Pgamma90_Main), "Pa")


CNccZ3 = {'RoofSlop':  [0, 7.5, 15, 30, 45],
           'OMEWA1CA':  [2.4, 3.2, 3.6, 5.2, 5.2],
           'OMEWA1CB': [-3.3, -4.2, -3.8, -5, -4.6],
           'OMEWA1OA':  [1.0, 1.6, 2.4, 3.2, 4.2],
           'OMEWA1OB': [-3.6, -5.1, -4.2, -4.6, -3.8],
           'OMEWA2CA':  [1.8, 2.4, 2.7, 3.9, 3.9],
           'OMEWA2CB': [-1.7, -2.1, -2.9, -3.8, -3.5],
           'OMEWA2OA':  [0.8, 1.2, 1.8, 2.4, 3.2],
           'OMEWA2OB': [-1.8, -2.6, -3.2, -3.5, -2.9],
           'OMEWA3CA':  [1.2, 1.6, 1.8, 2.6, 2.6],
           'OMEWA3CB': [-1.1, -1.4, -1.9, -2.5, -2.3],
           'OMEWA3OA':  [0.5, 0.8, 1.2, 1.6, 2.1],
           'OMEWA3OB': [-1.2, -1.7, -2.1, -2.3, -1.9],
           'OPEWA1CA':  [2.4, 2.2, 2.2, 2.6, 2.2],
           'OPEWA1CB': [-3.3, -3.6, -2.2, -1.8, -1.6],
           'OPEWA1OA':  [1.0, 1.0, 1.0, 1.0, 1.0],
           'OPEWA1OB': [-3.6, -5.1, -3.2, -2.4, -2.4],
           'OPEWA2CA':  [1.8, 1.7, 1.7, 2.0, 1.7],
           'OPEWA2CB': [-1.7, -1.8, -1.7, -1.4, -1.2],
           'OPEWA2OA':  [0.8, 0.8, 0.8, 0.8, 0.8],
           'OPEWA2OB': [-1.8, -2.6, -2.4, -1.8, -1.8],
           'OPEWA3CA':  [1.2, 1.1, 1.1, 1.3, 1.1],
           'OPEWA3CB': [-1.1, -1.2, -1.1, -0.9, -0.8],
           'OPEWA3OA':  [0.5, 0.5, 0.5, 0.5, 0.5],
           'OPEWA3OB': [-1.2, -1.7, -1.6, -1.2, -1.2]
           }

CNccZ2 = {'RoofSlop':  [0, 7.5, 15, 30, 45],
           'OMEWA1CA':  [1.8, 2.4, 2.7, 3.9, 3.9],
           'OMEWA1CB': [-1.7, -2.1, -2.9, -3.8, -3.5],
           'OMEWA1OA':  [0.8, 1.2, 1.8, 2.4, 3.2],
           'OMEWA1OB': [-1.8, -2.6, -3.2, -3.5, -2.9],
           'OMEWA2CA':  [1.8, 2.4, 2.7, 3.9, 3.9],
           'OMEWA2CB': [-1.7, -2.1, -2.9, -3.8, -3.5],
           'OMEWA2OA':  [0.8, 1.2, 1.8, 2.4, 3.2],
           'OMEWA2OB': [-1.8, -2.6, -3.2, -3.5, -2.9],
           'OMEWA3CA':  [1.2, 1.6, 1.8, 2.6, 2.6],
           'OMEWA3CB': [-1.1, -1.4, -1.9, -2.5, -2.3],
           'OMEWA3OA':  [0.5, 0.8, 1.2, 1.6, 2.1],
           'OMEWA3OB': [-1.2, -1.7, -2.1, -2.3, -1.9],
           'OPEWA1CA':  [1.8, 1.7, 1.7, 2.0, 1.7],
           'OPEWA1CB': [-1.7, -1.8, -1.7, -1.4, -1.2],
           'OPEWA1OA':  [0.8, 0.8, 0.8, 0.8, 0.8],
           'OPEWA1OB': [-1.8, -2.6, -2.4, -1.8, -1.8],
           'OPEWA2CA':  [1.8, 1.7, 1.7, 2.0, 1.7],
           'OPEWA2CB': [-1.7, -1.8, -1.7, -1.4, -1.2],
           'OPEWA2OA':  [0.8, 0.8, 0.8, 0.8, 0.8],
           'OPEWA2OB': [-1.8, -2.6, -2.4, -1.8, -1.8],
           'OPEWA3CA':  [1.2, 1.1, 1.1, 1.3, 1.1],
           'OPEWA3CB': [-1.1, -1.2, -1.1, -0.9, -0.8],
           'OPEWA3OA':  [0.5, 0.5, 0.5, 0.5, 0.5],
           'OPEWA3OB': [-1.2, -1.7, -1.6, -1.2, -1.2]
           }

CNccZ1 = {'RoofSlop':  [0, 7.5, 15, 30, 45],
           'OMEWA1CA':  [1.2, 1.6, 1.8, 2.6, 2.6],
           'OMEWA1CB': [-1.1, -1.4, -1.9, -2.5, -2.3],
           'OMEWA1OA':  [0.5, 0.8, 1.2, 1.6, 2.1],
           'OMEWA1OB': [-1.2, -1.7, -2.1, -2.3, -1.9],
           'OMEWA2CA':  [1.2, 1.6, 1.8, 2.6, 2.6],
           'OMEWA2CB': [-1.1, -1.4, -1.9, -2.5, -2.3],
           'OMEWA2OA':  [0.5, 0.8, 1.2, 1.6, 2.1],
           'OMEWA2OB': [-1.2, -1.7, -2.1, -2.3, -1.9],
           'OMEWA3CA':  [1.2, 1.6, 1.8, 2.6, 2.6],
           'OMEWA3CB': [-1.1, -1.4, -1.9, -2.5, -2.3],
           'OMEWA3OA':  [0.5, 0.8, 1.2, 1.6, 2.1],
           'OMEWA3OB': [-1.2, -1.7, -2.1, -2.3, -1.9],
           'OPEWA1CA':  [1.2, 1.1, 1.1, 1.3, 1.1],
           'OPEWA1CB': [-1.1, -1.2, -1.1, -0.9, -0.8],
           'OPEWA1OA':  [0.5, 0.5, 0.5, 0.5, 0.5],
           'OPEWA1OB': [-1.2, -1.7, -1.6, -1.2, -1.2],
           'OPEWA2CA':  [1.2, 1.1, 1.1, 1.3, 1.1],
           'OPEWA2CB': [-1.1, -1.2, -1.1, -0.9, -0.8],
           'OPEWA2OA':  [0.5, 0.5, 0.5, 0.5, 0.5],
           'OPEWA2OB': [-1.2, -1.7, -1.6, -1.2, -1.2],
           'OPEWA3CA':  [1.2, 1.1, 1.1, 1.3, 1.1],
           'OPEWA3CB': [-1.1, -1.2, -1.1, -0.9, -0.8],
           'OPEWA3OA':  [0.5, 0.5, 0.5, 0.5, 0.5],
           'OPEWA3OB': [-1.2, -1.7, -1.6, -1.2, -1.2]
           }

Cnccs = [CNccZ3, CNccZ2, CNccZ1]
print ('\n<Wind Pressure for Components and Cladding>')
for sn in range(len(Cnccs)):
    temp = Cnccs[sn]
    CNcc = DataFrame(temp)
    cncc=[]
    z_ = 3-sn
    print (' Cladding Zone :', z_)
    for j in LoadCase:
        k=Type+ewa+blockage+j
        xi = CNcc['RoofSlop']
        yi = CNcc[(k)]
        f = interpolate.interp1d(xi, yi, kind='linear')
        ynew = float(f(xnew))
        cncc.append(ynew)
        print(f'CNcc for Loadcase {j}  = {round(ynew,4)}')
        P_cc = []
        for m in range(0,len(KZ)):
            q = 0.613*KZ[m]*KZT*Kd*V**2
            p = round(q*G*ynew,1)
            P_cc.append(p)
        print ("Pressure for Components & Cladding = ", max(P_cc), "Pa")
    print (' ')

    
