#这是一个工具包属于compass_game，是记录关卡的包
import geometry as geo
LEVEL_1={
    "name":"教程：作三角形",
    "goal":"连接三个点，组成三角形",
    "given_points":[(200,400),(400,150),(600,400)],
    "best_steps":3,
    "best_e":3,
    "time":60
}
def check_triangle_complete(lines,given_points):
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