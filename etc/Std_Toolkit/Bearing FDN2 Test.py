from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

qa = 191.5 # 허용지내력 kPa
h_BOFDN = 1.496 #기초 저면 m
S = 4.79 # Surcharge Load kN/m^2
w_c = 24 #콘크리트 단중 kN/m^3
w_s = 18.9 #흙 단중 kN/m^3
fc = 24.1 #콘크리트 압축강도 MPa
fy = 413.67 #철근항복강도 MPa
Cx = 0.406 #기둥 치수 x m
Cy = 0.406 #기둥 치수 y m
cc = 50 #피복두께 mm
Dc = 16 # 기둥 Pedestal 주근 mm
D = 16 # 기초 배근 mm

Ps = 1334 #사용축하중
Pu = 1815 #극한축하중
Msx = 0 #x축에 대한 사용모멘트
Msy = 189.8 #y축에 대한 사용모멘트
Mux = 0 #x축에 대한 극한모멘트
Muy = 260.3 #y축에 대한 극한모멘트

ex = Msy/Ps
ey = Msx/Ps
e = (ex**2+ey**2)**0.5

print ("")
print ("<Design Condition>")
print ("Eccentricity = ", round(e,4), "m")

qe = qa - (w_c+w_s)/2*h_BOFDN-S
x1 = (-6*e+((6*e)**2-4*6*(-2*Ps/qe))**0.5)/12
x2 = (-6*e-((6*e)**2-4*6*(-2*Ps/qe))**0.5)/12
if x1<0:
    x = x2
else:
    x = x1

Lx1 = 2*(e+x)
Lx = (Lx1*10-Lx1*10%1+1)/10
Ly = Lx
print ("")
print ("<Foundation Dimension>")
print ("Lx =", Lx, "m", " , " "Ly =", Ly, "m")
print ("")

# Soil Stress Under Serevice Load
a=Ps/(Lx*Ly)+Msx/(Lx*Ly**2/6)+Msy/(Ly*Lx**2/6)+(w_c+w_s)/2*h_BOFDN+S
b=Ps/(Lx*Ly)+Msx/(Lx*Ly**2/6)-Msy/(Ly*Lx**2/6)+(w_c+w_s)/2*h_BOFDN+S
c=Ps/(Lx*Ly)-Msx/(Lx*Ly**2/6)-Msy/(Ly*Lx**2/6)+(w_c+w_s)/2*h_BOFDN+S
d=Ps/(Lx*Ly)-Msx/(Lx*Ly**2/6)+Msy/(Ly*Lx**2/6)+(w_c+w_s)/2*h_BOFDN+S

s1=abs(a)-abs(b)+abs(b)*(abs(a)+abs(b))/abs(a)
t1=abs(a)
if b<0:
    u1=s1
else:
    u1=t1
if b<0:
    x1=abs(a)*Lx/(abs(a)+abs(b))
else:
    x1=Lx

s4=abs(a)-abs(d)+abs(d)*(abs(a)+abs(d))/abs(a)
t4=abs(a)
if d<0:
    u4=s4
else:
    u4=t4
if d<0:
    y4=abs(a)*Ly/(abs(a)+abs(d))
else:
    y4=Ly

if b*d<0:
    if b<0:
        c1=0
    else:
        c1=c
else:
    c1=b/(b+d)*c

if b*d<0:
    if d<0:
        c2=0
    else:
        c2=c
else:
    c2=d/(b+d)*c

s2=abs(b)+abs(c1)**2/abs(b)
t2=abs(b)
if b<0:
    u2=0
else:
    if c1<0:
        u2=s2
    else:
        u2=t2
if c1<0:
    if b>0:
        y2=Ly-abs(c1)*Ly/(abs(c1)+abs(b))
    else:
        y2=Ly

s3=abs(d)-abs(c2)+abs(c2)*(abs(d)+abs(c2))/abs(d)
t3=abs(d)
if d<0:
    u3=0
else:
    if c2<0:
        u3=s3
    else:
        u3=t3
if c2<0:
    x3=abs(d)*Lx/(abs(d+abs(c2)))
else:
    x3=Lx

if c2<0:
    u5=0
else:
    u5=abs(c)

us=max(u1,u4)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n=12
x = np.linspace(-Lx/2, Lx/2, n)
X = np.tile(x, (n, 1))
y = np.linspace(-Ly/2, Ly/2, n)
Y = np.transpose(np.tile(y,(n,1)))

res = []
y1 = np.linspace(u2,u5,n)
y2 = np.linspace(us,u3,n)
Z = np.array(list(map(lambda x: np.linspace(y1[x],y2[x],n), range(n))))
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=1, antialiased=False)
ax.contourf(X, Y, Z, zdir='z', offset=0, cmap='coolwarm')
ax.set_zlim(-10, qa+10)
plt.show()

#Soil Stress Under Ultimate Load
a=Pu/(Lx*Ly)+Mux/(Lx*Ly**2/6)+Muy/(Ly*Lx**2/6)
b=Pu/(Lx*Ly)+Mux/(Lx*Ly**2/6)-Muy/(Ly*Lx**2/6)
c=Pu/(Lx*Ly)-Mux/(Lx*Ly**2/6)-Muy/(Ly*Lx**2/6)
d=Pu/(Lx*Ly)-Mux/(Lx*Ly**2/6)+Muy/(Ly*Lx**2/6)

s1=abs(a)-abs(b)+abs(b)*(abs(a)+abs(b))/abs(a)
t1=abs(a)
if b<0:
    u1=s1
else:
    u1=t1
if b<0:
    x1=abs(a)*Lx/(abs(a)+abs(b))
else:
    x1=Lx

s4=abs(a)-abs(d)+abs(d)*(abs(a)+abs(d))/abs(a)
t4=abs(a)
if d<0:
    u4=s4
else:
    u4=t4
if d<0:
    y4=abs(a)*Ly/(abs(a)+abs(d))
else:
    y4=Ly

if b*d<0:
    if b<0:
        c1=0
    else:
        c1=c
else:
    c1=b/(b+d)*c

if b*d<0:
    if d<0:
        c2=0
    else:
        c2=c
else:
    c2=d/(b+d)*c

s2=abs(b)+abs(c1)**2/abs(b)
t2=abs(b)
if b<0:
    u2=0
else:
    if c1<0:
        u2=s2
    else:
        u2=t2
if c1<0:
    if b>0:
        y2=Ly-abs(c1)*Ly/(abs(c1)+abs(b))
    else:
        y2=Ly
else:
    y2=Ly

s3=abs(d)-abs(c2)+abs(c2)*(abs(d)+abs(c2))/abs(d)
t3=abs(d)
if d<0:
    u3=0
else:
    if c2<0:
        u3=s3
    else:
        u3=t3
if c2<0:
    x3=abs(d)*Lx/(abs(d+abs(c2)))
else:
    x3=Lx

if c2<0:
    u5=0
else:
    u5=abs(c)

uu=max(u1,u4)

#Soil Stress Under Ultimate Load (at Intermediate Point, Column Face)
if x3<Lx:
    s1=u3/x3*(x3-(Lx-Cx)/2)
else:
    s1=u5+(Lx+Cx)*(u3-u5)/(2*Lx)

if x1<Lx:
    s2=max(u1,u4)/x1*(x1-(Lx-Cx)/2)
else:
    s2=u2+(Lx+Cx)*(max(u1,u4)-u2)/(2*Lx)

if y4<Ly:
    s3=max(u1,u4)/y4*(y4-(Ly-Cy)/2)
else:
    s3=u3+(Ly+Cy)*(max(u1,u4)-u3)/(2*Ly)

if y2<Ly:
    s4=u2/y2*(y2-(Ly-Cy)/2)
else:
    s4=u5+(Ly+Cy)*(u2-u5)/(2*Ly)

#Required Moment
MUY=(s1+u3+s2+max(u1,u4))/4*(Lx/2-Cx/2)*(Lx/4-Cx/4)
MUX=(u2+s4+max(u1,u4)+s3)/4*(Ly/2-Cy/2)*(Ly/4-Cy/4)

#1면 전단에 의한 두께 산정
dy1=((s1+u3+max(u1,u4)+s2)/4*(Lx-Cx)/2)/((s1+u3+max(u1,u4)+s2)/4+0.75/6*(fc)**0.5*1000)
dx1=((s4+s3+max(u1,u4)+u2)/4*(Ly-Cy)/2)/((s4+s3+max(u1,u4)+u2)/4+0.75/6*(fc)**0.5*1000)

#2면 전단에 의한 두께 산정
sigma1=(max(u1,u4)+u2+u3+u5+s1+s2+s3+s4)/8
alpha=sigma1-0.75/3*(fc)**0.5*4*1000
beta=-(Cx+Cy)*sigma1-0.75/3*(fc)**0.5*2*(Cx+Cy)*1000
gamma=(Lx*Ly-Cx*Cy)*sigma1
xi1=(-beta+(beta**2-4*alpha*gamma)**0.5)/(2*alpha)
xi2=(-beta-(beta**2-4*alpha*gamma)**0.5)/(2*alpha)
if xi1<0:
    dxy2 = xi2
else:
    dxy2 = xi1

#기둥 압축 정착 길이에 의한 두께 산정
ldb = max(0.25*Dc*fy/(fc)**0.5, 0.043*Dc*fy)

#기초 두께 산정
if dx1>dy1:
    hx1=dx1+D/2000
    hy1=dy1+3*D/2000
else:
    hx1=dx1+3*D/2000
    hy1=dy1+D/2000
h=cc/1000+max(hx1,hy1,dxy2+D/1000,ldb/1000+2*D/1000)
H1=(((h*10)//1)+1)/10
print ("Foundation Depth : ", H1, "m with 100mm criteria")
H2=(((h*20)//1)+1)/20
print ("Foundation Depth : ", H2, "m with 50mm criteria")
print ("")

#1면 전단 확인
if MUX>MUY:
    dx=(H1*1000-cc-D/2)
    dy=(H1*1000-cc-3*D/2)
else:
    dx=(H1*1000-cc-3*D/2)
    dy=(H1*1000-cc-D/2)
print ("Effective Depth for Horizontal Direction, dx = ", dx, "mm")
print ("Effective Depth for Vertical Direction, dy = ", dy, "mm")
print ("")
Vuy1=((s1+u3+max(u1,u4)+s2)/4)*(Lx/2-Cx/2-dy/1000)*Ly
Vux1=((s4+s3+max(u1,u4)+u2)/4)*(Ly/2-Cy/2-dx/1000)*Lx
phiVcy1=0.75/6*fc**0.5*Ly*dy/1000*1000
phiVcx1=0.75/6*fc**0.5*Lx*dx/1000*1000
print ("Required 1-way Shear for Horizontal Direction, Vux1 = ", round(Vux1,1), "kN")
print ("1-way Shear Capacity for Horizontal Direction, phiVcx1 = ", round(phiVcx1,1), "kN")
print ("")
print ("Required 1-way Shear for Vertical Direction, Vuy1 = ", round(Vuy1,1), "kN")
print ("1-way Shear Capacity for Vertical Direction, phiVcy1 = ", round(phiVcy1,1), "kN")

#2면 전단 확인
dxy=(H1*1000-cc-D)/1000
Vu2=sigma1*(Lx*Ly-(Cx+dxy)*(Cy+dxy))
phiVc2=0.75/3*fc**0.5*(2*Cx+2*Cy+4*dxy)*dxy*1000
print("")
print ("Required Punching Shear : ", round(Vu2,1), "kN")
print ("Punching Shear Capacity, phiVc2 = ", round(phiVc2,1), "kN")

print ("")
print ("Required Moment about Y axis : ", round(MUY,1), "kNm/m")
b = 1000
Mu = MUY*10**6
dz = dy

a1 = ((-0.9*0.85*fc*b*dz)+((0.9*0.85*fc*b*dz)**2-4*(-0.9*0.85*fc*b*0.5)*(-Mu))**0.5)/(2*(-0.9*0.85*fc*b*0.5))
a2 = ((-0.9*0.85*fc*b*dz)-((0.9*0.85*fc*b*dz)**2-4*(-0.9*0.85*fc*b*0.5)*(-Mu))**0.5)/(2*(-0.9*0.85*fc*b*0.5))
if a1 < 0:
	a = a2
elif a2 < 0:
	a = a1
elif a1 > dz:
	a = a2
elif a2 > dz:
	a = a1

Asy = max(0.85*fc*a*b/fy, 0.0018*1000*H1*1000)
print ("Asy = ", round(Asy,1), "mm2/m")
print ("    = ", round(Asy*Ly,1), "mm2")
sy = int(1000/(Asy/((D/2)**2*3.141))/50)*50
print ("D",D,"@",sy, "(Provided : ", round((D/2)**2*3.14159265357989*1000/sy,1), "mm2/m)")
print ("")

print ("Required Moment about X axis : ", round(MUX,1), "kNm/m")
b = 1000
Mu = MUX*10**6
dz = dx

a1 = ((-0.9*0.85*fc*b*dz)+((0.9*0.85*fc*b*dz)**2-4*(-0.9*0.85*fc*b*0.5)*(-Mu))**0.5)/(2*(-0.9*0.85*fc*b*0.5))
a2 = ((-0.9*0.85*fc*b*dz)-((0.9*0.85*fc*b*dz)**2-4*(-0.9*0.85*fc*b*0.5)*(-Mu))**0.5)/(2*(-0.9*0.85*fc*b*0.5))
if a1 < 0:
	a = a2
elif a2 < 0:
	a = a1
elif a1 > dz:
	a = a2
elif a2 > dz:
	a = a1

Asx = max(0.85*fc*a*b/fy, 0.0018*1000*H1*1000)
print ("Asy = ", round(Asx,1), "mm2/m")
print ("    = ", round(Asx*Lx,1), "mm2")
sx = int(1000/(Asx/((D/2)**2*3.141592))/50)*50
print ("D",D,"@",sx, "(Provided : ", round((D/2)**2*3.14159265357989*1000/sx,1), "mm2/m)")

print ("")
print ("Allowable Soil Bearign Capacity : ", qa, "kPa")
print ("Service Max Soil Pressure :  ", round(us,1), "kPa")
print ("Factored Max Soil Pressure : ", round(uu,1), "kPa")
print ("")
