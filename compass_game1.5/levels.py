#这是一个工具包属于compass_game，是记录关卡的包
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
    mid=(A[0]+B[0])/2,(A[1]+B[1])/2
    
    for q in lines:
        p1,p2=q
        line_len=geo.distance(p1,p2)
        if line_len<1:
            continue
        cross=abs((p2[0]-p1[0])*(mid[1]-p1[1])-(p2[1]-p1[1])*(mid[0]-p1[0]))
        dist=cross/line_len
        if dist<5:
            lx=p2[0]-p1[0]
            ly=p2[1]-p1[1]
            dot=abx*lx+aby*ly
            if abs(dot)<50:
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
