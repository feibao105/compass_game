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
        lx=p2[0]-p1[0]
        ly=p2[1]-p1[1]
        #垂直判定（归一化）
        cos_theta=abs(abx*lx+aby*ly)/(ab_len*line_len)
        if cos_theta>=0.05:
            continue
        #中点到直线的距离
        cross=abs(lx*(mid[1]-p1[1])-ly*(mid[0]-p1[0]))
        dist=cross/line_len
        if dist>=5:
            continue
        t=((mid[0]-p1[0])*lx+(mid[1]-p1[1])*ly)/(line_len*line_len)
        if not (-0.02<=t<=1.02):
            continue
        if line_len<ab_len*0.5:
            continue
        has_proof=False
        for p in points:
            if p==A or p==B:
                continue
            #点到AB的距离要够大（排除线AB自动产生的"中点"交点）
            dab=abs(abx*(p[1]-A[1])-aby*(p[0]-A[0]))/ab_len
            if dab<10:
                continue
            #到A、B等距（垂直平分线的定义）
            if abs(geo.distance(p,A)-geo.distance(p,B))>=8:
                continue
            #这个点要真的在这条线上
            dp=abs(lx*(p[1]-p1[1])-ly*(p[0]-p1[0]))/line_len
            if dp<8:
                has_proof=True
                break
        if has_proof:
            return True
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

LEVEL_12={
    "name":"三十度角",
    "goal":"想办法作三十度角",
    "given_points":[(300,430),(520,430)],
    "given_lines":[[(300,430),(520,430)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":100
}
def check_30_degree(points,lines,circles,given_points):
    #检查是否存在一条从A出发的线（或点），与AB夹角约60度
    #用点积算夹角：cosθ=(AB·AQ)/(|AB|*|AQ|)
    #cos(30°)=√3/2，所以检查abs(cos-0.866)<0.05
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
        if abs(cos_theta-0.866)<0.05:
            for j in lines:
                if (geo.distance(j[0],A)<3) and (geo.distance(j[1],q)<3) or\
                   (geo.distance(j[0],q)<3) and (geo.distance(j[1],A)<3):
                    return True
    return False

LEVEL_13={
    "name":"二倍角",
    "goal":"想办法作已知角的二倍角",
    "given_points":[(320,440),(540,440),(476,284)],
    "given_lines":[[(320,440),(540,440)],[(320,440),(476,284)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":100
}
def check_double_angle(points,lines,circles,given_points):
    O,B,C=given_points        #O=顶点(320,440)，B=水平边(540,440)，C=斜边(476,284)
    obx=B[0]-O[0]
    oby=B[1]-O[1]
    ob_len=geo.distance(O,B)
    for q in lines:
        p1,p2=q
        #找从O出发的线（哪个端点是O都行）
        if geo.distance(p1,O)<3:
            other=p2
        elif geo.distance(p2,O)<3:
            other=p1
        else:
            continue
        qx=other[0]-O[0]
        qy=other[1]-O[1]
        q_len=geo.distance(O,other)
        if q_len<1:
            continue
        #①和OB垂直（90°=45°的两倍）
        cos_theta=abs(obx*qx+oby*qy)/(ob_len*q_len)
        if cos_theta>=0.05:
            continue
        #②必须往上走（在OB的上方那一侧，跟C同侧）
        if other[1]>=O[1]:
            continue
        #③线段不能太短，防止点一小点蒙混
        if q_len<80:
            continue
        return True
    return False

LEVEL_14={
    "name":"分割矩形",
    "goal":"将矩形分割成面积相等的两部分",
    "given_points":[(300,260),(480,260),(480,400),(300,400),(600,200)],
    "given_lines":[[(300,260),(480,260)],[(480,260),(480,400)],[(480,400),(300,400)],[(300,400),(300,260)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":60
}
def check_bisect_rectangle(points,lines,circles,given_points):
    A,B,C,D,P=given_points
    M=((A[0]+C[0])/2,(A[1]+C[1])/2)
    for i in lines:
        t=geo.project_t(P,i[0],i[1])
        if not (-0.02<=t<=1.02):
            continue
        if geo.point_line_dist(P,i[0],i[1])>=5:
            continue
        if geo.point_line_dist(M,i[0],i[1])>=5:
            continue
        if not (-0.02<=geo.project_t(P,i[0],i[1])<=1.02):
            continue
        if not (-0.02<=geo.project_t(M,i[0],i[1])<=1.02):
            continue
        return True
    return False

LEVEL_15_1={
    "name":"过直线外一点作垂线",
    "goal":"作该直线的垂线",
    "given_points":[(240,450),(540,450),(390,270)],
    "given_lines":[[(240,450),(540,450)]],
    "given_circles":[],
    "best_steps":2,
    "best_e":4,
    "time":120
}
LEVEL_15_2={
    "name":"过直线外一点作垂线",
    "goal":"作该直线的垂线",
    "given_points":[(240,450),(540,450),(390,270)],
    "given_lines":[[(240,450),(540,450)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":120
}
LEVEL_16_1={
    "name":"过直线上一点作垂线",
    "goal":"作该直线的垂线",
    "given_points":[(260,420),(540,420),(400,420)],
    "given_lines":[[(260,420),(540,420)]],
    "given_circles":[],
    "best_steps":1,
    "best_e":4,
    "time":120
}
LEVEL_16_2={
    "name":"过直线上一点作垂线",
    "goal":"作该直线的垂线",
    "given_points":[(260,420),(540,420),(400,420)],
    "given_lines":[[(260,420),(540,420)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":120
}
def check_perpendicular_through_point(points,lines,circles,given_points):
    A,B,P=given_points
    for i in lines:
        if geo.point_line_dist(P,i[0],i[1])>=5:
            continue
        #cosθ=|(CD·q)|/(|CD|·|q|)
        cos_theta=abs((B[0]-A[0])*(i[1][0]-i[0][0])+(B[1]-A[1])*(i[1][1]-i[0][1]))/(geo.distance(A,B)*geo.distance(i[0],i[1]))
        if cos_theta>=0.05:
            continue
        t=geo.project_t(P,i[0],i[1])
        if not (-0.02<=t<=1.02):
            continue
        if geo.distance(i[0],i[1])<80:
            continue
        return True
    return False

LEVEL_17_1={
    "name":"作与圆切于某点的直线",
    "goal":"与圆切于某点的直线",
    "given_points":[(380,360),(440,280)],
    "given_lines":[],
    "given_circles":[((380,360),(440,280))],
    "best_steps":2,
    "best_e":4,
    "time":120
}
LEVEL_17_2={
    "name":"作与圆切于某点的直线",
    "goal":"与圆切于某点的直线",
    "given_points":[(380,360),(440,280)],
    "given_lines":[],
    "given_circles":[((380,360),(440,280))],
    "best_steps":3,
    "best_e":3,
    "time":150
}
def check_tangent_to_circle(points,lines,circles,given_points):
    O,T=given_points
    for i in lines:
        if geo.point_line_dist(T,i[0],i[1])>=5:
            continue
        cos_theta=abs((T[0]-O[0])*(i[1][0]-i[0][0])+(T[1]-O[1])*(i[1][1]-i[0][1]))/(geo.distance(O,T)*geo.distance(i[0],i[1]))
        if cos_theta>=0.05:
            continue
        t=geo.project_t(T,i[0],i[1])
        if not (-0.02<=t<=1.02):
            continue
        if geo.distance(i[0],i[1])<50:
            continue
        return True
    return False

LEVEL_18={
    "name":"作与直线相切的圆",
    "goal":"给定圆心作圆,使其与直线相切",
    "given_points":[(400,300)],
    "given_lines":[[(260,470),(540,470)]],
    "given_circles":[],
    "best_steps":2,
    "best_e":4,
    "time":150    
}
def check_circle_tangent_to_line(points,lines,circles,given_points):
    O=given_points[0]
    r=geo.point_line_dist(O,lines[0][0],lines[0][1])
    for i in circles:
        if geo.distance(O,i[0])>=5:
            continue
        __r=geo.distance(i[0],i[1])
        if (__r-r)>=8:
            continue
        t=geo.project_t(O,lines[0][0],lines[0][1])
        if not (-0.02<=t<=1.02):
            continue
        return True
    return False

LEVEL_19={
    "name":"作菱形的内切圆",
    "goal":"再菱形中作一个内切圆",
    "given_points":[(400,240),(510,360),(400,480),(290,360)],
    "given_lines":[[(400,240),(510,360)],[(510,360),(400,480)],[(400,480),(290,360)],[(290,360),(400,240)]],
    "given_circles":[],
    "best_steps":4,
    "best_e":6,
    "time":120
}
def check_inscribed_circle_rhombus(points,lines,circles,given_points):
    A,B,C,D=given_points
    M=((A[0]+C[0])/2,(A[1]+C[1])/2)
    r=geo.point_line_dist(M,C,D)
    for i in circles:
        __r=geo.distance(i[0],i[1])
        if geo.distance(i[0],M)>8:
            continue
        if abs(__r-r)>5:
            continue
        return True
    return False

LEVEL_20={
    "name":"已知中点作弦",
    "goal":"已知弦的中点，作出这条弦",
    "given_points":[(360,270)],
    "given_lines":[],
    "given_circles":[((400,320),(520,320))],
    "best_steps":2,
    "best_e":4,
    "time":90
}
def check_chord_through_midpoint(points,lines,circles,given_points):
    #M=弦的中点（给定），O=圆心（给定圆自带）
    #弦的性质：弦垂直于OM，且过M
    M=given_points[0]
    O=circles[0][0]
    om=geo.distance(O,M)
    if om<1:
        return False
    for i in lines:
        if geo.point_line_dist(M,i[0],i[1])>=5:
            continue
        t=geo.project_t(M,i[0],i[1])
        if not (-0.02<=t<=1.02):
            continue
        #弦要够长，防止点一小段蒙混
        if geo.distance(i[0],i[1])<100:
            continue
        #垂直判定：弦的方向·OM的方向≈0
        lx,ly=i[1][0]-i[0][0],i[1][1]-i[0][1]
        L=geo.distance(i[0],i[1])
        cos_theta=abs(lx*(M[0]-O[0])+ly*(M[1]-O[1]))/(L*om)
        if cos_theta>=0.05:
            continue
        return True
    return False

LEVEL_21_1={
    "name":"垂心为O的三角形",
    "goal":"作一条线段连接角的两边，使三角形的垂心为O",
    "given_points":[(400,430),(600,430),(540,260),(490,388)],
    "given_lines":[[(400,430),(600,430)],[(400,430),(540,260)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":7,
    "time":150
}
LEVEL_21_2={
    "name":"垂心为O的三角形",
    "goal":"作一条线段连接角的两边，使三角形的垂心为O",
    "given_points":[(400,430),(600,430),(540,260),(490,388)],
    "given_lines":[[(400,430),(600,430)],[(400,430),(540,260)]],
    "given_circles":[],
    "best_steps":6,
    "best_e":6,
    "time":150
}
def check_orthocenter_O(points,lines,circles,given_points):
    #B=顶点，P1/P2=两边方向，O=垂心
    #D在BP1上、E在BP2上，要满足：BO⊥DE，DO⊥BE，EO⊥BD
    B,P1,P2,O=given_points
    def on_ray(p,V,Px,tol=5):
        if geo.point_line_dist(p,V,Px)>=tol:
            return False
        t=geo.project_t(p,V,Px)
        return t>0.05#在射线上且不是顶点
    def perp(a1,a2,b1,b2):
        ax,ay=a2[0]-a1[0],a2[1]-a1[1]
        bx,by=b2[0]-b1[0],b2[1]-b1[1]
        la=(ax*ax+ay*ay)**0.5
        lb=(bx*bx+by*by)**0.5
        if la<1 or lb<1:
            return False
        return abs(ax*bx+ay*by)/(la*lb)<0.05
    for i in lines:
        p,q=i
        for d,e in [(p,q),(q,p)]:
            if not on_ray(d,B,P1):
                continue
            if not on_ray(e,B,P2):
                continue
            if not perp(B,O,d,e):
                continue
            if not perp(d,O,B,e):
                continue
            if not perp(e,O,B,d):
                continue
            return True
    return False

LEVEL_22={
    "name":"外心为O的三角形",
    "goal":"作一条线段连接角的两边，使三角形的外心为O",
    "given_points":[(400,430),(600,430),(540,260),(486,390)],
    "given_lines":[[(400,430),(600,430)],[(400,430),(540,260)]],
    "given_circles":[],
    "best_steps":2,
    "best_e":2,
    "time":120
}
def check_circumcenter_O(points,lines,circles,given_points):
    #B=顶点，P1/P2=两边方向，O=外心
    #D在BP1上、E在BP2上，要满足：|OD|=|OE|=|OB|
    B,P1,P2,O=given_points
    ob=geo.distance(O,B)
    def on_ray(p,V,Px,tol=5):
        if geo.point_line_dist(p,V,Px)>=tol:
            return False
        t=geo.project_t(p,V,Px)
        return t>0.05
    for i in lines:
        p,q=i
        for d,e in [(p,q),(q,p)]:
            if not on_ray(d,B,P1):
                continue
            if not on_ray(e,B,P2):
                continue
            if abs(geo.distance(O,d)-ob)>=8:
                continue
            if abs(geo.distance(O,e)-ob)>=8:
                continue
            return True
    return False

LEVEL_23={
    "name":"BD=DM=ME",
    "goal":"在BA、BC上求点D、E，使BD=DM=ME",
    "given_points":[(400,440),(580,300),(220,300),(400,350)],
    "given_lines":[[(400,440),(580,300)],[(400,440),(220,300)]],
    "given_circles":[],
    "best_steps":4,
    "best_e":6,
    "time":180
}
def check_bd_dm_me(points,lines,circles,given_points):
    #B=顶点，A/C=两边方向，M=角内一点
    #D在BA上、E在BC上，BD=DM=ME，且DM、ME要真画出来
    B,A,C,M=given_points
    def on_ray(p,V,Px,tol=5):
        if geo.point_line_dist(p,V,Px)>=tol:
            return False
        t=geo.project_t(p,V,Px)
        return t>0.05
    def line_exists(p1,p2):
        for l in lines:
            if (geo.distance(l[0],p1)<5 and geo.distance(l[1],p2)<5) or\
               (geo.distance(l[0],p2)<5 and geo.distance(l[1],p1)<5):
                return True
        return False
    for d in points:
        if not on_ray(d,B,A):
            continue
        bd=geo.distance(B,d)
        if bd<20:
            continue
        if abs(geo.distance(d,M)-bd)>=8:
            continue
        for e in points:
            if not on_ray(e,B,C):
                continue
            if abs(geo.distance(M,e)-bd)>=8:
                continue
            if line_exists(d,M) and line_exists(M,e):
                return True
    return False

LEVEL_24_1={
    "name":"切于定点的圆",
    "goal":"作圆经过点A，并与直线相切于点B",
    "given_points":[(320,240),(460,420)],
    "given_lines":[[(280,420),(620,420)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":7,
    "time":120
}
LEVEL_24_2={
    "name":"切于定点的圆",
    "goal":"作圆经过点A，并与直线相切于点B",
    "given_points":[(320,240),(460,420)],
    "given_lines":[[(280,420),(620,420)]],
    "given_circles":[],
    "best_steps":6,
    "best_e":6,
    "time":120
}
def check_circle_tangent_at_point(points,lines,circles,given_points):
    #圆心=B处垂线与AB垂直平分线的交点
    A,B=given_points
    p1,p2=lines[0]#给定直线排在最前面，玩家画的线都在后面
    lx,ly=p2[0]-p1[0],p2[1]-p1[1]
    L=geo.distance(p1,p2)
    for i in circles:
        c=i[0]
        r=geo.distance(i[0],i[1])
        #圆要过A
        if abs(geo.distance(c,A)-r)>=5:
            continue
        #切点B要在圆上
        if abs(geo.distance(c,B)-r)>=5:
            continue
        #CB要垂直于直线（切线的性质）
        cb=geo.distance(c,B)
        if cb<1:
            continue
        cos_theta=abs(lx*(B[0]-c[0])+ly*(B[1]-c[1]))/(L*cb)
        if cos_theta>=0.05:
            continue
        return True
    return False

LEVEL_25_1={
    "name":"梯形底边的中点",
    "goal":"作一条经过梯形底边中点的直线",
    "given_points":[(240,440),(540,440),(470,300),(330,300)],
    "given_lines":[[(240,440),(540,440)],[(540,440),(470,300)],[(470,300),(330,300)],[(330,300),(240,440)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":7,
    "time":120
}
LEVEL_25_2={
    "name":"梯形底边的中点",
    "goal":"作一条经过梯形底边中点的直线",
    "given_points":[(240,440),(540,440),(470,300),(330,300)],
    "given_lines":[[(240,440),(540,440)],[(540,440),(470,300)],[(470,300),(330,300)],[(330,300),(240,440)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":3,
    "time":120
}
def check_trapezoid_base_midpoint(points,lines,circles,given_points):
    #底边=A(240,440) B(540,440)，中点M=(390,440)
    #经典作法：两条对角线交点K + 两腰延长交点P，直线PK过M
    #防蒙混：①对角线交点K必须真实存在（对角线得真画）
    #        ②过关线必须同时穿过M和K（瞄准竖线过不了）
    A,B,C,D=given_points
    M=((A[0]+B[0])/2,(A[1]+B[1])/2)
    #K=两条对角线的交点，先算理论位置，再看玩家有没有把它作出来
    K=geo.line_line(A,C,B,D)
    if K is None:
        return False
    k_exists=False
    for p in points:
        if geo.distance(p,K)<8:
            k_exists=True
            break
    if not k_exists:
        return False
    for i in lines:
        if geo.is_same_line(i[0],i[1],A,B):
            continue#底边自己不算
        if geo.point_line_dist(M,i[0],i[1])>=5:
            continue
        if geo.point_line_dist(K,i[0],i[1])>=5:
            continue#必须过K，竖线瞄M的在这里被刷掉
        t=geo.project_t(M,i[0],i[1])
        if not (-0.02<=t<=1.02):
            continue
        if geo.distance(i[0],i[1])<80:
            continue
        return True
    return False

LEVEL_26_1={
    "name":"45度角",
    "goal":"以给定射线为一边，作出45度角",
    "given_points":[(300,430),(520,430)],
    "given_lines":[[(300,430),(520,430)]],
    "given_circles":[],
    "best_steps":2,
    "best_e":7,
    "time":100
}
LEVEL_26_2={
    "name":"45度角",
    "goal":"以给定射线为一边，作出45度角",
    "given_points":[(300,430),(520,430)],
    "given_lines":[[(300,430),(520,430)]],
    "given_circles":[],
    "best_steps":3,
    "best_e":5,
    "time":100
}
def check_45_degree(points,lines,circles,given_points):
    #cos(45°)=√2/2≈0.7071
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
        if abs(cos_theta-0.7071)<0.05:
            for j in lines:
                if (geo.distance(j[0],A)<3) and (geo.distance(j[1],q)<3) or\
                   (geo.distance(j[0],q)<3) and (geo.distance(j[1],A)<3):
                    return True
    return False

LEVEL_27_1={
    "name":"45度菱形",
    "goal":"以给定射线为一边，作顶角为45度的菱形",
    "given_points":[(260,420),(460,420)],
    "given_lines":[[(260,420),(460,420)]],
    "given_circles":[],
    "best_steps":5,
    "best_e":12,
    "time":240
}
LEVEL_27_2={
    "name":"45度菱形",
    "goal":"以给定射线为一边，作顶角为45度的菱形",
    "given_points":[(260,420),(460,420)],
    "given_lines":[[(260,420),(460,420)]],
    "given_circles":[],
    "best_steps":7,
    "best_e":7,
    "time":240
}
def check_rhombus_45(points,lines,circles,given_points):
    #AB为一边，找E使|AE|=|AB|且∠BAE=45°，第四顶点F=B+E-A
    #AE、EF、FB三条边要真画出来（AB是给定边）
    A,B=given_points
    ab=geo.distance(A,B)
    abx,aby=B[0]-A[0],B[1]-A[1]
    def line_exists(p1,p2):
        for l in lines:
            if (geo.distance(l[0],p1)<5 and geo.distance(l[1],p2)<5) or\
               (geo.distance(l[0],p2)<5 and geo.distance(l[1],p1)<5):
                return True
        return False
    for E in points:
        ae=geo.distance(A,E)
        if ae<10 or abs(ae-ab)>=8:
            continue
        cos_theta=(abx*(E[0]-A[0])+aby*(E[1]-A[1]))/(ab*ae)
        if abs(cos_theta-0.7071)>=0.05:
            continue
        F=(B[0]+E[0]-A[0],B[1]+E[1]-A[1])
        f=None
        for p in points:
            if geo.distance(p,F)<8:
                f=p
                break
        if f is None:
            continue
        if line_exists(A,E) and line_exists(E,f) and line_exists(B,f):
            return True
    return False