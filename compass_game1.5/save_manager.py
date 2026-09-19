#这是一个工具包属于compass_game，是一个存档包
import json
import os
import sys
import base64
import hashlib

if getattr(sys,'frozen',False):
    BASE_DIR=os.path.dirname(sys.executable)
else:
    BASE_DIR=os.path.dirname(os.path.abspath(__file__))
__savefile__=os.path.join(BASE_DIR,"scores.dat")
__progressfile__=os.path.join(BASE_DIR,"progress.dat")
__key="compass_game_2026"

def make_checksum(data_str):
    #生成校验码：数据+密钥一起算MD5
    return hashlib.md5((data_str+__key).encode()).hexdigest()

def load_scores():
    if not os.path.exists(__savefile__):
        return {}
    try:
        with open(__savefile__,"r",encoding="utf-8") as f:
            content=f.read()
        #content格式："校验码|Base64数据"
        checksum,encoded_data=content.split("|",1)
        #Base64解码
        data_str=base64.b64decode(encoded_data.encode()).decode()
        if checksum!=make_checksum(data_str):
            #校验不通过，被改过了，重置
            return {}
        return json.loads(data_str)
    except:
        return {}
def save_score(level_num,steps,elements,elapsed,grade):
    scores=load_scores()
    key=str(level_num)
    grade_order={"S":5,"A":4,"B":3,"C":2,"D":1}
    if key not in scores:
        scores[key]={"steps":steps,"elements":elements,"time":elapsed,"grade":grade}
    else:
        old=scores[key]
        if grade_order[grade]>grade_order[old["grade"]] or\
           (grade==old["grade"] and steps<old["steps"]):
            scores[key]={"steps":steps,"elements":elements,"time":elapsed,"grade":grade}
    data_str=json.dumps(scores,ensure_ascii=False)
    checksum=make_checksum(data_str)
    encoded=base64.b64encode(data_str.encode()).decode()
    with open(__savefile__,"w",encoding="utf-8") as f:
        f.write(checksum+"|"+encoded)
def load_all_progress():
    if not os.path.exists(__progressfile__):
            return {}
    try:
        with open(__progressfile__,"r",encoding="utf-8") as f:
            content=f.read()
        #content格式："校验码|Base64数据"
        checksum,encoded_data=content.split("|",1)
        #Base64解码
        data_str=base64.b64decode(encoded_data.encode()).decode()
        if checksum!=make_checksum(data_str):
            #校验不通过，被改过了，重置
            return {}
        return json.loads(data_str)
    except:
        return {}
def save_progress(name,current_level):
    data=load_all_progress()
    import time
    data[name]={
        "current_level":current_level,
        "time":time.strftime("%Y-%m-%d %H:%M:%S")
    }
    data_str=json.dumps(data,ensure_ascii=False)
    checksum=make_checksum(data_str)
    encoded=base64.b64encode(data_str.encode()).decode()
    with open(__progressfile__,"w",encoding="utf-8") as f:
        f.write(checksum+"|"+encoded)
def load_progress(name):
    data=load_all_progress()
    if name in data:
        return data[name]["current_level"]
