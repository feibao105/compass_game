#这是一个工具包属于compass_game，是一个ui包
import pygame as py
BLACK=(0,0,0)
import platform
import sys

IS_WEB=(sys.platform=="emscripten")
OS_NAME = platform.system()
def load_font(size):
    if IS_WEB:
        return py.font.Font("msyh.ttc", size)           # 网页版用默认字体
    elif OS_NAME == "Windows":
        return py.font.Font("C:/Windows/Fonts/msyh.ttc", size)
    elif OS_NAME == "Darwin":                       # Mac
        return py.font.Font("/System/Library/Fonts/PingFang.ttc", size)
    else:                                            # Linux
        return py.font.Font("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", size)
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
    __tip=mid_font.render("按R重新开始",True,(200,200,200))
    __tip2=mid_font.render("按A键进入上一关，按D键进入下一关",True,(200,200,200))
    __tip3=mid_font.render("需用英文输入法",True,(200,200,200))
    screen.blit(__name,(400-__name.get_width()//2,180))
    screen.blit(__grade,(400-__grade.get_width()//2,250))
    screen.blit(__then,(400-__then.get_width()//2,300))
    screen.blit(__tip,(400-__tip.get_width()//2,350))
    screen.blit(__tip2,(400-__tip2.get_width()//2,400))
    screen.blit(__tip3,(400-__tip3.get_width()//2,450))