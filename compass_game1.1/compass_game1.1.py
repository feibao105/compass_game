import pygame as py
import sys
import geometry as geo

#创建一个窗口
py.init()
screen=py.display.set_mode((800,600))
py.display.set_caption("尺规作图1.1")
clock=py.time.Clock()

WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,225)
RED=(225,0,0)

running=True
number=0
lines=[]
circles=[]
points=[]
last=None

print("0:空 1:点 2:线 3:圆")

#辅助函数
def if_add_point(pt,points,tolerance=3):
    #如果pt和points里的点距离小于tolerance就不再加了
    for i in points:
        if geo.distance(pt,i)<tolerance:
            return
    points.append(pt)

while running:
    screen.fill(WHITE)
    #每一帧重绘
    for i in lines:
        py.draw.line(screen,BLACK,i[0],i[1],2)
    for i in circles:
        #利用勾股定理算距离
        r=int(((i[0][0]-i[1][0])**2+(i[0][1]-i[1][1])**2)**0.5)
        py.draw.circle(screen,BLACK,i[0],r,2)
    for i in points:
        py.draw.circle(screen,BLUE,i,4,0)
    #跟着鼠标画预览
    if last is not None:
        mouse=py.mouse.get_pos()
        if number==2:
            py.draw.line(screen,RED,last,mouse,1)
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
        elif i.type==py.MOUSEBUTTONDOWN:
            if i.button==1:
                if number==0:
                    print("当前选择：空")
                    continue
                if number==1:
                    points.append(i.pos)
                elif number==2:
                    if last is None:
                        last=i.pos
                        if_add_point(last,points)
                    else:
                        lines.append((last,i.pos))
                        if_add_point(i.pos,points)

                        #求交点
                        for j in lines:
                            if j==(last,i.pos):
                                continue
                            new_point=geo.line_line(j[0],j[1],last,i.pos)
                            if new_point is not None:
                                if_add_point(new_point,points)
                        for j in circles:
                            r=geo.distance(j[0],j[1])
                            new_point=geo.line_circle(last,i.pos,j[0],r)
                            if new_point is not None:
                                for k in new_point:
                                    if_add_point(k,points)
                        last=None
                elif number==3:
                    if last is None:
                        last=i.pos
                        if_add_point(last,points)
                    else:
                        circles.append((last,i.pos))
                        if_add_point(last,points)
                        center=last
                        r=geo.distance(last,i.pos)

                        #求交点
                        for j in lines:
                            new_point=geo.line_circle(j[0],j[1],center,r)
                            if new_point is not None:
                                for k in new_point:
                                    if_add_point(k,points)
                        for j in circles:
                            temp=geo.distance(j[0],j[1])
                            if j[0]==center and j[1]==i.pos:
                                continue
                            new_point=geo.circle_circle(j[0],temp,center,r)
                            if new_point is not None:
                                for k in new_point:
                                    if_add_point(k,points)
                        last=None
    py.display.flip()
    #控制帧率
    clock.tick(60)


py.quit()
sys.exit()