#这是一个工具包属于compass_game，是记录关卡的包
from itertools import combinations
import geometry as geo
LEVEL_1={
    "name":"教程：作三角形",
    "goal":"连接三个点，组成三角形",
    "given_points":[(200,400),(400,150),(600,400)],
    "given_lines":[],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":60
}
def check_triangle_complete(points,lines,circles,given_points):
    A,B,C=given_points
    needed=[(A,B),(B,C),(C,A)]
    for x,y in needed:
        flag=False
        for i in lines:
            if (geo.distance(i[0],x)<3 and geo.distance(i[1],y)<3)or\
               (geo.distance(i[0],y)<3 and geo.distance(i[1],x)<3):
                flag=True
                break
        if not flag:
            return False
    return True

LEVEL_2={
    "name":"作等边三角形",
    "goal":"以两点为边，作出等边三角形的第三个顶点",
    "given_points":[(300, 350),(500, 350)],
    "given_lines":[[(300, 350),(500, 350)]],
    "given_circles":[],
    "best_steps":4,
    "best_e":4,
    "time":60
}
def check_equilateral_triangle(points,lines,circles,given_points):
    A,B=given_points
    ab=geo.distance(A,B)
    for i in points:
        ac=geo.distance(i,A)
        bc=geo.distance(i,B)
        if abs(ac-ab)<5 and abs(bc-ab)<5:
            has_ac=False
            has_bc=False
            for j in lines:
                if (geo.distance(j[0],A)<3) and (geo.distance(j[1],i)<3) or\
                   (geo.distance(j[0],i)<3) and (geo.distance(j[1],A)<3):
                    has_ac=True
                if (geo.distance(j[0],B)<3) and (geo.distance(j[1],i)<3) or\
                   (geo.distance(j[0],i)<3) and (geo.distance(j[1],B)<3):
                    has_bc=True
            if has_ac and has_bc:
                return True
    return False

LEVEL_3={
    "name":"60度角",
    "goal":"以给定射线为一边，作出60度角",
    "given_points":[(250,350),(550,350)],
    "given_lines":[[(250,350),(550,350)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":60
}
def check_60_degree(points,lines,circles,given_points):
    #检查是否存在一条从A出发的线（或点），与AB夹角约60度
    #用点积算夹角：cosθ=(AB·AQ)/(|AB|*|AQ|)
    #cos(60°)=0.5，所以检查abs(cos-0.5)<0.05
    A,B=given_points
    abx=B[0]-A[0]
    aby=B[1]-A[1]
    ab_len=geo.distance(A,B)
    
    for q in points:
        if geo.distance(q,A)<5 or geo.distance(q,B)<5:
            continue
        qx=q[0]-A[0]
        qy=q[1]-A[1]
        q_len=geo.distance(q,A)
        if q_len<5:
            continue
        cos_theta=(abx*qx+aby*qy)/(ab_len*q_len)
        if abs(cos_theta-0.5)<0.05:
            for j in lines:
                if (geo.distance(j[0],A)<3) and (geo.distance(j[1],q)<3) or\
                   (geo.distance(j[0],q)<3) and (geo.distance(j[1],A)<3):
                    return True
    return False

LEVEL_4={
    "name":"垂直平分线",
    "goal":"作出给定线段的垂直平分线",
    "given_points":[(300,350),(500,350)],
    "given_lines":[[(300,350),(500,350)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":60
}
def check_perpendicular_bisector(points,lines,circles,given_points):
    #检查是否存在一条线，是AB的垂直平分线
    A,B=given_points
    abx=B[0]-A[0]
    aby=B[1]-A[1]
    ab_len=geo.distance(A,B)
    mid=(A[0]+B[0])/2,(A[1]+B[1])/2
    
    for q in lines:
        p1,p2=q
        line_len=geo.distance(p1,p2)
        if line_len<1:
            continue
        #中点到直线的距离
        cross=abs((p2[0]-p1[0])*(mid[1]-p1[1])-(p2[1]-p1[1])*(mid[0]-p1[0]))
        dist=cross/line_len
        if dist<5:
            lx=p2[0]-p1[0]
            ly=p2[1]-p1[1]
            dot=abx*lx+aby*ly
            cos_theta=abs(dot)/(ab_len*line_len)#归一化
            if cos_theta<0.05:
                return True
    return False

LEVEL_5={
    "name":"作中点",
    "goal":"作出给定线段的中点",
    "given_points":[(300, 350),(500,350)],
    "given_lines":[],
    "given_circles":[],
    "best_steps":2,
    "best_e":4,
    "time":60
}

def check_midpoint(points, lines, circles, given_points):
    A,B=given_points
    mid=((A[0]+B[0])/2,(A[1]+B[1])/2)
    for p in points:
        if geo.distance(p,mid)<5:
            #for i in lines:
            #    if (geo.distance(i[0],A)<3) and (geo.distance(i[1],p)<3) or\
            #       (geo.distance(i[0],p)<3) and (geo.distance(i[1],A)<3):
                    return True
    return False

LEVEL_6={
    "name":"正方形的内切圆",
    "goal":"作出给定正方形的内切圆",
    "given_points":[(300, 200),(500, 200),(500, 400),(300, 400)],
    "given_lines":[
        [(300,200),(500,200)],
        [(500,200),(500,400)],
        [(500,400),(300,400)],
        [(300,400),(300,200)]
    ],
    "given_circles":[],
    "best_steps":3,
    "best_e":5,
    "time":90
}

def check_inscribed_circle(points,lines,circles,given_points):
    """
    检查是否存在一个圆，是正方形的内切圆
    条件：圆心在正方形中心，半径≈边长的一半
    """
    A,B,C,D=given_points
    #正方形中心（对角线交点）
    center=((A[0]+C[0])/2,(A[1]+C[1])/2)
    side=geo.distance(A, B)
    target_r=side/2
    
    for circle in circles:
        c=circle[0]
        r=geo.distance(circle[0],circle[1])
        if geo.distance(c,center)<5 and abs(r-target_r)<5:
            return True
    return False

LEVEL_7={
    "name":"矩形的内接菱形",
    "goal":"作内接菱形",
    "given_points":[(200,150),(600,150),(600,450),(200,450)],
    "given_lines":[((200,150),(600,150)),((600,150),(600,450)),
                  ((600,450),(200,450)),((200,450),(200,150))],
    "given_circles":[],
    "best_steps":3,
    "best_e":5,
    "time":120
}
def check_inscribed_rhombus_rect(points,lines,circles,given_points):
    A,B,C,D=given_points

    def line_exists(p1,p2):
        for i in lines:
            if (geo.distance(i[0],p1)<8 and geo.distance(i[1],p2)<8) or\
               (geo.distance(i[0],p2)<8 and geo.distance(i[1],p1)<8):
                return True
        return False

    def on_segment(p,a,b):
        return min(a[0],b[0])-8<=p[0]<=max(a[0],b[0])+8 and\
               min(a[1],b[1])-8<=p[1]<=max(a[1],b[1])+8

    def check_diagonal(d1,d2):
        mid=((d1[0]+d2[0])/2,(d1[1]+d2[1])/2)
        dx=d2[0]-d1[0]
        dy=d2[1]-d1[1]
        pb1=(mid[0]+dy*1000,mid[1]-dx*1000)
        pb2=(mid[0]-dy*1000,mid[1]+dx*1000)
        sides=[(A,B),(B,C),(C,D),(D,A)]
        intersections=[]
        for s1,s2 in sides:
            p=geo.line_line(pb1,pb2,s1,s2)
            if p is not None and on_segment(p,s1,s2):
                dup=False
                for q in intersections:
                    if geo.distance(p,q)<8:
                        dup=True
                        break
                if not dup:
                    intersections.append(p)
        if len(intersections)!=2:
            return False
        e,f=intersections
        # d1→e 和 d2→f 与矩形边共线，被去重拒绝，不用查
        # 只查两条斜线：e→d2 和 f→d1（e、f顺序两种都试）
        return (line_exists(e,d2) and line_exists(f,d1)) or\
               (line_exists(f,d2) and line_exists(e,d1))

    if check_diagonal(A,C):
        return True
    if check_diagonal(B,D):
        return True
    return False


LEVEL_8_1={
    "name":"做圆心",
    "goal":"找出圆的圆心",
    "given_points":[],
    "given_lines":[],
    "given_circles":[((400,300),(550,300))],
    "hide_given_center":True,
    "best_steps":2,
    "best_e":6,
    "time":90
}
LEVEL_8_2={
    "name":"做圆心",
    "goal":"找出圆的圆心",
    "given_points":[],
    "given_lines":[],
    "given_circles":[((400,300),(550,300))],
    "hide_given_center":True,
    "best_steps":5,
    "best_e":5,
    "time":90
}
def check_circle_center(points,lines,circles,given_points):
    center=circles[0][0]
    #检查points里是否有一个点距离圆心<5像素
    for p in points:
        if geo.distance(p, center)<8:
            return True
    return False

LEVEL_9_1={
    "name":"做内接正方形",
    "goal":"在圆内作内接正方形",
    "given_points":[(400,240)],  #圆上一点
    "given_lines":[],
    "given_circles":[((400,320),(400,240))],
    "best_steps":6,
    "best_e":8,
    "time":120
}
LEVEL_9_2={
    "name":"做内接正方形",
    "goal":"在圆内作内接正方形",
    "given_points":[(400,240)],  #圆上一点
    "given_lines":[],
    "given_circles":[((400,320),(400,240))],
    "best_steps":7,
    "best_e":7,
    "time":120
}
def check_inscribed_square(points,lines,circles,given_points):
    center=circles[0][0]
    r=geo.distance(circles[0][0],circles[0][1])
    #圆上的点（去重）
    on_circle=[]
    for p in points:
        if abs(geo.distance(p,center)-r)<5:
            if all(geo.distance(p,q)>=3 for q in on_circle):
                on_circle.append(p)
    if len(on_circle)<4:
        return False
    #6个两两距离：应恰好4条边(≈r√2)、2条对角线(≈2r)
    side=r*(2**0.5)
    diag=2*r
    for quad in combinations(on_circle,4):
        n_side=0
        n_diag=0
        sides=[]
        for i in range(4):
            for j in range(i+1,4):
                d=geo.distance(quad[i],quad[j])
                if abs(d-side)<8:
                    n_side+=1
                    sides.append((quad[i],quad[j]))
                elif abs(d-diag)<8:
                    n_diag+=1
        if n_side!=4 or n_diag!=2:
            continue
        ok=True
        #4条边必须真的画出来
        for p1,p2 in sides:
            found=False
            for line in lines:
                if (geo.distance(line[0],p1)<5 and geo.distance(line[1],p2)<5) or\
                   (geo.distance(line[0],p2)<5 and geo.distance(line[1],p1)<5):
                    found=True
                    break
            if not found:
                ok=False
                break
        if ok:
            return True
    return False

LEVEL_10={
    "name":"做角平分线",
    "goal":"作出角的平分线",
    "given_points":[(200,450),(500,450),(300,200)],
    "given_lines":[((200,450),(500,450)),((200,450),(300,200))],
    "given_circles":[],
    "best_steps":2,
    "best_e":4,
    "time":90
}
def check_angle_bisector(points,lines,circles,given_points):
    vertex=given_points[0]
    p1=given_points[1]
    p2=given_points[2]
    bisector=geo.angle_bisector(vertex,p1,p2)
    for line in lines:
        p,q=line
        L=geo.distance(p,q)
        if L<1:
            continue
        #顶点到这条直线的距离
        cross=abs((q[0]-p[0])*(vertex[1]-p[1])-(q[1]-p[1])*(vertex[0]-p[0]))
        if cross/L>=5:
            continue
        if geo.is_same_line(p,q,bisector[0],bisector[1]):
            return True
    return False

LEVEL_11={
    "name":"三角形的内接菱形",
    "goal":"在三角形内作内接菱形",
    "given_points":[(200,450),(600,450),(400,150)],
    "given_lines":[((200,450),(600,450)),((600,450),(400,150)),((400,150),(200,450))],
    "given_circles":[],
    "best_steps":4,
    "best_e":9,
    "time":150
}
def check_inscribed_rhombus_tri(points,lines,circles,given_points):
    A,B,C=given_points
    sides={A:(B,C),B:(A,C),C:(A,B)}

    def line_exists(p1,p2):
        for l in lines:
            if (geo.distance(l[0],p1)<5 and geo.distance(l[1],p2)<5) or\
               (geo.distance(l[0],p2)<5 and geo.distance(l[1],p1)<5):
                return True
        return False

    def line_covers(p1,p2):
        #存在一条从p1出发、且覆盖到p2的线（p2可以在线段中间）
        for l in lines:
            a,b=l
            if not (geo.distance(a,p1)<5 or geo.distance(b,p1)<5):
                continue
            L=geo.distance(a,b)
            if L<1:
                continue
            cross=abs((b[0]-a[0])*(p2[1]-a[1])-(b[1]-a[1])*(p2[0]-a[0]))
            if cross/L<5 and on_segment(p2,a,b):
                return True
        return False

    def on_segment(p,a,b,tol=5):
        cross=abs((b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0]))
        if cross>tol*geo.distance(a,b):
            return False
        return min(a[0],b[0])-tol<=p[0]<=max(a[0],b[0])+tol and\
               min(a[1],b[1])-tol<=p[1]<=max(a[1],b[1])+tol

    def find_point_near(target,cand,tol=5):
        for p in cand:
            if geo.distance(p,target)<tol:
                return p
        return None

    for V,(P,Q) in sides.items():
        R=None
        if V==A: R=(B,C)
        elif V==B: R=(A,C)
        else: R=(A,B)
        for E in points:
            if not on_segment(E,V,P):
                continue
            for F in points:
                if not on_segment(F,V,Q):
                    continue
                s=geo.distance(V,E)
                if s<10 or abs(geo.distance(V,F)-s)>=5:
                    continue
                G=(E[0]+F[0]-V[0],E[1]+F[1]-V[1])
                if not on_segment(G,R[0],R[1]):
                    continue
                g=find_point_near(G,points)
                if g is None:
                    continue
                #从V出发的两边：覆盖即可（给定边也算）；两条斜边：必须真画
                if line_covers(V,E) and line_covers(V,F) and\
                   line_exists(E,g) and line_exists(F,g):
                    return True
    return False