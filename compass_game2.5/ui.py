#这是一个工具包属于compass_game，是一个ui包
import pygame as py
import platform
import sys
import lang

IS_WEB=(sys.platform=="emscripten")
OS_NAME=platform.system()
BLACK=(0,0,0)
PAPER=(250,247,240)   #米色纸背景
GRID=(232,226,210)    #网格线
GRID_AX=(210,200,175) #中心十字线
GIVEN=(70,70,70)      #给定元素：深灰
INK=(40,80,160)       #玩家画的：墨蓝
PT_GIVEN=(30,130,80)  #给定点：墨绿
TEXT=(60,60,60)       #文字
BTN_BG=(255,255,255)
BTN_BD=(205,198,180)  #按钮描边
BTN_SH=(215,208,190)  #按钮阴影
HUD_BG=(247,243,234)
GOLD=(212,175,55)

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

def draw_hud(screen,font,steps,__step,elements,__elements,elapsed,level,level_index,level_total):
    _=py.Rect(8,8,550,150)
    py.draw.rect(screen,HUD_BG,_,border_radius=10)
    py.draw.rect(screen,BTN_BD,_,1,border_radius=10)
    texts=lang.hud_rows(level_index,level_total,level["name"],level["goal"],steps,__step,elements,__elements,elapsed)
    colors=[INK,TEXT,TEXT,TEXT]
    for i,(t,c) in enumerate(zip(texts,colors)):
        screen.blit(font.render(t,True,c),(20,18+i*32))
    #2.5加入了中英互译,见上
    """rows=[
        (f"第{level_index+1} / {level_total}关·{level['name']}",INK),
        ("目标："+level["goal"],TEXT),
        (f"步数:{steps}/{__step}    元素数:{elements}/{__elements}",TEXT),
        (f"用时:{elapsed}s",TEXT)
    ]
    for i,(t,c) in enumerate(rows):
        screen.blit(font.render(t,True,c),(20,18+i*32))"""
def draw_pass_screen(screen,step_count,element_count,pass_time,level,score,grade):
    overlay=py.Surface((800,640),py.SRCALPHA)
    overlay.fill((60,55,45,120))
    screen.blit(overlay,(0,0))
    big_font=load_font(48)
    mid_font=load_font(28)

    card=py.Rect(220,190,360,280)
    py.draw.rect(screen,BTN_SH,card.move(3,4),border_radius=16)
    py.draw.rect(screen,BTN_BG,card,border_radius=16)
    py.draw.rect(screen,BTN_BD,card,1,border_radius=16)

    __name=big_font.render(lang.T("过关！"),True,TEXT)
    __grade=big_font.render(grade,True,GOLD)
    #2.5用lang模块
    __1,__2=lang.pass_lines(step_count,element_count,pass_time,score)
    __then=mid_font.render(__1,True,TEXT)
    ___then=mid_font.render(__2,True,TEXT)
    screen.blit(__name,(400-__name.get_width()//2,220))
    screen.blit(__grade,(400-__grade.get_width()//2,285))
    screen.blit(__then,(400-__then.get_width()//2,365))
    screen.blit(___then,(400-___then.get_width()//2,405))

#2.3新增,ui美化
def tool_rects(tools):
    #工具栏按钮布局（短名80宽，长名110宽）画和点都用它，保证对齐
    widths=[80 if len(t["name"])<=2 else 110 for t in tools]
    total=sum(widths)+10*(len(tools)-1)
    x=(800-total)//2
    rects=[]
    for w in widths:
        rects.append((x,650,w,38))
        x+=w+10
    return rects
def draw_button(screen,rect,text,font,state="normal"):
    #通用圆角按钮，state:normal/active/disabled
    x,y,w,h=rect
    py.draw.rect(screen,BTN_SH,(x+2,y+2,w,h),border_radius=8)
    if state=="active":
        py.draw.rect(screen,INK,rect,border_radius=8)
        color=(255,255,255)
    elif state=="disabled":
        py.draw.rect(screen,(240,237,230),rect,border_radius=8)
        color=(170,170,170)
    else:
        py.draw.rect(screen,BTN_BG,rect,border_radius=8)
        color=TEXT
    py.draw.rect(screen,BTN_BD,rect,1,border_radius=8)
    label=font.render(text,True,color)
    screen.blit(label,(x+(w-label.get_width())//2,y+(h-label.get_height())//2))

#由main.py搬入
def draw_toolbar(screen,font,current_tool,tool4_unlocked,tool5_unlocked,tool6_unlocked,tools):
    # 画工具栏背景
    py.draw.rect(screen,(240,236,226),(0,640,800,60))
    
    #计算按钮起始x，居中排列
    total_width=len(tools)*100+(len(tools)-1)*10
    start_x=(800-total_width)//2
    button_y=650
    
    for tool,rect in zip(tools,tool_rects(tools)):
        #判断按钮状态
        locked=(tool["num"]==4 and not tool4_unlocked) or\
               (tool["num"]==5 and not tool5_unlocked) or\
               (tool["num"]==6 and not tool6_unlocked)
        if locked:
            state="disabled"
        elif tool["num"]==current_tool:
            state="active"
        else:
            state="normal"
        #画按钮
        draw_button(screen,rect,lang.T(tool["name"]),font,state)
def check_toolbar_click(pos,tool4_unlocked,tool5_unlocked,tool6_unlocked,tools):
    for tool,(x,y,w,h) in zip(tools,tool_rects(tools)): 
        if x<=pos[0]<=x+w and y<=pos[1]<=y+h:
            if tool["num"]==4 and not tool4_unlocked:
                return None
            elif tool["num"]==5 and not tool5_unlocked:
                return None
            elif tool["num"]==6 and not tool6_unlocked:
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
        state="normal"if enabled else "disabled"
        draw_button(screen,(i["x"],i["y"],i["w"],i["h"]),lang.T(i["name"]),font,state)
def check_screen_button_click(pos,screen_buttons):
    for i in screen_buttons:
        if i["x"]<=pos[0]<=i["x"]+i["w"] and\
           i["y"]<=pos[1]<=i["y"]+i["h"]:
            return i["action"]
    return None

#2.3新增,ui美化
def draw_paper(screen):
    #坐标纸背景（替代screen.fill(WHITE)）
    screen.fill(PAPER)
    #画坐标系
    for x in range(0,801,40):
        py.draw.line(screen,GRID,(x,0),(x,640))
    for y in range(0,641,40):
        py.draw.line(screen,GRID,(0,y),(800,y))
    #画中心十字线
    py.draw.line(screen,GRID_AX,(400,0),(400,640))
    py.draw.line(screen,GRID_AX,(0,320),(800,320))

#2.4新增，选关界面
def level_cell_rects(level_count):
    #关卡格子的位置，画和点都用它，保证对齐（和tool_rects一个思路）
    cols=5
    w,h,gap=120,80,12
    start_x=(800-(cols*w+(cols-1)*gap))//2
    start_y=110
    rects=[]
    for i in range(level_count):
        r,c=divmod(i,cols)
        rects.append((start_x+c*(w+gap),start_y+r*(h+gap),w,h))
    return rects

def is_level_unlocked(index,scores):
    #第1关永远开放；第N关开放=N-1关有成绩
    if index==0:
        return True
    return str(index) in scores

def draw_level_select(screen,levels,scores,current_level):
    #半透明遮罩
    overlay=py.Surface((800,700),py.SRCALPHA)
    overlay.fill((60,55,45,150))
    screen.blit(overlay,(0,0))
    #标题
    title_font=load_font(36)
    title=title_font.render(lang.T("选择关卡"),True,(255,255,255))
    screen.blit(title,(400-title.get_width()//2,50))
    num_font=load_font(28)
    small_font=load_font(14)
    grade_font=load_font(20)
    for i,(rect,lv) in enumerate(zip(level_cell_rects(len(levels)),levels)):
        x,y,w,h=rect
        unlocked=is_level_unlocked(i,scores)
        record=scores.get(str(i+1))
        #格子底色：当前关金色描边，未解锁灰色
        if unlocked:
            py.draw.rect(screen,BTN_BG,rect,border_radius=10)
        else:
            py.draw.rect(screen,(200,196,188),rect,border_radius=10)
        border=GOLD if i==current_level else BTN_BD
        py.draw.rect(screen,border,rect,2 if i==current_level else 1,border_radius=10)
        #关卡号
        num_color=TEXT if unlocked else (150,150,150)
        num=num_font.render(str(i+1),True,num_color)
        screen.blit(num,(x+8,y+6))
        #成绩
        if record:
            g=grade_font.render(record["grade"],True,GOLD)
            screen.blit(g,(x+w-g.get_width()-8,y+8))
        elif unlocked:
            g=small_font.render(lang.T("未通关"),True,(170,170,170))
            screen.blit(g,(x+w-g.get_width()-8,y+12))
        else:
            g=small_font.render(lang.T("未解锁"),True,(150,150,150))
            screen.blit(g,(x+w-g.get_width()-8,y+12))
        #关卡名（太长就截断）
        name=lv["name"]
        if small_font.size(name)[0]>w-16:
            while name and small_font.size(name+"…")[0]>w-16:
                name=name[:-1]
            name=name+"…"
        nm=small_font.render(name,True,num_color)
        screen.blit(nm,(x+8,y+h-nm.get_height()-8))

def check_level_select_click(pos,levels,scores):
    #点到格子：解锁返回关卡号，没解锁返回None；点到空白返回"close"
    for i,(x,y,w,h) in enumerate(level_cell_rects(len(levels))):
        if x<=pos[0]<=x+w and y<=pos[1]<=y+h:
            if is_level_unlocked(i,scores):
                return i
            return None
    return "close"