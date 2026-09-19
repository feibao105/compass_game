#这是一个工具包属于compass_game，是计算分数的包
def calculate_score(steps,elements,elapsed,level):
    step=steps/level["best_steps"]
    e=elements/level["best_e"]
    time=elapsed/level["time"]

    score=step*0.5+e*0.3+time*0.2
    if score<=1.0:
        return (score,"S")
    elif score<=1.3:
        return (score,"A")
    elif score<=1.7:
        return (score,"B")
    elif score<=2.5:
        return (score,"C")
    else:
        return (score,"D")