import pygame as py
import time
import sys
import platform
import asyncio
import geometry as geo
import save_manager as sa
import levels as le
import scoring as sc
import ui
import logger as lo

IS_WEB=(sys.platform=="emscripten")
OS_NAME = platform.system()

def load_font(size):
    if IS_WEB:
        return py.font.Font("msyh.ttc",size)#网页版用默认字体
    elif OS_NAME=="Windows":
        return py.font.Font("C:/Windows/Fonts/msyh.ttc",size)
    elif OS_NAME=="Darwin":#Mac
        return py.font.Font("/System/Library/Fonts/PingFang.ttc",size)
    else:#Linux
        return py.font.Font("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",size)
def get_save_name():
    if IS_WEB:
        return "compass_game_progress"#网页版用默认值
    else:
        return input("存档名:")

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
levels=[
    le.LEVEL_1,
    le.LEVEL_2,
    le.LEVEL_3,
    le.LEVEL_4,
    le.LEVEL_5,
    le.LEVEL_6,
    le.LEVEL_7,
    le.LEVEL_8_1,
    le.LEVEL_8_2,
    le.LEVEL_9_1,
    #le.LEVEL_9_2,
    le.LEVEL_10,
    le.LEVEL_11
]
checks=[
    le.check_triangle_complete,
    le.check_equilateral_triangle,
    le.check_60_degree,
    le.check_perpendicular_bisector,
    le.check_midpoint,
    le.check_inscribed_circle,
    le.check_inscribed_rhombus_rect,
    le.check_circle_center,
    le.check_circle_center,
    le.check_inscribed_square,
    #le.check_inscribed_square,
    le.check_angle_bisector,
    le.check_inscribed_rhombus_tri
]
tools=[
    {"name":"空","num":0},
    {"name":"点","num":1},
    {"name":"线","num":2},
    {"name":"圆","num":3},
    {"name":"垂直平分线","num":4},
    {"name":"角平分线","num":5}
]
screen_buttons=[
    {"name":"存档","action":"save","x":700,"y":10,"w":80,"h":28},
    {"name":"读档","action":"load","x":700,"y":43,"w":80,"h":28},
    {"name":"上一关","action":"prev","x":700,"y":76,"w":80,"h":28},
    {"name":"下一关","action":"next","x":700,"y":109,"w":80,"h":28},
    {"name":"重开","action":"reset","x":700,"y":142,"w":80,"h":28},
]
current_level=0
level=levels[current_level]
check=checks[current_level]
history=[]#一步一个字典{"type": "line", "data": (p1, p2)}
lines=[]
circles=[]
points=[]
score=0
grade=""
tool4=False
bisector_step=0
bisector_vertex=None
bisector_p1=None
tool5=False
last=None

print("0:空 1:点 2:线 3:圆 4:垂直平分线")
print("F1:存档 F2:读档")

#辅助函数
def if_add_point(pt,points,tolerance=3):
    #如果pt和points里的点距离小于tolerance就不再加了
    for i in points:
        if geo.distance(pt,i)<tolerance:
            return False
    points.append(pt)
    return True
def recalculate_intersections():
    global points
    #清空所有点，重新加端点、重新算所有交点
    points.clear()
    for i in level["given_points"]:
        points.append(i)
    for i in level["given_lines"]:
        if_add_point(i[0],points)
        if_add_point(i[1],points)
    for i in level["given_circles"]:
        if not level.get("hide_given_center",False):
            if_add_point(i[0],points)
            if_add_point(i[1],points)

    for i in lines:
        if_add_point(i[0],points)
        if_add_point(i[1],points)
    for i in circles:
        if_add_point(i[0],points)
        if_add_point(i[1],points)

    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            p1,p2=lines[i]
            p3,p4=lines[j]
            new_point=geo.line_line(p1,p2,p3,p4)
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
def draw_screen_buttons(screen,font,passed,current_level,total_levels):
    global screen_buttons
    for i in screen_buttons:
        enabled=True
        if i["action"]=="next" and not passed:
            enabled=False
        if i["action"]=="prev" and current_level==0:
            enabled=False
        if enabled:
            color=(220,220,220)
            text_=(0,0,0)
        else:
            color=(240,240,240)
            text_=(180,180,180)
        py.draw.rect(screen,color,(i["x"],i["y"],i["w"],i["h"]),border_radius=3)
        text=font.render(i["name"],True,text_)
        screen.blit(text,(i["x"]+i["w"]//2-text.get_width()//2,
                          i["y"]+i["h"]//2-text.get_height()//2))
def check_screen_button_click(pos):
    for i in screen_buttons:
        if i["x"]<=pos[0]<=i["x"]+i["w"] and\
           i["y"]<=pos[1]<=i["y"]+i["h"]:
            return i["action"]
    return None
def undo():
    #撤销最后一步
    global last,points,lines,circles,log
    if not history:
        return

    action=history.pop()
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
    log.info(f"撤销操作：{action['type']}")
def reset_level():
    global start_time,passed,last,score,grade,lines,circles,points,history,log
    global bisector_step,bisector_vertex,bisector_p1
    lines.clear()
    circles.clear()
    points.clear()
    history.clear()
    for i in level["given_points"]:
        points.append(i)
    for i in level["given_lines"]:
        lines.append((i[0],i[1]))
        if_add_point(i[0],points)
        if_add_point(i[1],points)
    for i in level["given_circles"]:
        circles.append((i[0],i[1]))
        if not level.get("hide_given_center",False):
            if_add_point(i[0],points)
            if_add_point(i[1],points)
    start_time=time.time()
    passed=False
    last=None
    bisector_step=0
    bisector_vertex=None
    bisector_p1=None
    log.info("重新开始关卡")
def draw_toolbar(screen,font,current_tool,tool4_unlocked,tool5_unlocked):
    # 画工具栏背景
    py.draw.rect(screen,(240,240,240),(0,640,800,60))
    #画分隔线
    #py.draw.line(screen,(180,180,180),(0,600-60),(800,600-60),2)
    
    #计算按钮起始x，居中排列
    total_width=len(tools)*100+(len(tools)-1)*10
    start_x=(800-total_width)//2
    button_y=650
    
    for i,tool in enumerate(tools):
        x=start_x+i*(100+10)
        #判断按钮状态
        if tool["num"]==4 and not tool4_unlocked:
            color=(200,200,200)
        elif tool["num"]==5 and not tool5_unlocked:
            color=(200,200,200)
        elif tool["num"]==current_tool:
            color=(100,150,255)
        else:
            color=(220,220,220)
        #画按钮
        py.draw.rect(screen,color,(x,button_y,100,40),border_radius=5)
        text=font.render(tool["name"],True,(0,0,0))
        screen.blit(text,(x+100//2-text.get_width()//2,
                          button_y+40//2-text.get_height()//2))
def check_toolbar_click(pos,tool4_unlocked,tool5_unlocked):
    total_width=len(tools)*100+(len(tools)-1)*10
    start_x=(800-total_width)//2
    button_y=640+20//2
    for i,tool in enumerate(tools):
        x=start_x+i*110
        if x<=pos[0]<=x+100 and button_y<=pos[1]<=button_y+40:
            if tool["num"]==4 and not tool4_unlocked:
                print("垂直平分线工具未解锁")
                return None
            elif tool["num"]==5 and not tool5_unlocked:
                print("角平分线工具未解锁")
                return None
            return tool["num"]
    return None

for i in level["given_points"]:
    points.append(i)
for i in level["given_lines"]:
    lines.append((i[0],i[1]))
    if_add_point(i[0], points)
    if_add_point(i[1], points)
for i in level["given_circles"]:
    circles.append((i[0],i[1]))
    if_add_point(i[0], points)
    if_add_point(i[1], points)

#主函数
async def main():
    global running,screen,font,clock,log,start_time
    #创建一个窗口
    py.init()
    font=load_font(24)
    screen=py.display.set_mode((800,700))
    py.display.set_caption("尺规作图2.1")
    log=lo.setup_logger()
    clock=py.time.Clock()
    start_time=time.time()
    global number,last,lines,circles,points,history
    global passed,pass_time,score,grade,tool4,bisector_step,bisector_p1,bisector_vertex,tool5
    global current_level,level,check
    while running:
        screen.fill(WHITE)

        step=sum(a["step_cost"]for a in history)
        e=sum(a["e_cost"]for a in history)
        if passed:
            elapsed=int(pass_time)
        else:
            elapsed=int(time.time()-start_time)
        ui.draw_hud(screen,font,step,e,elapsed,level)

        #加入预览点
        for i in level["given_points"]:
            py.draw.circle(screen,(0,180,0),i,6,0)
        for i in level["given_lines"]:
            py.draw.line(screen,(0,180,0),i[0],i[1],2)
        for i in level["given_circles"]:
            r=int(geo.distance(i[0],i[1]))
            py.draw.circle(screen,(0,180,0),i[0],r,2)

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
            elif number==4:
                py.draw.line(screen,RED,geo.perpendicular_bisector(last,mouse)[0],geo.perpendicular_bisector(last,mouse)[1],2)
            py.draw.circle(screen,BLUE,last,4,0)
        if number==5:
            mouse=geo.snap_to_point(py.mouse.get_pos(),points)
            if bisector_step==1:
                #已选第一边点，正在选顶点：画第一边点到鼠标的线
                py.draw.line(screen,RED,bisector_p1,mouse,1)
            elif bisector_step==2:
                #已选第一边点+顶点，正在选第二边点：画角平分线预览
                preview=geo.angle_bisector(bisector_vertex,bisector_p1,mouse)
                py.draw.line(screen,RED,preview[0],preview[1],1)
            if bisector_p1:
                py.draw.circle(screen,BLUE,bisector_p1,4,0)
            if bisector_vertex:
                py.draw.circle(screen,BLUE,bisector_vertex,4,0)
        for i in py.event.get():
            if i.type==py.QUIT:
                running=False

            elif i.type==py.KEYDOWN:
                #从2.1开始禁用数字键切换工具
                """
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
                elif i.key==py.K_4:
                    if not tool4:
                        print("垂直平分线工具未解锁，请先通过第四关")
                        log.warning("尝试使用未解锁工具：垂直平分线")
                    else:
                        number=4
                        last=None
                        print("已切换至：垂直平分线")
                elif i.key==py.K_5:
                    if not tool5:
                        print("角平分线工具未解锁，请先通过第十关")
                        log.warning("尝试使用未解锁工具：角平分线")
                    else:
                        number=5
                        last=None
                        bisector_step=0
                        bisector_vertex=None
                        bisector_p1=None

                        print("已切换至：角平分线")
                """
                if i.key==py.K_ESCAPE:
                    last=None
                    bisector_step=0
                    bisector_vertex=None
                    bisector_p1=None
                elif i.key==py.K_z and i.mod&py.KMOD_CTRL:
                    undo()
                elif i.key==py.K_r and passed:
                    reset_level()

                elif i.key==py.K_a:
                    if current_level==0:
                        print("已是第一关")
                    else:
                        current_level=(current_level-1)%len(levels)
                        level=levels[current_level]
                        check=checks[current_level]
                        reset_level()
                        bisector_step=0
                        bisector_vertex=None
                        bisector_p1=None
                        log.info(f"切换到关卡：{level['name']}")
                elif i.key==py.K_d:
                    if not passed:
                        print("请先通过当前关卡")
                        log.warning(f"关卡未通过，无法切换下一关：{level['name']}")
                    else:
                        current_level=(current_level+1)%len(levels)
                        level=levels[current_level]
                        check=checks[current_level]
                        reset_level()
                        bisector_step=0
                        bisector_vertex=None
                        bisector_p1=None
                        log.info(f"切换到关卡：{level['name']}")
                elif i.key==py.K_F1:
                    name=get_save_name()
                    sa.save_progress(name,current_level)
                elif i.key==py.K_F2:
                    name=get_save_name()
                    lv=sa.load_progress(name)
                    if lv is not None:
                        current_level=lv
                        level=levels[current_level]
                        check=checks[current_level]
                        reset_level()
                        if current_level>=3:
                            tool4=True
                        else:
                            tool4=False
                        if current_level>=10:
                            tool5=True
                        else:
                            tool5=False
                        log.info(f"读档：{name}，恢复到第{current_level+1}关")
            elif i.type==py.MOUSEBUTTONDOWN:
                if i.button==1:
                    clicked=check_toolbar_click(i.pos, tool4,tool5)
                    if clicked is not None:
                        number=clicked
                        last=None
                        bisector_step=0
                        bisector_vertex=None
                        bisector_p1=None
                        continue
                    btn=check_screen_button_click(i.pos)
                    if btn is not None:
                        if btn=="save":
                            name=get_save_name()
                            sa.save_progress(name,current_level)
                            log.info(f"存档：{name}")
                        elif btn=="load":
                            name=get_save_name()
                            lv=sa.load_progress(name)
                            if lv is not None:
                                current_level=lv
                                level=levels[current_level]
                                check=checks[current_level]
                                reset_level()
                                if current_level>=3:
                                    tool4=True
                                else:
                                    tool4=False
                                if current_level>=10:
                                    tool5=True
                                else:
                                    tool5=False
                                log.info(f"读档：{name}，恢复到第{current_level+1}关")
                        elif btn=="prev":
                            if current_level==0:
                                print("已是第一关")
                            else:
                                current_level=(current_level-1)%len(levels)
                                level=levels[current_level]
                                check=checks[current_level]
                                reset_level()
                                bisector_step=0
                                bisector_vertex=None
                                bisector_p1=None
                                log.info(f"切换到关卡：{level['name']}")
                        elif btn=="next":
                            if not passed:
                                print("请先通过当前关卡")
                                log.warning(f"关卡未通过，无法切换下一关：{level['name']}")
                            else:
                                current_level=(current_level+1)%len(levels)
                                level=levels[current_level]
                                check=checks[current_level]
                                reset_level()
                                bisector_step=0
                                bisector_vertex=None
                                bisector_p1=None
                                log.info(f"切换到关卡：{level['name']}")
                        elif btn=="reset":
                            reset_level()
                        continue                   
                    click=geo.snap_to_point(i.pos,points)
                    if i.pos[1]>=640:
                        continue
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
                            if geo.distance(last,click)<3:
                                print("两点距离太近")
                                log.warning("两点距离太近！")
                                last=None
                                continue
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
                                log.info(f"绘制直线 {last}→{click}")

                            else:
                                print("这条线已经存在")
                                log.warning("共线直线已存在，操作忽略")
                            last=None
                    elif number==3:
                        if last is None:
                            last=click
                            if_add_point(last,points)
                        else:
                            if geo.distance(last,click)<3:
                                print("两点距离太近")
                                log.warning("两点距离太近！")
                                last=None
                                continue                        
                            center=last
                            r=geo.distance(last,click)
                            flag=False
                            for j in circles:
                                j_r=geo.distance(j[0],j[1])
                                if geo.is_same_circle(center,r,j[0],j_r):
                                    flag=True
                                    break
                            if not flag:
                                circles.append((last,click))
                                if_add_point(click,points)

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
                                log.info(f"绘制圆 圆心{center} 半径{r}")

                            else:
                                print("这个圆已存在")
                                log.warning("重复圆已存在，操作忽略")
                            last=None
                    elif number==4:
                        if last is None:
                            last=click
                            if_add_point(last,points)
                        else:
                            if geo.distance(last,click)<3:
                                print("两点距离太近")
                                log.warning("两点距离太近！")
                                last=None
                                continue
                            new_line=geo.perpendicular_bisector(last,click)
                            flag=False
                            for j in lines:
                                if geo.is_same_line(new_line[0],new_line[1],j[0],j[1]):
                                    flag=True
                                    break
                            if not flag:
                                lines.append(new_line)
                                if_add_point(click,points)

                                #求交点
                                for j in lines:
                                    if j==new_line:
                                        continue
                                    new_point=geo.line_line(j[0],j[1],new_line[0],new_line[1])
                                    if new_point is not None:
                                        if_add_point(new_point,points)
                                for j in circles:
                                    r=geo.distance(j[0],j[1])
                                    new_point=geo.line_circle(new_line[0],new_line[1],j[0],r)
                                    if new_point is not None:
                                        for k in new_point:
                                            if_add_point(k,points)
                                history.append({"type":"line","data":(new_line[0],new_line[1]),"step_cost":1,"e_cost":3})
                                log.info(f"绘制 {last}→{click} 的垂直平分线 {new_line[1]}→{new_line[0]}")

                            else:
                                print("这个垂直平分线已存在")
                                log.warning("重复垂直平分线已存在，操作忽略")
                            last=None
                    elif number==5:
                        if not tool5:
                            print("角平分线工具未解锁")
                            continue
                        if bisector_step==0:
                            #第一次点击：第一条边上的点
                            bisector_p1=click
                            if_add_point(bisector_p1,points)
                            bisector_step=1
                        elif bisector_step==1:
                            #第二次点击：角顶点
                            if geo.distance(bisector_p1,click)<3:
                                print("两点距离太近")
                                bisector_step=0
                                bisector_p1=None
                                continue
                            bisector_vertex=click
                            if_add_point(bisector_vertex, points)
                            bisector_step=2
                        elif bisector_step==2:
                            if geo.distance(bisector_vertex,click)<3:
                                print("两点距离太近")
                                continue
                            bisector_p2=click
                            if_add_point(bisector_p2,points)
                            new_line=geo.angle_bisector(bisector_vertex,bisector_p1,bisector_p2)
                            flag=False
                            for j in lines:
                                if geo.is_same_line(new_line[0],new_line[1],j[0],j[1]):
                                    flag=True
                                    break
                            if not flag:
                                lines.append(new_line)
                                if_add_point(click,points)

                                #求交点
                                for j in lines:
                                    if j==new_line:
                                        continue
                                    new_point=geo.line_line(j[0],j[1],new_line[0],new_line[1])
                                    if new_point is not None:
                                        if_add_point(new_point,points)
                                for j in circles:
                                    r=geo.distance(j[0],j[1])
                                    new_point=geo.line_circle(new_line[0],new_line[1],j[0],r)
                                    if new_point is not None:
                                        for k in new_point:
                                            if_add_point(k,points)
                                history.append({"type":"line","data":(new_line[0],new_line[1]),"step_cost":1,"e_cost":4})
                                log.info(f"绘制角平分线 {bisector_vertex}")

                            else:
                                print("这个角平分线已存在")
                                log.warning("重复角平分线已存在，操作忽略")
                            bisector_step=0
                            bisector_vertex=None
                            bisector_p1=None

        if not passed:
            if check(points,lines,circles,level["given_points"]):
                passed=True
                if current_level==3:
                    tool4=True
                    log.info("解锁工具：垂直平分线")
                if current_level==10:
                    tool5=True
                    log.info("解锁工具：角平分线")
                pass_time=time.time()-start_time
                score,grade=sc.calculate_score(step,e,pass_time,level)
                sa.save_score(current_level+1,step,e,int(pass_time),grade)
                log.info(f"过关！步数{step} 元素数{e} 用时{int(pass_time)}s 评级{grade}")
        if passed:
            ui.draw_pass_screen(screen,step,e,int(pass_time),level,score,grade)

        draw_toolbar(screen,font,number,tool4,tool5)
        draw_screen_buttons(screen,font,passed,current_level,len(levels))
        py.display.flip()
        #控制帧率
        clock.tick(60)
        #pygbag必须
        await asyncio.sleep(0)

    lo.log_shutdown()
    py.quit()

asyncio.run(main())