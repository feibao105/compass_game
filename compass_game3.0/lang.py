#这是一个工具包属于compass_game，是中英文语言包
#用法：界面上要显示中文的地方，用lang.T("中文")包一层；
#关卡名/目标用lang.level_name(序号,中文名)/lang.level_goal(序号,中文目标)
import sys
import os

IS_WEB=(sys.platform=="emscripten")
if IS_WEB:
    from platform import window

LANG="zh"

#界面短句翻译（中文作为钥匙，找不到就原样返回中文）
_EN={
    #屏幕按钮
    "存档":"Save","读档":"Load","上一关":"Prev","下一关":"Next",
    "重开":"Reset","撤销":"Undo","选关":"Levels",
    #工具栏
    "空":"None","点":"Point","线":"Line","圆":"Circle",
    "垂直平分线":"Perp.Bis","角平分线":"Ang.Bis","垂线":"Perp.",
    #选关界面
    "选择关卡":"Select Level","未通关":"Not cleared","锁定":"Locked",
    "上一页":"Prev","下一页":"Next",
    #过关面板
    "过关！":"Clear!",
}

#23关的英文名（按关卡顺序，从0开始数）
LEVEL_NAME_EN=[
    "Tutorial: Triangle",        #1 教程：作三角形
    "Equilateral Triangle",      #2 作等边三角形
    "60° Angle",                 #3 60度角
    "Perpendicular Bisector",    #4 垂直平分线
    "Midpoint",                  #5 作中点
    "Incircle of Square",        #6 正方形的内切圆
    "Rhombus in Rectangle",      #7 矩形的内接菱形
    "Find the Center",           #8_1 做圆心
    "Find the Center",           #8_2 做圆心
    "Inscribed Square",          #9_1 做内接正方形
    "Angle Bisector",            #10 做角平分线
    "Rhombus in Triangle",       #11 三角形的内接菱形
    "30° Angle",                 #12 三十度角
    "Double Angle",              #13 二倍角
    "Bisect the Rectangle",      #14 分割矩形
    "Perp. from Outer Point",    #15_1 过直线外一点作垂线
    "Perp. from Outer Point",    #15_2
    "Perp. at Point on Line",    #16_1 过直线上一点作垂线
    "Perp. at Point on Line",    #16_2
    "Tangent to Circle",         #17_1 作与圆切于某点的直线
    "Tangent to Circle",         #17_2
    "Circle Tangent to Line",    #18 作与直线相切的圆
    "Incircle of Rhombus",       #19 作菱形的内切圆
    "Construct the Chord",       #20 已知中点作弦
    "Orthocenter O",             #21_1 垂心为O的三角形
    "Orthocenter O",             #21_2
    "Circumcenter O",            #22 外心为O的三角形
    "BD = DM = ME",              #23 BD=DM=ME
    "Circle Tangent at B",       #24_1 切于定点的圆
    "Circle Tangent at B",       #24_2
    "Trapezoid Base Midpoint",   #25_1 梯形底边的中点
    "Trapezoid Base Midpoint",   #25_2
    "45° Angle",                 #26_1 45度角
    "45° Angle",                 #26_2
    "45° Rhombus",               #27_1 45度菱形
    "45° Rhombus",               #27_2
]

#23关的英文目标
LEVEL_GOAL_EN=[
    "Connect the three points to form a triangle",
    "Construct the third vertex of an equilateral triangle on the given side",
    "Construct a 60° angle on the given ray",
    "Construct the perpendicular bisector of the segment",
    "Find the midpoint of the segment",
    "Construct the incircle of the given square",
    "Inscribe a rhombus in the rectangle",
    "Locate the center of the circle",
    "Locate the center of the circle",
    "Inscribe a square in the circle",
    "Bisect the given angle",
    "Inscribe a rhombus in the triangle",
    "Construct a 30° angle",
    "Double the given angle",
    "Split the rectangle into two equal-area parts",
    "Construct a perpendicular to the line",
    "Construct a perpendicular to the line",
    "Construct a perpendicular to the line",
    "Construct a perpendicular to the line",
    "Construct the tangent to the circle at the given point",
    "Construct the tangent to the circle at the given point",
    "With the given center, draw a circle tangent to the line",
    "Construct the incircle of the rhombus",
    "Given the midpoint of a chord, construct the chord",
    "Join the two sides of the angle so that O is the orthocenter",
    "Join the two sides of the angle so that O is the orthocenter",
    "Join the two sides of the angle so that O is the circumcenter",
    "Find D on BA and E on BC so that BD = DM = ME",
    "Draw a circle through A, tangent to the line at B",
    "Draw a circle through A, tangent to the line at B",
    "Construct a line through the midpoint of the trapezoid's base",
    "Construct a line through the midpoint of the trapezoid's base",
    "Construct a 45° angle on the given ray",
    "Construct a 45° angle on the given ray",
    "Construct a rhombus with a 45° vertex on the given ray",
    "Construct a rhombus with a 45° vertex on the given ray",
]

def T(s):
    #短句翻译：英文模式查表，中文模式原样返回
    if LANG=="en":
        return _EN.get(s,s)
    return s

def level_name(index,zh_name):
    if LANG=="en" and 0<=index<len(LEVEL_NAME_EN):
        return LEVEL_NAME_EN[index]
    return zh_name

def level_goal(index,zh_goal):
    if LANG=="en" and 0<=index<len(LEVEL_GOAL_EN):
        return LEVEL_GOAL_EN[index]
    return zh_goal

def hud_rows(level_index,level_total,zh_name,zh_goal,steps,best_steps,elements,best_e,elapsed):
    #HUD四行文字，中英文两套格式
    name=level_name(level_index,zh_name)
    goal=level_goal(level_index,zh_goal)
    if LANG=="en":
        return [f"Level {level_index+1} / {level_total} · {name}",
                "Goal: "+goal,
                f"Steps:{steps}/{best_steps}   Elements:{elements}/{best_e}",
                f"Time:{elapsed}s"]
    return [f"第{level_index+1} / {level_total}关·{name}",
            "目标："+goal,
            f"步数:{steps}/{best_steps}    元素数:{elements}/{best_e}",
            f"用时:{elapsed}s"]

def pass_lines(step_count,element_count,pass_time,score):
    #过关面板的两行小字
    if LANG=="en":
        return (f"Steps:{step_count}, Elements:{element_count}, Time:{pass_time}",
                f"Score:{score:.2f}")
    return (f"步数:{step_count},元素数:{element_count},时间:{pass_time}",
            f"分数:{score:.2f}")

#语言选择的保存/读取
def _path():
    if getattr(sys,'frozen',False):
        base=os.path.dirname(sys.executable)
    else:
        base=os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base,"lang.dat")

def load_lang():
    global LANG
    try:
        if IS_WEB:
            v=window.localStorage.getItem("lang.dat")
        else:
            if os.path.exists(_path()):
                with open(_path(),"r",encoding="utf-8") as f:
                    v=f.read()
            else:
                v=None
        if v in ("zh","en"):
            LANG=v
    except:
        pass

def toggle():
    global LANG
    LANG="en" if LANG=="zh" else "zh"
    try:
        if IS_WEB:
            window.localStorage.setItem("lang.dat",LANG)
        else:
            with open(_path(),"w",encoding="utf-8") as f:
                f.write(LANG)
    except:
        pass
