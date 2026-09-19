#这是一个工具包属于compass_game，是一个存档包
import json
import os
import sys
import base64
import hashlib

IS_WEB=(sys.platform=="emscripten")
if IS_WEB:
    from platform import window
    localStorage=window.localStorage

if getattr(sys,'frozen',False):
    BASE_DIR=os.path.dirname(sys.executable)
else:
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
__savefile__=os.path.join(BASE_DIR,"scores.dat")
__progressfile__=os.path.join(BASE_DIR,"progress.dat")
__key="compass_game_2026"

def __read__(filename):
    if IS_WEB:
        return localStorage.getItem(filename)
    else:
        path=os.path.join(BASE_DIR,filename)
        if os.path.exists(path):
            with open(path,"r",encoding="utf-8") as f:
                return f.read()
        return None
def __write__(filename,content):
    if IS_WEB:
        localStorage.setItem(filename, content)
    else:
        path=os.path.join(BASE_DIR,filename)
        with open(path,"w",encoding="utf-8") as f:
            f.write(content)

def make_checksum(data_str):
    #生成校验码：数据+密钥一起算MD5
    return hashlib.md5((data_str+__key).encode()).hexdigest()

def load_scores():
    __content=__read__("scores.dat")
    if __content is None:
        return {}
    try:
        raw=base64.b64decode(__content).decode("utf-8")
        #content格式："校验码|Base64数据"
        data_str,checksum=raw.split("|",1)
        if hashlib.md5((data_str+__key).encode()).hexdigest()==checksum:
            return json.loads(data_str)
    except:
        pass
    return {}#校验失败返回空
def save_score(level_num,steps,elements,elapsed,grade):
    scores=load_scores()
    #scores[str(level_num)]={
    #    "steps":steps,
    #    "elements":elements,
    #    "elapsed":elapsed,
    #    "grade":grade
    #}
    key=str(level_num)
    grade_order={"S":5,"A":4,"B":3,"C":2,"D":1}
    new={"steps":steps,"elements":elements,"time":elapsed,"grade":grade}
    if key not in scores:
        scores[key]=new
    else:
        old=scores[key]
        if grade_order[grade]>grade_order[old["grade"]] or\
           (grade==old["grade"] and steps<old["steps"]):
            scores[key]=new
    data_str=json.dumps(scores,ensure_ascii=False)
    checksum=hashlib.md5((data_str+__key).encode()).hexdigest()
    __content=base64.b64encode(f"{data_str}|{checksum}".encode("utf-8")).decode("utf-8")
    __write__("scores.dat",__content)
def load_all_progress():
    __content=__read__("progress.dat")
    if __content is None:
            return {}
    try:
        raw=base64.b64decode(__content).decode("utf-8")
        #content格式："校验码|Base64数据"
        data_str,checksum=raw.split("|",1)
        #Base64解码
        if hashlib.md5((data_str+__key).encode()).hexdigest()==checksum:
            return json.loads(data_str)
    except:
        pass
    return {}#校验失败返回空
def save_progress(name,current_level):
    data=load_all_progress()
    data[name]={
        "current_level":current_level,
    }
    data_str=json.dumps(data)
    checksum=hashlib.md5((data_str+__key).encode()).hexdigest()
    content=base64.b64encode(f"{data_str}|{checksum}".encode("utf-8")).decode("utf-8")
    __write__("progress.dat",content)
def load_progress(name):
    data=load_all_progress()
    if name in data:
        return data[name]["current_level"]
    return None
