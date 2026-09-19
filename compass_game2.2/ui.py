#这是一个工具包属于compass_game，是一个ui包
import pygame as py
import platform
import sys

IS_WEB=(sys.platform=="emscripten")
OS_NAME=platform.system()
BLACK=(0,0,0)

#2.2新增，缓存
_font_cache={}
def load_font(size):
    if size not in _font_cache:
        if IS_WEB:
            _font_cache[size]=py.font.Font("msyh.ttc", size)
        elif OS_NAME == "Windows":
            _font_cache[size]=py.font.Font("C:/Windows/Fonts/msyh.ttc", size)
        elif OS_NAME == "Darwin":
            _font_cache[size]=py.font.Font("/System/Library/Fonts/PingFang.ttc", size)
        else:
            _font_cache[size]=py.font.Font("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", size)
    return _font_cache[size]

def draw_hud(screen,font,steps,elements,elapsed,level):
    step=font.render(f"步数:{steps}",True,BLACK)
    e=font.render(f"元素数:{elements}",True,BLACK)
    name=font.render(level["name"],True,BLACK)
    goal=font.render("目标："+level["goal"],True,BLACK)
    time=font.render(f"Time:{elapsed}s",True,BLACK)
    screen.blit(step,(10, 10))
    screen.blit(e,(10, 35))
    screen.blit(name,(10,60))
    screen.blit(goal,(10,85))
    screen.blit(time,(10,110))
def draw_pass_screen(screen,step_count,element_count,pass_time,level,score,grade):
    overlay=py.Surface((800,640))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay,(0,0))
    big_font=load_font(48)
    mid_font=load_font(28)

    __name=big_font.render("过关！",True,(255,255,255))
    __grade=mid_font.render(grade,True,(255,215,0))
    __then=mid_font.render(f"步数:{step_count},元素数:{element_count},时间:{pass_time},分数:{score:.2f}",True,(255,255,255))
    screen.blit(__name,(400-__name.get_width()//2,250))
    screen.blit(__grade,(400-__grade.get_width()//2,300))
    screen.blit(__then,(400-__then.get_width()//2,350))

#由main.py搬入
def draw_toolbar(screen,font,current_tool,tool4_unlocked,tool5_unlocked,tools):
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
def check_toolbar_click(pos,tool4_unlocked,tool5_unlocked,tools):
    total_width=len(tools)*100+(len(tools)-1)*10
    start_x=(800-total_width)//2
    button_y=640+20//2
    for i,tool in enumerate(tools):
        x=start_x+i*110
        if x<=pos[0]<=x+100 and button_y<=pos[1]<=button_y+40:
            if tool["num"]==4 and not tool4_unlocked:
                return None
            elif tool["num"]==5 and not tool5_unlocked:
                return None
            return tool["num"]
    return None
def draw_screen_buttons(screen,font,passed,current_level,screen_buttons,total_levels):
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
def check_screen_button_click(pos,screen_buttons):
    for i in screen_buttons:
        if i["x"]<=pos[0]<=i["x"]+i["w"] and\
           i["y"]<=pos[1]<=i["y"]+i["h"]:
            return i["action"]
    return None