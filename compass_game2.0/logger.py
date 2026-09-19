#这是一个工具包属于compass_game，是写日志的包
import logging,time,os,sys
import pygame as py

if getattr(sys,'frozen',False):
    dir=os.path.dirname(sys.executable)
else:
    dir=os.path.dirname(os.path.abspath(__file__))
__start_time=time.time()

def setup_logger():
    #初始化日志系统，返回logger对象
    log_path=os.path.join(dir,"compass_game.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="[%(asctime)s][%(levelname)s]%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8"
    )
    logging.info(f"游戏启动,pygame{py.ver},Python{sys.version.split()[0]},系统{sys.platform}")
    return logging.getLogger()

def log_shutdown():
    #程序退出时调用，记录运行时长
    elapsed=int(time.time()-__start_time)
    logging.info(f"游戏退出，运行时长{elapsed}s")