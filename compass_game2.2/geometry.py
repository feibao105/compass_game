#这是一个工具包属于compass_game，是一个工具包
from math import sqrt

#距离工具
def distance(p1,p2):
    a=p1[0]-p2[0]
    b=p1[1]-p2[1]
    return sqrt(a**2+b**2)

#直线函数
def extend_line(p1,p2,length=2000):
    #把线段p1-p2向两端各延长length像素
    dx=p2[0]-p1[0]
    dy=p2[1]-p1[1]
    d=sqrt(dx**2+dy**2)
    if d<0.0001:
        return (p1,p2)

    ux=dx/d
    uy=dy/d

    new_p1=(p1[0]-ux*length,p1[1]-uy*length)
    new_p2=(p2[0]+ux*length,p2[1]+uy*length)

    return (new_p1,new_p2)
def is_same_line(p1,p2,p3,p4,tolerance=0.0001):
    #判断两条直线p1-p2和p3-p4是否共线
    x1,y1=p1
    x2,y2=p2
    x3,y3=p3
    x4,y4=p4
    cross1=(x2-x1)*(y3-y1)-(y2-y1)*(x3-x1)
    cross2=(x2-x1)*(y4-y1)-(y2-y1)*(x4-x1)
    return abs(cross1)<tolerance and abs(cross2)<tolerance

#圆工具
def is_same_circle(p1,r1,p2,r2,tolerance=3):
    #判断两个圆是否相同（圆心距离小于tolerance，半径差小于tolerance）
    return distance(p1,p2)<tolerance and abs(r1-r2)<tolerance

#垂直平分线工具
def perpendicular_bisector(p1,p2,length=2000):
    #返回垂直平分线的两个端点
    mid=((p1[0]+p2[0])/2,(p1[1]+p2[1])/2)
    dx=p2[0]-p1[0]
    dy=p2[1]-p1[1]
    d=sqrt(dx**2+dy**2)
    if d<0.0001:
        return (mid,mid)
    ux=-dy/d
    uy=dx/d
    pos1=(mid[0]-ux*length,mid[1]-uy*length)
    pos2=(mid[0]+ux*length,mid[1]+uy*length)
    return (pos1,pos2)

#角平分线工具
def angle_bisector(vertex, p1, p2, length=2000):
    vx, vy=vertex
    #两条边的方向向量
    d1x=p1[0]-vx
    d1y=p1[1]-vy
    d2x=p2[0]-vx
    d2y=p2[1]-vy
    
    #单位化
    len1=sqrt(d1x**2+d1y**2)
    len2=sqrt(d2x**2+d2y**2)
    if len1<0.0001 or len2<0.0001:
        return(vertex,vertex)
    u1x=d1x/len1
    u1y=d1y/len1
    u2x=d2x/len2
    u2y=d2y/len2
    
    #角平分线方向=两单位向量之和
    dx=u1x+u2x
    dy=u1y+u2y
    d_len=sqrt(dx**2+dy**2)
    if d_len<0.0001:
        return (vertex,vertex)
    
    #延长到指定长度
    end_x=vx+(dx/d_len)*length
    end_y=vy+(dy/d_len)*length
    
    return (vertex,(end_x,end_y))

#交点工具
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
    h=sqrt(max(0.0,r1**2-a**2))

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

#吸附工具
def snap_to_point(pos,points,threshold=15):
    #把鼠标位置吸附到最近的已有点
    if not points:
        return pos

    near=pos
    minn=100000000.0
    for i in points:
        if minn>=distance(pos,i):
            minn=distance(pos,i)
            near=i
        else:
            continue

    if minn<threshold:
        return near
    else:
        return pos
