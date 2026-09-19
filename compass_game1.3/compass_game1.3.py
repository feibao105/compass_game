import pygame as py
import sys
import geometry as geo
import time
import levels as le
import scoring as sc
import ui

#创建一个窗口
py.init()
font=py.font.Font("C:/Windows/Fonts/msyh.ttc",24)
screen=py.display.set_mode((800,600))
py.display.set_caption("尺规作图1.3")
clock=py.time.Clock()
start_time=time.time()

WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,225)
RED=(225,0,0)
LIGHT_GRAY=(200,200,200)
LIGHT_RED=(255,200,200)

running=True
passed=False
pass_time=0
number=0
history=[]#一步一个字典{"type": "line", "data": (p1, p2)}
lines=[]
circles=[]
points=[]
score=0
grade=""
last=None

print("0:空 1:点 2:线 3:圆")

#辅助函数
def if_add_point(pt,points,tolerance=3):
    #如果pt和points里的点距离小于tolerance就不再加了
    for i in points:
        if geo.distance(pt,i)<tolerance:
            return False
    points.append(pt)
    return True
def recalculate_intersections():
    #清空所有点，重新加端点、重新算所有交点
    points.clear()

    for i in lines:
        if_add_point(i[0],points)
        if_add_point(i[1],points)
    for i in circles:
        if_add_point(i[0],points)
        if_add_point(i[1],points)

    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            p1, p2=lines[i]
            p3, p4=lines[j]
            new_point=geo.line_line(p1, p2, p3, p4)
            if new_point is not None:
                if_add_point(new_point, points)
    for i in lines:
        for j in circles:
            r=geo.distance(j[0],j[1])
            new_point=geo.line_circle(i[0],i[1],j[0],r)
            for k in new_point:
                if_add_point(k, points)
    for i in range(len(circles)):
        for j in range(i+1,len(circles)):
            c1, e1=circles[i]
            c2, e2=circles[j]
            r1=geo.distance(c1,e1)
            r2=geo.distance(c2,e2)
            new_point=geo.circle_circle(c1,r1,c2,r2)
            for k in new_point:
                if_add_point(k, points)
def undo():
    #撤销最后一步
    global last
    if not history:
        return

    action = history.pop()
    if action["type"]=="point":
        points.remove(action["data"])
    elif action["type"]=="line":
        lines.remove(action["data"])
    elif action["type"]=="circle":
        circles.remove(action["data"])
    #重新算交点
    recalculate_intersections()

    #清空未完成的选择
    last=None

for i in le.LEVEL_1["given_points"]:
    points.append(i)

while running:
    screen.fill(WHITE)

    step=sum(a["step_cost"]for a in history)
    e=sum(a["e_cost"]for a in history)
    elapsed=int(time.time()-start_time)
    ui.draw_hud(screen,font,step,e,elapsed,le.LEVEL_1)

    #加入预览点
    for i in le.LEVEL_1["given_points"]:
        py.draw.circle(screen,(0,180,0),i,6,0)

    #每一帧重绘
    for i in lines:
        p1,p2=geo.extend_line(i[0],i[1])
        py.draw.line(screen,LIGHT_GRAY,p1,p2,1)
        py.draw.line(screen,BLACK,i[0],i[1],2)
    for i in circles:
        #利用勾股定理算距离
        r=int(((i[0][0]-i[1][0])**2+(i[0][1]-i[1][1])**2)**0.5)
        py.draw.circle(screen,BLACK,i[0],r,2)
    #从1.2开始，不显示点
    #for i in points:
    #    py.draw.circle(screen,BLUE,i,4,0)
    #跟着鼠标画预览
    if last is not None:
        mouse=py.mouse.get_pos()
        mouse=geo.snap_to_point(mouse,points)
        if number==2:
            p1,p2=geo.extend_line(last,mouse)
            py.draw.line(screen,LIGHT_RED,p1,p2,1)
            py.draw.line(screen,RED,last,mouse,2)
        elif number==3:
            r=int(((last[0]-mouse[0])**2+(last[1]-mouse[1])**2)**0.5)
            py.draw.circle(screen,RED,last,r,1)
        py.draw.circle(screen,BLUE,last,4,0)
    for i in py.event.get():
        if i.type==py.QUIT:
            running=False

        elif i.type==py.KEYDOWN:
            if i.key==py.K_0:
                number=0
                last=None
                print("已切换至：空")
            elif i.key==py.K_1:
                number=1
                last=None
                print("已切换至：点")
            elif i.key==py.K_2:
                number=2
                last=None
                print("已切换至：线")
            elif i.key==py.K_3:
                number=3
                last=None
                print("已切换至：圆")
            elif i.key==py.K_ESCAPE:
                last=None
            elif i.key==py.K_z and i.mod&py.KMOD_CTRL:
                undo()
            elif i.key==py.K_r and passed:
                lines.clear()
                circles.clear()
                points.clear()
                history.clear()
                for i in le.LEVEL_1["given_points"]:
                    points.append(i)
                start_time=time.time()
                passed=False
                last=None
        elif i.type==py.MOUSEBUTTONDOWN:
            if i.button==1:
                click=geo.snap_to_point(i.pos,points)
                if number==0:
                    print("当前选择：空")
                    continue
                if number==1:
                    if if_add_point(click,points):#成功才记录
                        history.append({"type":"point","data":click,"step_cost":0,"e_cost":0})
                elif number==2:
                    if last is None:
                        last=click
                        if_add_point(last,points)
                    else:
                        flag=False
                        for j in lines:
                            if geo.is_same_line(last,click,j[0],j[1]):
                                flag=True
                                break
                        if not flag:
                            lines.append((last,click))
                            if_add_point(click,points)

                            #求交点
                            for j in lines:
                                if j==(last,click):
                                    continue
                                new_point=geo.line_line(j[0],j[1],last,click)
                                if new_point is not None:
                                    if_add_point(new_point,points)
                            for j in circles:
                                r=geo.distance(j[0],j[1])
                                new_point=geo.line_circle(last,click,j[0],r)
                                if new_point is not None:
                                    for k in new_point:
                                        if_add_point(k,points)
                            history.append({"type":"line","data":(last,click),"step_cost":1,"e_cost":1})

                        else:
                            print("这条线已经存在")
                        last=None
                elif number==3:
                    if last is None:
                        last=click
                        if_add_point(last,points)
                    else:
                        circles.append((last,click))
                        if_add_point(click,points)
                        center=last
                        r=geo.distance(last,click)

                        #求交点
                        for j in lines:
                            new_point=geo.line_circle(j[0],j[1],center,r)
                            if new_point is not None:
                                for k in new_point:
                                    if_add_point(k,points)
                        for j in circles:
                            temp=geo.distance(j[0],j[1])
                            if j[0]==center and j[1]==click:
                                continue
                            new_point=geo.circle_circle(j[0],temp,center,r)
                            if new_point is not None:
                                for k in new_point:
                                    if_add_point(k,points)
                        history.append({"type":"circle","data":(last,click),"step_cost":1,"e_cost":1})
                        last=None

    if not passed:
        if le.check_triangle_complete(lines,le.LEVEL_1["given_points"]):
            passed=True
            pass_time=time.time()-start_time
            score,grade=sc.calculate_score(step,e,pass_time,le.LEVEL_1)
    if passed:
        ui.draw_pass_screen(screen,step,e,int(pass_time),le.LEVEL_1,score,grade)
    

    py.display.flip()
    #控制帧率
    clock.tick(60)


py.quit()
sys.exit()