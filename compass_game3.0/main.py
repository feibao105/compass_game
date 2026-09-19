#导入系统自带包
import pygame as py
import time
import sys
import platform
import asyncio
#导入工具包
import geometry as geo
import save_manager as sa
import levels as le
import scoring as sc
import ui
import logger as lo
import lang

IS_WEB=(sys.platform=="emscripten")
OS_NAME=platform.system()

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
    #le.LEVEL_8_1,
    #le.LEVEL_8_2,
    le.LEVEL_9_1,
    #le.LEVEL_9_2,
    le.LEVEL_10,
    le.LEVEL_11,
    le.LEVEL_12,
    le.LEVEL_13,
    le.LEVEL_14,
    le.LEVEL_15_1,
    le.LEVEL_15_2,
    le.LEVEL_16_1,
    le.LEVEL_16_2,
    le.LEVEL_17_1,
    le.LEVEL_17_2,
    le.LEVEL_18,
    le.LEVEL_19,
    le.LEVEL_20,
    le.LEVEL_21_1,
    le.LEVEL_21_2,
    le.LEVEL_22,
    le.LEVEL_23,
    le.LEVEL_24_1,
    le.LEVEL_24_2,
    #le.LEVEL_25_1,
    #le.LEVEL_25_2,
    le.LEVEL_26_1,
    le.LEVEL_26_2,
    #le.LEVEL_27_1,
    #le.LEVEL_27_2
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
    le.check_inscribed_rhombus_tri,
    le.check_30_degree,
    le.check_double_angle,
    le.check_bisect_rectangle,
    le.check_perpendicular_through_point,
    le.check_perpendicular_through_point,
    le.check_perpendicular_through_point,
    le.check_perpendicular_through_point,
    le.check_tangent_to_circle,
    le.check_tangent_to_circle,
    le.check_circle_tangent_to_line,
    le.check_inscribed_circle_rhombus,
    le.check_chord_through_midpoint,
    le.check_orthocenter_O,
    le.check_orthocenter_O,
    le.check_circumcenter_O,
    le.check_bd_dm_me,
    le.check_circle_tangent_at_point,
    le.check_circle_tangent_at_point,
    #le.check_trapezoid_base_midpoint,
    le.check_trapezoid_base_midpoint,
    le.check_45_degree,
    le.check_45_degree,
    #le.check_rhombus_45,
    #le.check_rhombus_45
]
tools=[
    {"name":"空","num":0},
    {"name":"点","num":1},
    {"name":"线","num":2},
    {"name":"圆","num":3},
    {"name":"垂直平分线","num":4},
    {"name":"角平分线","num":5},
    {"name":"垂线","num":6}
]
screen_buttons=[
    {"name":"存档","action":"save","x":700,"y":10,"w":80,"h":28},
    {"name":"读档","action":"load","x":700,"y":43,"w":80,"h":28},
    {"name":"上一关","action":"prev","x":700,"y":76,"w":80,"h":28},
    {"name":"下一关","action":"next","x":700,"y":109,"w":80,"h":28},
    {"name":"重开","action":"reset","x":700,"y":142,"w":80,"h":28},
    {"name":"撤销","action":"undo","x":700,"y":175,"w":80,"h":28},
    {"name":"选关","action":"select","x":700,"y":208,"w":80,"h":28},
    {"name":"中/EN","action":"lang","x":700,"y":241,"w":80,"h":28},
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
tool6=False
selecting=False
select_page=0
last=None

#存档用的辅助函数
def get_save_name():
    if IS_WEB or (platform.system()=="Android") or (sys.platform=="android"):
        return "compass_game_progress"#网页版用默认值
    else:
        return input("存档名:")

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
    for a,i in enumerate(circles):
        if a<len(level["given_circles"]):
            continue
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

"""for i in level["given_points"]:
    points.append(i)
for i in level["given_lines"]:
    lines.append((i[0],i[1]))
    if_add_point(i[0], points)
    if_add_point(i[1], points)
for i in level["given_circles"]:
    circles.append((i[0],i[1]))
    if not level.get("hide_given_center",False):
        if_add_point(i[0], points)
        if_add_point(i[1], points)"""
def refresh_tool_unlocks():
    #根据当前关卡恢复工具解锁状态
    global tool4,tool5,tool6
    tool4=(current_level>=3)
    tool5=(current_level>=10)
    tool6=(current_level>=18)

#主函数
async def main():
    global running,screen,font,clock,log,start_time
    #创建一个窗口
    py.init()
    lang.load_lang()
    font=ui.load_font(24)
    if IS_WEB:
        screen=py.display.set_mode((800,700))
    else:
        screen=py.display.set_mode((800,700),py.SCALED)
    py.display.set_caption("尺规作图3.0")
    log=lo.setup_logger()
    clock=py.time.Clock()
    start_time=time.time()
    global number,last,lines,circles,points,history
    global passed,pass_time,score,grade,tool4,bisector_step,bisector_p1,bisector_vertex,tool5,tool6
    global current_level,level,check,selecting,select_page
    while running:
        ui.draw_paper(screen)

        step=sum(a["step_cost"]for a in history)
        e=sum(a["e_cost"]for a in history)
        if passed:
            elapsed=int(pass_time)
        else:
            elapsed=int(time.time()-start_time)
        ui.draw_hud(screen,font,step,level["best_steps"],e,level["best_e"],elapsed,level,current_level,len(levels))

        #加入预览
        for i in level["given_points"]:
            py.draw.circle(screen,ui.PT_GIVEN,i,6,0)
        for i in level["given_lines"]:
            py.draw.line(screen,ui.GIVEN,i[0],i[1],2)
        for i in level["given_circles"]:
            r=int(geo.distance(i[0],i[1]))
            py.draw.circle(screen,ui.GIVEN,i[0],r,2)

        #每一帧重绘
        for i in lines:
            p1,p2=geo.extend_line(i[0],i[1])
            py.draw.line(screen,LIGHT_GRAY,p1,p2,1)
            py.draw.line(screen,ui.INK,i[0],i[1],2)
        for i in circles:
            #利用勾股定理算距离
            r=int(((i[0][0]-i[1][0])**2+(i[0][1]-i[1][1])**2)**0.5)
            py.draw.circle(screen,ui.INK,i[0],r,2)
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
            elif number==6:
                target=geo.nearest_line(mouse,lines)
                if target is not None:
                    preview=geo.perpendicular_through_point(last,target[0],target[1])
                    if preview is not None:
                        py.draw.line(screen,RED,preview[0],preview[1],2)
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

        #自动吸附点高亮
        _m=py.mouse.get_pos()
        _snap=geo.snap_to_point(_m,points)
        if geo.distance(_m,_snap)>0.5:
            py.draw.circle(screen,(0,150,255),_snap,8,2)

        #监听键盘
        for i in py.event.get():
            if i.type==py.QUIT:
                running=False

            elif i.type==py.KEYDOWN:
                if i.key==py.K_ESCAPE or i.key==py.K_AC_ESCAPE:
                    last=None
                    bisector_step=0
                    bisector_vertex=None
                    bisector_p1=None
                    if selecting:
                        selecting=False
                        continue
            elif i.type==py.MOUSEBUTTONDOWN:
                if i.button==1:
                    if selecting:
                        scores=sa.load_scores()
                        r=ui.check_level_select_click(i.pos,levels,scores,select_page)
                        if r=="close":
                            selecting=False
                        elif r=="prev_page":
                            select_page-=1
                        elif r=="next_page":
                            select_page+=1
                        elif r is not None:
                            current_level=r
                            level=levels[current_level]
                            check=checks[current_level]
                            reset_level()
                            refresh_tool_unlocks()
                            selecting=False
                            log.info(f"选关跳转到：{level['name']}")
                        continue
                    clicked=ui.check_toolbar_click(i.pos, tool4,tool5,tool6,tools)
                    if clicked is not None:
                        number=clicked
                        last=None
                        bisector_step=0
                        bisector_vertex=None
                        bisector_p1=None
                        continue
                    btn=ui.check_screen_button_click(i.pos,screen_buttons)
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
                                refresh_tool_unlocks()
                                log.info(f"读档：{name}，恢复到第{current_level+1}关")
                        elif btn=="prev":
                            if current_level!=0:
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
                        elif btn=="undo":
                            undo()
                        elif btn=="select":
                            selecting=True
                            select_page=0
                        elif btn=="lang":
                            lang.toggle()
                        continue

                    #没有点工具栏，画图                  
                    click=geo.snap_to_point(i.pos,points)
                    if i.pos[1]>=640:
                        continue

                    if number==0:
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

                                #求交点
                                recalculate_intersections()

                                history.append({"type":"line","data":(last,click),"step_cost":1,"e_cost":1})
                                log.info(f"绘制直线 {last}→{click}")

                            else:
                                log.warning("共线直线已存在，操作忽略")
                            last=None
                    elif number==3:
                        if last is None:
                            last=click
                            if_add_point(last,points)
                        else:
                            if geo.distance(last,click)<3:
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

                                #求交点
                                recalculate_intersections()

                                history.append({"type":"circle","data":(last,click),"step_cost":1,"e_cost":1})
                                log.info(f"绘制圆 圆心{center} 半径{r}")

                            else:
                                log.warning("重复圆已存在，操作忽略")
                            last=None
                    elif number==4:
                        if last is None:
                            last=click
                            if_add_point(last,points)
                        else:
                            if geo.distance(last,click)<3:
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

                                #求交点
                                recalculate_intersections()

                                history.append({"type":"line","data":(new_line[0],new_line[1]),"step_cost":1,"e_cost":3})
                                log.info(f"绘制 {last}→{click} 的垂直平分线 {new_line[1]}→{new_line[0]}")

                            else:
                                log.warning("重复垂直平分线已存在，操作忽略")
                            last=None
                    elif number==5:
                        if not tool5:
                            continue
                        if bisector_step==0:
                            #第一次点击：第一条边上的点
                            bisector_p1=click
                            if_add_point(bisector_p1,points)
                            bisector_step=1
                        elif bisector_step==1:
                            #第二次点击：角顶点
                            if geo.distance(bisector_p1,click)<3:
                                bisector_step=0
                                bisector_p1=None
                                continue
                            bisector_vertex=click
                            if_add_point(bisector_vertex, points)
                            bisector_step=2
                        elif bisector_step==2:
                            if geo.distance(bisector_vertex,click)<3:
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
                                recalculate_intersections()

                                history.append({"type":"line","data":(new_line[0],new_line[1]),"step_cost":1,"e_cost":4})
                                log.info(f"绘制角平分线 {bisector_vertex}")

                            else:
                                log.warning("重复角平分线已存在，操作忽略")
                            bisector_step=0
                            bisector_vertex=None
                            bisector_p1=None
                    elif number==6:
                        if not tool6:
                            continue
                        if last is None:
                            last=click
                            if_add_point(last,points)
                        else:
                            target=geo.nearest_line(i.pos,lines)
                            if target is None:
                                log.warning("没点到线！")
                                last=None
                                continue
                            new_line=geo.perpendicular_through_point(last,target[0],target[1])

                            if new_line is None:
                                last=None
                                continue
                            
                            flag=False
                            for j in lines:
                                if geo.is_same_line(new_line[0],new_line[1],j[0],j[1]):
                                    flag=True
                                    break
                            
                            if not flag:
                                lines.append(new_line)

                                #求交点
                                recalculate_intersections()

                                history.append({"type":"line","data":(new_line[0],new_line[1]),"step_cost":1,"e_cost":3})
                                log.info(f"绘制 {last}→{click} 的垂线 {new_line[1]}→{new_line[0]}")

                            else:
                                log.warning("重复垂线已存在，操作忽略")
                            last=None                    

        if not passed:
            if check(points,lines,circles,level["given_points"]):
                passed=True
                if current_level==3:
                    tool4=True
                    log.info("解锁工具：垂直平分线")
                if current_level==10:
                    tool5=True
                    log.info("解锁工具：角平分线")
                if current_level==18:
                    tool6=True
                    log.info("解锁工具：垂线")
                pass_time=time.time()-start_time
                score,grade=sc.calculate_score(step,e,pass_time,level)
                sa.save_score(current_level+1,step,e,int(pass_time),grade)
                log.info(f"过关！步数{step} 元素数{e} 用时{int(pass_time)}s 评级{grade}")
        if passed:
            ui.draw_pass_screen(screen,step,e,int(pass_time),level,score,grade)

        #重新画一遍
        ui.draw_toolbar(screen,font,number,tool4,tool5,tool6,tools)
        ui.draw_screen_buttons(screen,font,passed,current_level,screen_buttons,len(levels))
        if selecting:
            ui.draw_level_select(screen,levels,sa.load_scores(),current_level,select_page)

        py.display.flip()
        #控制帧率
        clock.tick(60)

        #pygbag必须
        await asyncio.sleep(0)

    lo.log_shutdown()
    py.quit()

asyncio.run(main())