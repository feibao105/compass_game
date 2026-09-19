#这是一个工具包属于compass_game，是测算交点的包
from math import sqrt

def distance(p1,p2):
    a=p1[0]-p2[0]
    b=p1[1]-p2[1]
    return sqrt(a**2+b**2)

def line_line(p1,p2,p3,p4):
    #两条直线的交点p1->p2,p3->p4
    den=(p1[0]-p2[0])*(p3[1]-p4[1])-(p1[1]-p2[1])*(p3[0]-p4[0])
    if abs(den)<0.0001:
        #平行
        return None
    t=((p1[0]-p3[0])*(p3[1]-p4[1])-(p1[1]-p3[1])*(p3[0]-p4[0]))/den
    x=p1[0]+t*(p2[0]-p1[0])
    y=p1[1]+t*(p2[1]-p1[1])
    return (x,y)
def line_circle(p1,p2,center,r):
    #直线和圆的交点p1->p2,以c为中心r为半径的圆
    dx=p2[0]-p1[0]
    dy=p2[1]-p1[1]
    fx=p1[0]-center[0]
    fy=p1[1]-center[1]

    #一元二次方程参数
    a=dx**2+dy**2
    b=2*(fx*dx+fy*dy)
    c=fx**2+fy**2-r**2

    #根的判别式：Δ
    disc=b*b-4*a*c
    if disc<0:
        return []#无交点

    sqrt_disc=sqrt(disc)
    t1=(-b-sqrt_disc)/(2*a)
    t2=(-b+sqrt_disc)/(2*a)

    pos1=(p1[0]+t1*dx,p1[1]+t1*dy)
    pos2=(p1[0]+t2*dx,p1[1]+t2*dy)
    if abs(disc)<0.0001:
        return [pos1]
    else:
        return [pos1,pos2]
def circle_circle(c1,r1,c2,r2):
    dx=c2[0]-c1[0]
    dy=c2[1]-c1[1]
    d=sqrt(dx**2+dy**2)
    if d>r1+r2+0.0001:
        return []#外离
    elif d<abs(r1-r2)-0.0001:
        return []#内含
    elif d<0.0001:
        return []#圆心重合

    a=(r1**2-r2**2+d**2)/(2*d)
    h=sqrt(r1**2-a**2)

    mx=c1[0]+a*dx/d
    my=c1[1]+a*dy/d

    ox=-dy*h/d
    oy=dx*h/d

    pos1=(mx+ox,my+oy)
    pos2=(mx-ox,my-oy)

    if h<0.0001:
        return [pos1]#相切
    else:
        return [pos1,pos2]
